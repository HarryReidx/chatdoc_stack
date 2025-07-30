"""
本地重排序服务 - 替代TEXTIN的重排序功能
Author: AI Assistant
Date: 2025-07-28
"""
import time
from typing import List, Tuple, Union
import torch
from sentence_transformers import CrossEncoder
from pkg.config import config
from pkg.utils.logger import logger
from pkg.utils import retry_exponential_backoff


class LocalRerankService:
    """本地重排序服务"""
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        初始化本地重排序服务
        :param model_name: 模型名称
        :param device: 设备 (cpu/cuda)
        """
        self.model_name = model_name or self._get_default_model()
        self.device = device or self._get_device()
        self.model = None
        self._load_model()
    
    def _get_default_model(self) -> str:
        """获取默认模型"""
        local_config = config.get("local_services", {}).get("rerank", {})
        return local_config.get("model", "cross-encoder/ms-marco-MiniLM-L-12-v2")
    
    def _get_device(self) -> str:
        """获取设备"""
        local_config = config.get("local_services", {}).get("rerank", {})
        device = local_config.get("device", "auto")
        
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def _load_model(self):
        """加载模型"""
        try:
            logger.info(f"正在加载重排序模型: {self.model_name}, 设备: {self.device}")
            self.model = CrossEncoder(self.model_name, device=self.device)
            logger.info(f"重排序模型加载成功")
        except Exception as e:
            logger.error(f"重排序模型加载失败: {str(e)}")
            # 回退到CPU和更简单的模型
            try:
                logger.info("尝试使用CPU和默认模型")
                self.device = "cpu"
                self.model_name = "cross-encoder/ms-marco-TinyBERT-L-2-v2"  # 更小的模型
                self.model = CrossEncoder(self.model_name, device=self.device)
                logger.info(f"回退模型加载成功: {self.model_name}")
            except Exception as e2:
                logger.error(f"回退模型也加载失败: {str(e2)}")
                raise Exception(f"无法加载任何重排序模型: {str(e2)}")
    
    def rerank(self, query: str, documents: List[str], if_softmax: int = 0) -> List[float]:
        """
        重排序文档
        :param query: 查询文本
        :param documents: 文档列表
        :param if_softmax: 是否使用softmax（0或1）
        :return: 重排序分数列表
        """
        if not self.model:
            raise Exception("重排序模型未加载")
        
        if not documents:
            return []
        
        try:
            start_time = time.time()
            
            # 构建查询-文档对
            pairs = [[query, doc] for doc in documents]
            
            # 计算相似度分数
            scores = self.model.predict(pairs)
            
            # 转换为列表格式
            if hasattr(scores, 'tolist'):
                scores = scores.tolist()
            else:
                scores = list(scores)
            
            # 如果需要softmax
            if if_softmax == 1:
                scores = self._apply_softmax(scores)
            
            end_time = time.time()
            logger.info(f"重排序完成，文档数量: {len(documents)}, 耗时: {(end_time - start_time)*1000:.1f}ms")
            
            return scores
                
        except Exception as e:
            logger.error(f"重排序失败: {str(e)}")
            raise Exception(f"重排序失败: {str(e)}")
    
    def _apply_softmax(self, scores: List[float]) -> List[float]:
        """应用softmax函数"""
        import math
        
        # 防止数值溢出
        max_score = max(scores)
        exp_scores = [math.exp(score - max_score) for score in scores]
        sum_exp = sum(exp_scores)
        
        return [exp_score / sum_exp for exp_score in exp_scores]
    
    def rerank_pairs(self, pairs: List[List[str]], if_softmax: int = 0) -> List[float]:
        """
        直接对查询-文档对进行重排序
        :param pairs: 查询-文档对列表，每个元素是[query, document]
        :param if_softmax: 是否使用softmax（0或1）
        :return: 重排序分数列表
        """
        if not self.model:
            raise Exception("重排序模型未加载")
        
        if not pairs:
            return []
        
        try:
            start_time = time.time()
            
            # 计算相似度分数
            scores = self.model.predict(pairs)
            
            # 转换为列表格式
            if hasattr(scores, 'tolist'):
                scores = scores.tolist()
            else:
                scores = list(scores)
            
            # 如果需要softmax
            if if_softmax == 1:
                scores = self._apply_softmax(scores)
            
            end_time = time.time()
            logger.info(f"重排序完成，对数量: {len(pairs)}, 耗时: {(end_time - start_time)*1000:.1f}ms")
            
            return scores
                
        except Exception as e:
            logger.error(f"重排序失败: {str(e)}")
            raise Exception(f"重排序失败: {str(e)}")


# 全局实例
_rerank_service = None

def get_rerank_service() -> LocalRerankService:
    """获取全局重排序服务实例"""
    global _rerank_service
    if _rerank_service is None:
        _rerank_service = LocalRerankService()
    return _rerank_service


# 兼容原有接口的函数
@retry_exponential_backoff()
def rerank_api(pairs: List[List[str]], headers=None, url: str = None, if_softmax: int = 0) -> List[float]:
    """
    本地重排序API - 兼容原rerank_api接口
    :param pairs: 查询-文档对列表
    :param headers: 兼容参数（忽略）
    :param url: 兼容参数（忽略）
    :param if_softmax: 是否使用softmax
    :return: 重排序分数列表
    """
    service = get_rerank_service()
    return service.rerank_pairs(pairs, if_softmax)


@retry_exponential_backoff()
def local_rerank(query: str, documents: List[str], if_softmax: int = 0) -> List[float]:
    """
    本地重排序 - 便捷接口
    :param query: 查询文本
    :param documents: 文档列表
    :param if_softmax: 是否使用softmax
    :return: 重排序分数列表
    """
    service = get_rerank_service()
    return service.rerank(query, documents, if_softmax)
