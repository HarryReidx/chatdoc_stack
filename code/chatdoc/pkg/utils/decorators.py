'''
Author: longsion<xianglong_chen@intsig.net>
Date: 2024-04-25 16:24:15
LastEditors: longsion
LastEditTime: 2024-10-15 16:53:47
'''


import time
import json
import datetime
import traceback
from functools import wraps

from pydantic import BaseModel
from pkg.utils.logger import logger
from pkg.utils.jaeger import tracer
from enum import Enum


class CustomerEncoder(json.JSONEncoder):
    """
    自定义的 JSON 编码器：
    - 支持将 Enum 枚举类型自动转换为其值（value），方便序列化成 JSON 字符串。
    """
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


def register_span_func(func_name: str = None, span_export_func: callable = None, update_durations=True):
    """
    OpenTelemetry 跟踪的装饰器，用于记录函数执行过程中的性能指标和异常信息。

    参数:
        - func_name (str): 自定义的函数名，如果为 None，则使用原始函数名。
        - span_export_func (callable): 可选的导出 span trace 的函数（暂时注释掉未启用）。
        - update_durations (bool): 是否更新上下文对象中的 durations 字典以记录函数耗时。

    返回:
        - 装饰器函数，包装原函数以增加 tracing 和日志功能。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            __func_name_ = func_name or func.__name__

            # 创建一个 tracing span
            with tracer.start_as_current_span(__func_name_) as span:
                start_time = time.time()
                # 开始计时
                start_time_str = str(datetime.datetime.now())

                try:
                    result = func(*args, **kwargs)  # 调用原始函数
                    return result
                except Exception as e:
                    # 异常捕捉和日志记录
                    logger.error(f"Error in {__func_name_}: {e}, traceback: {traceback.format_exc()}")
                    raise e
                finally:
                    end_time = time.time()
                    logger.info(f"Span: {__func_name_} start at {start_time_str}, duration: {(end_time - start_time)*1000:.1f}ms")

                    # 如启用耗时记录，将时间写入上下文对象
                    if update_durations:
                        if "context" in kwargs:
                            context = kwargs.get("context")
                        else:
                            context = args[0] if args else None

                        if context and isinstance(context, BaseModel) and hasattr(context, "durations") and isinstance(context.durations, dict) and hasattr(context, "start_ts"):
                            context.durations.update(
                                {
                                    func_name: dict(
                                        start=f"{(start_time - context.start_ts)*1000:.1f}ms",
                                        duration=f"{(end_time - start_time) * 1000:.1f}ms"
                                    )
                                }
                            )

        return wrapper

    return decorator
