"""
兼容性适配器 - 处理版本兼容性问题
Author: AI Assistant
Date: 2025-07-28
"""
import os
import sys
from typing import List, Union
from pkg.config import config
from pkg.utils.logger import logger


class CompatibilityEmbeddingService:
    """兼容性嵌入服务"""
    
    def __init__(self):
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """初始化服务"""
        try:
            # 尝试使用sentence-transformers
            from sentence_transformers import SentenceTransformer
            model_name = config.get("local_services", {}).get("embedding", {}).get("model", "paraphrase-multilingual-MiniLM-L12-v2")
            self.service = SentenceTransformer(model_name, device='cpu')
            self.service_type = "sentence_transformers"
            logger.info("使用sentence-transformers嵌入服务")
            
        except Exception as e:
            logger.warning(f"sentence-transformers初始化失败: {e}")
            try:
                # 尝试使用transformers手动实现
                from transformers import AutoTokenizer, AutoModel
                import torch
                
                model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                self.service_type = "manual_transformers"
                logger.info("使用transformers手动实现嵌入服务")
                
            except Exception as e2:
                logger.warning(f"transformers初始化失败: {e2}")
                # 使用简单实现
                self.service_type = "simple"
                logger.info("使用简单实现嵌入服务")
    
    def encode_single(self, text: str, dimension: int = 1024, digit: int = 8) -> List[float]:
        """单文本嵌入"""
        try:
            if self.service_type == "sentence_transformers":
                return self.service.encode(text).tolist()
            
            elif self.service_type == "manual_transformers":
                return self._manual_encode(text)
            
            else:
                return self._simple_encode(text)
                
        except Exception as e:
            logger.error(f"嵌入失败，使用简单实现: {e}")
            return self._simple_encode(text)
    
    def encode_batch(self, texts: List[str], dimension: int = 1024, digit: int = 8) -> List[List[float]]:
        """批量文本嵌入"""
        try:
            if self.service_type == "sentence_transformers":
                embeddings = self.service.encode(texts)
                return [emb.tolist() for emb in embeddings]
            
            elif self.service_type == "manual_transformers":
                return [self._manual_encode(text) for text in texts]
            
            else:
                return [self._simple_encode(text) for text in texts]
                
        except Exception as e:
            logger.error(f"批量嵌入失败，使用简单实现: {e}")
            return [self._simple_encode(text) for text in texts]
    
    def _manual_encode(self, text: str) -> List[float]:
        """手动实现嵌入"""
        import torch
        
        encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Mean pooling
            token_embeddings = model_output[0]
            attention_mask = encoded_input['attention_mask']
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            sentence_embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return sentence_embedding[0].numpy().tolist()
    
    def _simple_encode(self, text: str) -> List[float]:
        """简单实现嵌入"""
        # 基于字符频率的简单特征
        features = []
        
        # 文本统计特征
        features.append(len(text) / 100.0)
        features.append(len(text.split()) / 50.0)
        features.append(text.count('。') / 10.0)
        
        # 字符频率
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # 常见字符特征
        common_chars = '的是在了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'
        
        for char in common_chars[:125]:
            freq = char_freq.get(char, 0) / len(text) if len(text) > 0 else 0
            features.append(freq)
        
        # 补齐到128维
        while len(features) < 128:
            features.append(0.0)
        
        return features[:128]


class CompatibilityRerankService:
    """兼容性重排序服务"""
    
    def __init__(self):
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """初始化服务"""
        try:
            # 尝试使用CrossEncoder
            from sentence_transformers import CrossEncoder
            model_name = config.get("local_services", {}).get("rerank", {}).get("model", "cross-encoder/ms-marco-TinyBERT-L-2-v2")
            if model_name != "simple":
                self.service = CrossEncoder(model_name, device='cpu')
                self.service_type = "cross_encoder"
                logger.info("使用CrossEncoder重排序服务")
            else:
                self.service_type = "simple"
                logger.info("使用简单重排序服务")
                
        except Exception as e:
            logger.warning(f"CrossEncoder初始化失败: {e}")
            self.service_type = "simple"
            logger.info("使用简单重排序服务")
    
    def rerank_pairs(self, pairs: List[List[str]], if_softmax: int = 0) -> List[float]:
        """重排序查询-文档对"""
        try:
            if self.service_type == "cross_encoder":
                scores = self.service.predict(pairs)
                scores = scores.tolist() if hasattr(scores, 'tolist') else list(scores)
            else:
                scores = [self._simple_similarity(pair[0], pair[1]) for pair in pairs]
            
            if if_softmax == 1:
                scores = self._softmax(scores)
            
            return scores
            
        except Exception as e:
            logger.error(f"重排序失败，使用简单实现: {e}")
            scores = [self._simple_similarity(pair[0], pair[1]) for pair in pairs]
            if if_softmax == 1:
                scores = self._softmax(scores)
            return scores
    
    def _simple_similarity(self, text1: str, text2: str) -> float:
        """简单相似度计算"""
        # 预处理文本
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()

        if not text1 or not text2:
            return 0.0

        # 词级别相似度
        words1 = set(text1.split())
        words2 = set(text2.split())

        if len(words1) == 0 and len(words2) == 0:
            return 1.0

        word_intersection = len(words1.intersection(words2))
        word_union = len(words1.union(words2))
        word_similarity = word_intersection / word_union if word_union > 0 else 0.0

        # 字符级别相似度
        chars1 = set(text1.replace(' ', ''))
        chars2 = set(text2.replace(' ', ''))

        char_intersection = len(chars1.intersection(chars2))
        char_union = len(chars1.union(chars2))
        char_similarity = char_intersection / char_union if char_union > 0 else 0.0

        # 包含关系加分
        containment_bonus = 0.0
        if text1 in text2 or text2 in text1:
            containment_bonus = 0.3

        # 组合相似度
        final_similarity = 0.5 * word_similarity + 0.3 * char_similarity + containment_bonus

        return min(final_similarity, 1.0)  # 确保不超过1.0
    
    def _softmax(self, scores: List[float]) -> List[float]:
        """应用softmax"""
        import math
        max_score = max(scores) if scores else 0
        exp_scores = [math.exp(score - max_score) for score in scores]
        sum_exp = sum(exp_scores)
        return [exp_score / sum_exp for exp_score in exp_scores]


# 全局实例
_compatibility_embedding_service = None
_compatibility_rerank_service = None

def get_compatibility_embedding_service():
    """获取兼容性嵌入服务"""
    global _compatibility_embedding_service
    if _compatibility_embedding_service is None:
        _compatibility_embedding_service = CompatibilityEmbeddingService()
    return _compatibility_embedding_service

def get_compatibility_rerank_service():
    """获取兼容性重排序服务"""
    global _compatibility_rerank_service
    if _compatibility_rerank_service is None:
        _compatibility_rerank_service = CompatibilityRerankService()
    return _compatibility_rerank_service
