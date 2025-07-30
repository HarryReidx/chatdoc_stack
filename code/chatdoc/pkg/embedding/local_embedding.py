"""
本地嵌入服务 - 替代TEXTIN的嵌入功能
Author: AI Assistant
Date: 2025-07-28
"""
import time
from typing import List, Union
import torch
from sentence_transformers import SentenceTransformer
from pkg.config import config
from pkg.utils.logger import logger
from pkg.utils import retry_exponential_backoff
from pkg.utils.lru_cache import LRUCacheDict, LRUCachedFunction


class LocalEmbeddingService:
    """本地嵌入服务"""
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        初始化本地嵌入服务
        :param model_name: 模型名称
        :param device: 设备 (cpu/cuda)
        """
        self.model_name = model_name or self._get_default_model()
        self.device = device or self._get_device()
        self.model = None
        self._load_model()
    
    def _get_default_model(self) -> str:
        """获取默认模型"""
        # 优先使用配置中的模型，否则使用默认模型
        local_config = config.get("local_services", {}).get("embedding", {})
        return local_config.get("model", "all-mpnet-base-v2")
    
    def _get_device(self) -> str:
        """获取设备"""
        local_config = config.get("local_services", {}).get("embedding", {})
        device = local_config.get("device", "auto")
        
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def _load_model(self):
        """加载模型"""
        try:
            logger.info(f"正在加载嵌入模型: {self.model_name}, 设备: {self.device}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"嵌入模型加载成功")
        except Exception as e:
            logger.error(f"嵌入模型加载失败: {str(e)}")
            # 回退到CPU和更简单的模型
            try:
                logger.info("尝试使用CPU和默认模型")
                self.device = "cpu"
                self.model_name = "all-MiniLM-L6-v2"  # 更小的模型
                self.model = SentenceTransformer(self.model_name, device=self.device)
                logger.info(f"回退模型加载成功: {self.model_name}")
            except Exception as e2:
                logger.error(f"回退模型也加载失败: {str(e2)}")
                raise Exception(f"无法加载任何嵌入模型: {str(e2)}")
    
    def encode_single(self, text: str, dimension: int = 1024, digit: int = 8) -> List[float]:
        """
        单文本嵌入
        :param text: 输入文本
        :param dimension: 维度（暂时忽略，由模型决定）
        :param digit: 精度（暂时忽略）
        :return: 嵌入向量
        """
        if not self.model:
            raise Exception("嵌入模型未加载")
        
        try:
            start_time = time.time()
            embedding = self.model.encode(text, convert_to_tensor=False)
            end_time = time.time()
            
            logger.debug(f"单文本嵌入完成，耗时: {(end_time - start_time)*1000:.1f}ms")
            
            # 转换为列表格式
            if hasattr(embedding, 'tolist'):
                return embedding.tolist()
            else:
                return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
                
        except Exception as e:
            logger.error(f"文本嵌入失败: {str(e)}")
            raise Exception(f"文本嵌入失败: {str(e)}")
    
    def encode_batch(self, texts: List[str], dimension: int = 1024, digit: int = 8) -> List[List[float]]:
        """
        批量文本嵌入
        :param texts: 输入文本列表
        :param dimension: 维度（暂时忽略，由模型决定）
        :param digit: 精度（暂时忽略）
        :return: 嵌入向量列表
        """
        if not self.model:
            raise Exception("嵌入模型未加载")
        
        if not texts:
            return []
        
        try:
            start_time = time.time()
            embeddings = self.model.encode(texts, convert_to_tensor=False, batch_size=32)
            end_time = time.time()
            
            logger.info(f"批量嵌入完成，文本数量: {len(texts)}, 耗时: {(end_time - start_time)*1000:.1f}ms")
            
            # 转换为列表格式
            result = []
            for embedding in embeddings:
                if hasattr(embedding, 'tolist'):
                    result.append(embedding.tolist())
                else:
                    result.append(list(embedding))
            
            return result
                
        except Exception as e:
            logger.error(f"批量文本嵌入失败: {str(e)}")
            raise Exception(f"批量文本嵌入失败: {str(e)}")


# 全局实例
_embedding_service = None

def get_embedding_service() -> LocalEmbeddingService:
    """获取全局嵌入服务实例"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = LocalEmbeddingService()
    return _embedding_service


# 兼容原有接口的函数
@retry_exponential_backoff()
def local_embedding_single(text: str, dimension: int = 1024, digit: int = 8) -> List[float]:
    """
    本地单文本嵌入 - 兼容原acge_embedding接口
    :param text: 输入文本
    :param dimension: 维度
    :param digit: 精度
    :return: 嵌入向量
    """
    service = get_embedding_service()
    return service.encode_single(text, dimension, digit)


@retry_exponential_backoff()
def local_embedding_multi(text_list: List[str], dimension: int = 1024, digit: int = 8, headers=None, url=None) -> List[List[float]]:
    """
    本地批量文本嵌入 - 兼容原acge_embedding_multi接口
    :param text_list: 输入文本列表
    :param dimension: 维度
    :param digit: 精度
    :param headers: 兼容参数（忽略）
    :param url: 兼容参数（忽略）
    :return: 嵌入向量列表
    """
    service = get_embedding_service()
    return service.encode_batch(text_list, dimension, digit)


# LRU缓存支持
local_embedding_lru_cache = LRUCacheDict(max_size=5000, expiration=60 * 60)
local_embedding_with_cache = LRUCachedFunction(local_embedding_single, local_embedding_lru_cache, cache_key_suffix="local_embedding")


# 兼容原有的embedding_multi函数
@retry_exponential_backoff()
def embedding_multi(origin_text: Union[str, List[str]], headers=None, url=None) -> Union[List[float], List[List[float]]]:
    """
    兼容原有的embedding_multi接口
    :param origin_text: 输入文本或文本列表
    :param headers: 兼容参数（忽略）
    :param url: 兼容参数（忽略）
    :return: 嵌入向量或嵌入向量列表
    """
    service = get_embedding_service()
    
    if isinstance(origin_text, str):
        return service.encode_single(origin_text)
    elif isinstance(origin_text, list):
        return service.encode_batch(origin_text)
    else:
        raise ValueError(f"不支持的输入类型: {type(origin_text)}")
