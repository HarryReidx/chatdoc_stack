'''
整体作用: 
本代码实现了一个多路召回系统，用于从文档中检索相关表格和段落信息。支持两种召回模式：分析员模式（ANALYST）和个人模式（PERSONAL）。
根据用户输入的上下文（Context），通过多线程并行执行表格和段落召回，并对召回结果进行过滤，以去除无关或重复内容。最终返回包含召回结果的上下文对象。
'''

import re
from difflib import get_close_matches
from pkg.es.es_doc_table import DocTableES, DocTableModel
from pkg.es.es_doc_fragment import DocFragmentES, DocFragmentModel
from pkg.es.es_file import ESFileObject
from pkg.es.es_p_doc_fragment import PDocFragmentES, PDocFragmentModel
from pkg.es.es_p_doc_table import PDocTableES, PDocTableModel
from pkg.es.es_p_file import PESFileObject
from pkg.utils.decorators import register_span_func
from pkg.global_.objects import Context, GlobalQAType
from pkg.utils.thread_with_return_value import ThreadWithReturnValue
from pkg.utils.logger import logger

def lambda_func(context: Context):
    """
    功能: 将上下文对象的指定字段序列化为字典
    参数: context - 上下文对象，包含查询参数和分析结果
    返回: 包含指定字段的字典
    """
    return context.model_dump(include=[
        "params",
        "trace_id",
        "question_analysis",
        "fixed_table_retrieve_small",
        "normal_table_retrieve_small",
        "fragment_retrieve_small",
    ])


def retrieve_small_full_by_analyst(context: Context) -> Context:
    """
    功能: 分析员模式的全文召回，检索表格和段落
    参数: context - 上下文对象，包含查询参数和分析结果
    返回: 更新后的上下文对象，包含召回的表格和段落
    """
    document_uuids = []
    # 没有选中文件时，进行全局检索，只使用段落召回与表格召回
    _normal_table_retrieve_l = ThreadWithReturnValue(target=retrieve_by_table, args=(context, document_uuids))
    _normal_table_retrieve_l.start()

    _paragraph_retrieve_l = ThreadWithReturnValue(target=retrieve_by_paragraph, args=(context, document_uuids))
    _paragraph_retrieve_l.start()

    normal_table_retrieve_small = _normal_table_retrieve_l.join()
    fragment_retrieve_small = _paragraph_retrieve_l.join()

    # 过滤召回内容
    files = [file for file in context.locationfiles]
    if files:
        filter_uuids = list(set([file.uuid for file in files]))
        normal_table_retrieve_small = [r for r in normal_table_retrieve_small if r.uuid not in filter_uuids]
        fragment_retrieve_small = [r for r in fragment_retrieve_small if r.file_uuid not in filter_uuids]
        if context.question_analysis.companies:
            garbage = ["股份有限公司", "有限公司", "招股说明书", "招股书", "年度报告", "季度报告", "季报"]
            compare_key_infos = []
            for k in context.question_analysis.companies + [context.params.question]:  # 原问题也作为匹配条件
                for g in garbage:
                    k = k.replace(g, "")
                k = re.sub(r'\d{4}年', "", k)
                compare_key_infos.append(k)
            normal_table_retrieve_small = [r for r in normal_table_retrieve_small if
                                           get_ebed(r.ebed_text, compare_key_infos)]
            fragment_retrieve_small = [r for r in fragment_retrieve_small if
                                       get_ebed(r.ebed_text, compare_key_infos)]
    context.normal_table_retrieve_small += normal_table_retrieve_small
    context.fragment_retrieve_small += fragment_retrieve_small

    return context


def retrieve_small_full_by_personal(context: Context) -> Context:
    """
    功能: 个人模式的全文召回，检索表格和段落
    参数: context - 上下文对象，包含查询参数和分析结果
    返回: 更新后的上下文对象，包含召回的表格和段落
    """
    document_uuids = []
    logger.info(">>> 进入retrieve_small_full_by_personal")
    # 打印context内容
    logger.info(context)
    # 没有选中文件时，进行全局检索，只使用段落召回与表格召回
    _normal_table_retrieve_l = ThreadWithReturnValue(target=retrieve_by_personal_table, args=(context, document_uuids))
    _normal_table_retrieve_l.start()

    _paragraph_retrieve_l = ThreadWithReturnValue(target=retrieve_by_personal_paragraph, args=(context, document_uuids))
    _paragraph_retrieve_l.start()

    normal_table_retrieve_small = _normal_table_retrieve_l.join()
    fragment_retrieve_small = _paragraph_retrieve_l.join()

    # 过滤召回内容
    files = [file for file in context.locationfiles]
    if files:
        filter_uuids = list(set([file.uuid for file in files]))
        normal_table_retrieve_small = [r for r in normal_table_retrieve_small if r.uuid not in filter_uuids]
        fragment_retrieve_small = [r for r in fragment_retrieve_small if r.file_uuid not in filter_uuids]
        if context.question_analysis.companies:
            garbage = ["股份有限公司", "有限公司", "招股说明书", "招股书", "年度报告", "季度报告", "季报"]
            compare_key_infos = []
            for k in context.question_analysis.companies + [context.params.question]:  # 原问题也作为匹配条件
                for g in garbage:
                    k = k.replace(g, "")
                k = re.sub(r'\d{4}年', "", k)
                compare_key_infos.append(k)
            normal_table_retrieve_small = [r for r in normal_table_retrieve_small if
                                           get_ebed(r.ebed_text, compare_key_infos)]
            fragment_retrieve_small = [r for r in fragment_retrieve_small if
                                       get_ebed(r.ebed_text, compare_key_infos)]
    context.normal_table_retrieve_small += normal_table_retrieve_small
    context.fragment_retrieve_small += fragment_retrieve_small

    return context


@register_span_func(func_name="多路召回Full", span_export_func=lambda context: lambda_func(context))
def retrieve_small_full(context: Context) -> Context:
    """
    功能: 根据QA类型调用不同的召回函数，支持分析员和个人模式
    参数: context - 上下文对象，包含查询参数和分析结果
    返回: 更新后的上下文对象，包含召回的表格和段落
    """
    logger.info(">>> 进入retrieve_small_full1")
    if context.params.qa_type == GlobalQAType.ANALYST.value:
        context = retrieve_small_full_by_analyst(context)
    elif context.params.qa_type == GlobalQAType.PERSONAL.value:
        context = retrieve_small_full_by_personal(context)
    else:
        personal_t = ThreadWithReturnValue(target=retrieve_small_full_by_personal, args=(context,))
        personal_t.start()
        context = retrieve_small_full_by_analyst(context)
        context = personal_t.join()

    return context


def retrieve_by_table(context: Context, document_uuids: list[str]) -> list[DocTableModel]:
    """
    功能: 从文档中召回表格内容
    参数: 
        context - 上下文对象，包含查询参数和分析结果
        document_uuids - 文档UUID列表
    返回: 召回的表格内容列表
    """
    files = [
        file for file in context.locationfiles if isinstance(file, ESFileObject)
    ]
    if files:
        size = min(4 * len(files), 10)
    else:
        size = 10
    doc_table_items: list[DocTableModel] = []
    threads = []
    for keyword in context.question_analysis.keywords:
        t = ThreadWithReturnValue(target=DocTableES().search_table, kwargs=dict(bm25_text=keyword,
                                                                                ebd_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                document_uuids=document_uuids,
                                                                                size=size))
        t.start()
        threads.append(t)

    for t in threads:
        doc_table_items.extend(t.join())
    return doc_table_items


def retrieve_by_paragraph(context: Context, document_uuids: list[str]) -> list[DocFragmentModel]:
    """
    功能: 从文档中召回段落内容
    参数: 
        context - 上下文对象，包含查询参数和分析结果
        document_uuids - 文档UUID列表
    返回: 召回的段落内容列表
    """
    files = [
        file for file in context.locationfiles if isinstance(file, ESFileObject)
    ]
    if files:
        size = min(20 * len(files), 25)
    else:
        size = 25
    doc_fragment_items: list[DocFragmentModel] = DocFragmentES().search_fragment(bm25_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                 ebd_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                 document_uuids=document_uuids,
                                                                                 size=size)
    return doc_fragment_items


def retrieve_by_personal_table(context: Context, document_uuids: list[str]) -> list[PDocTableModel]:
    """
    功能: 从个人文档中召回表格内容
    参数: 
        context - 上下文对象，包含查询参数和分析结果
        document_uuids - 文档UUID列表
    返回: 召回的表格内容列表
    """
    files = [
        file for file in context.locationfiles if isinstance(file, PESFileObject)
    ]
    if files:
        size = min(4 * len(files), 10)
    else:
        size = 10

    doc_table_items: list[PDocTableModel] = []
    threads = []
    for keyword in context.question_analysis.keywords:
        t = ThreadWithReturnValue(target=PDocTableES().search_table, kwargs=dict(bm25_text=keyword,
                                                                                 ebd_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                 document_uuids=document_uuids,
                                                                                 size=size,
                                                                                 user_id=context.params.user_id))
        t.start()
        threads.append(t)

    for t in threads:
        doc_table_items.extend(t.join())
    return doc_table_items


def retrieve_by_personal_paragraph(context: Context, document_uuids: list[str]) -> list[PDocFragmentModel]:
    """
    功能: 从个人文档中召回段落内容
    参数: 
        context - 上下文对象，包含查询参数和分析结果
        document_uuids - 文档UUID列表
    返回: 召回的段落内容列表
    """
    files = [
        file for file in context.locationfiles if isinstance(file, PESFileObject)
    ]
    if files:
        size = min(20 * len(files), 25)
    else:
        size = 25
    doc_fragment_items: list[PDocFragmentModel] = PDocFragmentES().search_fragment(bm25_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                   ebd_text=context.question_analysis.retrieve_question if document_uuids != [] else context.params.question,
                                                                                   document_uuids=document_uuids,
                                                                                   size=size,
                                                                                   user_id=context.params.user_id)
    return doc_fragment_items


def get_ebed(text, key_infos):
    """
    功能: 判断文本中是否包含关键信息（如公司名）
    参数:
        text - 要检查的文本
        key_infos - 关键信息列表（公司名等）
    返回: 布尔值，True表示包含关键信息，False表示不包含
    步骤:
        1. 如果文本直接与关键信息高度匹配，认为是无效信息，返回False
        2. 将文本按标点分割，若无标点则按字长切分
        3. 检查分割后的文本是否与关键信息匹配
    """
    # 步骤0: 直接匹配检查
    if get_close_matches(text, key_infos, cutoff=0.8):
        return False
    # 步骤1: 按标点分割文本
    pattern = r'[。！!？?，,]'
    text_list_span = re.split(pattern, text)
    text_list_span = [item for item in text_list_span if item.strip()]
    if len(text_list_span) == 1:
        text_list_span = [text[i:i + 20] for i in range(0, len(text), 20)]
    # 步骤2: 逐段匹配关键信息
    for t in text_list_span:
        matches = get_close_matches(t, key_infos, cutoff=0.3)
        if matches:
            return True
        else:
            continue
    return False
