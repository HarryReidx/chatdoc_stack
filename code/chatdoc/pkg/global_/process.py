"""
process.py - ChatDoc 问答主流程控制模块

功能：
- 接收外部请求参数 Params，构造上下文 Context
- 并行执行合规检测与检索
- 进行检索结果重排、截断、生成
- 支持流式输出/非流式问答模式
- 打点耗时、链路追踪、问题合规性控制

作者：longsion
"""

import datetime
import time
from pkg.global_.objects import Params, Context, Response
from pkg.utils.logger import logger
from pkg.utils.decorators import register_span_func
from pkg.config import config
from pkg.utils.thread_with_return_value import ThreadWithReturnValue
from pkg.llm.util import check_repetition, get_stream_json, remove_repetition, set_stream_json, stream_fixes_suffix

from opentelemetry import context as otel_context
from opentelemetry.trace import get_current_span


def process(params: Params) -> Context:
    """
    ChatDoc 问答主流程函数：处理一次用户提问到返回答案的完整链路。
    包括合规检测、检索、重排、上下文构建、生成与追踪等。
    """
    logger.info("启动问答主流程")

    from .compliance_question import compliance_question
    from .preprocess_question import preprocess_question
    from .rerank_by_question import rerank_by_question
    from .small2big import small2big
    from .truncation import truncation
    from .generation import generation
    from .compliance_answer import func as compliance_answer
    from .rerank_by_answer import func as rerank_by_answer
    from .retrieve_small import retrieve_small
    from .retrieve_small_full import retrieve_small_full

    context = Context(params=params)
    context.start_ts = time.time()
    context.durations.update(start=str(datetime.datetime.now()))

    span_ctx = otel_context.get_current()
    # 赋予trace_id
    context.trace_id = f"{get_current_span().context.trace_id:0x}"

    # 启动问题合规性检测线程
    compliance_t = ThreadWithReturnValue(target=compliance_question, args=(context,), parent_span_context=span_ctx)
    compliance_t.start()

    # 问题预处理（意图识别、标准化等）
    logger.info("开始预处理问题")
    context = preprocess_question(context)
    logger.info("预处理完成")

    # 启动全局检索线程
    retrieve_all_t = ThreadWithReturnValue(target=retrieve_small_full, args=(context,))
    retrieve_all_t.start()

    # 等待合规检测完成
    context = compliance_t.join()
    if context.question_compliance is False:
        logger.warning("问题未通过合规性检测")
        context.answer_response = Response(answer=config["compliance"]["warning_text"], question_compliance=False, trace_id=context.trace_id)
        return context

    # 执行局部检索（针对用户选定文档）
    logger.info("开始局部检索")
    context = retrieve_small(context)
    logger.info("局部检索完成")

    # 等待全局检索线程完成
    context = retrieve_all_t.join()

    # rerank：基于问题的相似度重新排序
    logger.info("执行问题级别rerank")
    context = rerank_by_question(context)
    logger.info("问题 rerank 完成")

    # small2big：段落上下文扩展
    logger.info("执行 small2big 拓展段落")
    context = small2big(context)

    # truncation：拼接后做截断，控制上下文大小
    logger.info("执行上下文截断")
    context = truncation(context)

    # no_chat 模式直接返回召回内容
    if context.params.no_chat:
        logger.info("no_chat 模式，直接构造响应")
        context.answer_response = gen_response_by_context(context)
        return context

    # ↓↓↓ 以下为生成环节：流式或非流式 ↓↓↓

    def _on_done(context) -> Response:
        otel_context.attach(span_ctx)

        if context.answer_compliance is False:
            return Response(answer=config["compliance"]["warning_text"], question_compliance=True, answer_compliance=False, trace_id=context.trace_id, durations=context.durations)

        context = compliance_answer(context)
        if context.answer_compliance is False:
            return Response(answer=config["compliance"]["warning_text"], question_compliance=True, answer_compliance=False, trace_id=context.trace_id, durations=context.durations)

        if len(context.files) < 2:
            context = rerank_by_answer(context)

        context = report_process_result(context)
        return gen_response_by_context(context)

    def _after_trunction():
        nonlocal context
        ori = [
            dict(ori_id=ori_id, uuid=r.file_uuid, reference_tag=r.reference_tag, kb=r.kb, i=i)
            for i, r in enumerate(context.rerank_retrieve_before_qa) for ori_id in r.ori_ids
        ]
        context.durations.update(推送召回结果=f"{(time.time() - context.start_ts) * 1000:.1f}ms")
        logger.info(f"推送召回结果 duration: {context.durations['推送召回结果']}")
        yield set_stream_json({
            "status": "DOING", "content": "", "stage": "retrieve_result", "data": dict(source=ori)
        })

        logger.info("开始生成答案")
        context = generation(context)
        logger.info("生成完成")
        yield from _after_generation()

    def _after_generation():
        nonlocal context
        answer_text = ""
        first_ts, last_ts = -1, -1

        for x in context.stream_iter:
            if not answer_text:
                first_ts = time.time()
                context.durations.update(首token=f"{(first_ts - context.start_ts) * 1000:.1f}ms")
                logger.info(f"首token duration: {context.durations['首token']}")

            if x == stream_fixes_suffix:
                last_ts = time.time()
                context.durations.update(
                    尾token=f"{(last_ts - context.start_ts) * 1000:.1f}ms",
                    token速率=f"{len(answer_text)/(last_ts-first_ts):.1f} token/s"
                )
                logger.info(f"尾token duration: {context.durations['尾token']}, token速率: {context.durations['token速率']}")
                yield x
                break

            x_json = get_stream_json(x)
            if x_json["status"] == "DONE":
                context.llm_answer = answer_text
                response = _on_done(context)
                x_json.update(data=response.model_dump_json())
                yield set_stream_json(x_json)
            elif check_repetition(answer_text, x_json["content"]):
                context.llm_answer = remove_repetition(answer_text, x_json["content"])
                response = _on_done(context)
                x_json.update(data=response.model_dump_json(), status="DONE")
                yield set_stream_json(x_json)
                last_ts = time.time()
                context.durations.update(
                    尾token=f"{(last_ts - context.start_ts) * 1000:.1f}ms",
                    token速率=f"{len(answer_text)/(last_ts-first_ts):.1f} token/s"
                )
                logger.info(f"尾token duration: {context.durations['尾token']}, token速率: {context.durations['token速率']}")
                yield stream_fixes_suffix
                break
            else:
                answer_text += x_json["content"]
                yield x

    if context.params.stream:
        context.answer_response_iter = _after_trunction()
    else:
        logger.info("开始生成答案")
        context = generation(context)
        logger.info("生成结束，构造响应对象")
        context.answer_response = _on_done(context)

    return context


def gen_response_by_context(context: Context) -> Response:
    # 增加文件名属性，测试用
    uuid_name_dic = {c.uuid: c.filename for c in context.files + context.locationfiles}
    for r in context.rerank_retrieve_before_qa + context.rerank_retrieve_after_qa:
        r.file_name = uuid_name_dic[r.file_uuid]
    rerank = context.rerank_retrieve_after_qa or context.rerank_retrieve_before_qa
    ori = [
        dict(
            ori_id=ori_id,
            uuid=r.file_uuid,
            i=i  # 返回召回的顺序
        )
        for i, r in enumerate(rerank) for ori_id in r.ori_ids
    ]

    return Response(
        answer=context.llm_answer or "",
        prompt=context.llm_question or "",
        source=ori,
        full=[r.gen_full_return() for r in rerank],
        retrieval={},
        answer_or_iterator=context.llm_answer,
        question_compliance=context.question_compliance,
        answer_compliance=context.answer_compliance,
        trace_id=context.trace_id,
        durations=context.durations,
    )


def func_span(context: Context):

    return dict(
        params=context.params.model_dump(),
        question_analysis=context.question_analysis.model_dump(),
        files=[
            file.model_dump(exclude=["doc_fragments_json"]) for file in context.files
        ],
        llm_question=context.llm_question,
        llm_answer=context.llm_answer,
        question_compliance=context.question_compliance,
        answer_compliance=context.answer_compliance,
        rerank_retrieve_after_qa=[
            dict(
                answer_rerank_score=retrieve_context.answer_rerank_score,
                ori_id=retrieve_context.ori_ids,
                file_uuid=retrieve_context.file_uuid,
                ans_rerank_texts=retrieve_context.ans_rerank_texts,
            )
            for retrieve_context in context.rerank_retrieve_after_qa
        ]
    )


@register_span_func(func_name="问答结果", span_export_func=func_span)
def report_process_result(context: Context):
    return context
