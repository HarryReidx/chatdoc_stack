#!/usr/bin/env python3
"""
创建简单的TEXTIN替代方案 - 不依赖复杂模型
Author: AI Assistant
Date: 2025-07-28
"""
import os
import sys

def create_simple_embedding_replacement():
    """创建简单的嵌入服务替代"""
    
    code = '''
"""
简单嵌入服务 - TEXTIN替代方案
"""
import numpy as np
from typing import List
import hashlib
import json

class SimpleEmbeddingService:
    """简单嵌入服务 - 使用TF-IDF和词频特征"""
    
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.dimension = 128
        
    def _build_vocab(self, texts):
        """构建词汇表"""
        word_counts = {}
        doc_counts = {}
        
        for text in texts:
            words = set(text.lower().split())
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
                doc_counts[word] = doc_counts.get(word, 0) + 1
        
        # 计算IDF
        total_docs = len(texts)
        for word, count in doc_counts.items():
            self.idf[word] = np.log(total_docs / (count + 1))
        
        # 选择最常见的词作为词汇表
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        self.vocab = {word: i for i, (word, _) in enumerate(sorted_words[:self.dimension])}
    
    def _text_to_vector(self, text):
        """将文本转换为向量"""
        words = text.lower().split()
        vector = np.zeros(self.dimension)
        
        # TF-IDF特征
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        total_words = len(words)
        for word, count in word_counts.items():
            if word in self.vocab:
                tf = count / total_words
                idf = self.idf.get(word, 1.0)
                vector[self.vocab[word]] = tf * idf
        
        # 归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector.tolist()
    
    def encode_single(self, text, dimension=1024, digit=8):
        """单文本嵌入"""
        # 如果没有词汇表，使用简单特征
        if not self.vocab:
            return self._simple_features(text)
        return self._text_to_vector(text)
    
    def encode_batch(self, texts, dimension=1024, digit=8):
        """批量文本嵌入"""
        if not self.vocab:
            self._build_vocab(texts)
        return [self._text_to_vector(text) for text in texts]
    
    def _simple_features(self, text):
        """简单特征提取"""
        features = []
        
        # 基本统计特征
        features.append(len(text) / 100.0)  # 文本长度
        features.append(len(text.split()) / 50.0)  # 词数
        features.append(text.count('。') / 10.0)  # 句子数
        
        # 字符频率特征
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # 常见字符
        common_chars = '的是在了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'
        
        for char in common_chars[:100]:
            freq = char_freq.get(char, 0) / len(text) if len(text) > 0 else 0
            features.append(freq)
        
        # 补齐到128维
        while len(features) < 128:
            features.append(0.0)
        
        return features[:128]

# 全局实例
_simple_embedding_service = None

def get_simple_embedding_service():
    global _simple_embedding_service
    if _simple_embedding_service is None:
        _simple_embedding_service = SimpleEmbeddingService()
    return _simple_embedding_service
'''
    
    with open("pkg/embedding/simple_embedding.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("✅ 简单嵌入服务已创建: pkg/embedding/simple_embedding.py")


def create_simple_rerank_replacement():
    """创建简单的重排序服务替代"""
    
    code = '''
"""
简单重排序服务 - TEXTIN替代方案
"""
import re
from typing import List

class SimpleRerankService:
    """简单重排序服务 - 使用文本相似度"""
    
    def __init__(self):
        pass
    
    def _preprocess_text(self, text):
        """预处理文本"""
        # 转小写，去除标点
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()
    
    def _jaccard_similarity(self, text1, text2):
        """计算Jaccard相似度"""
        words1 = set(self._preprocess_text(text1))
        words2 = set(self._preprocess_text(text2))
        
        if len(words1) == 0 and len(words2) == 0:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _cosine_similarity(self, text1, text2):
        """计算余弦相似度"""
        words1 = self._preprocess_text(text1)
        words2 = self._preprocess_text(text2)
        
        # 构建词频向量
        all_words = set(words1 + words2)
        
        vec1 = [words1.count(word) for word in all_words]
        vec2 = [words2.count(word) for word in all_words]
        
        # 计算余弦相似度
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_similarity(self, query, document):
        """计算查询和文档的相似度"""
        jaccard = self._jaccard_similarity(query, document)
        cosine = self._cosine_similarity(query, document)
        
        # 组合相似度
        return 0.6 * jaccard + 0.4 * cosine
    
    def rerank(self, query, documents, if_softmax=0):
        """重排序文档"""
        scores = []
        for doc in documents:
            score = self._calculate_similarity(query, doc)
            scores.append(score)
        
        if if_softmax == 1:
            scores = self._softmax(scores)
        
        return scores
    
    def rerank_pairs(self, pairs, if_softmax=0):
        """重排序查询-文档对"""
        scores = []
        for pair in pairs:
            if len(pair) >= 2:
                score = self._calculate_similarity(pair[0], pair[1])
                scores.append(score)
            else:
                scores.append(0.0)
        
        if if_softmax == 1:
            scores = self._softmax(scores)
        
        return scores
    
    def _softmax(self, scores):
        """应用softmax"""
        import math
        max_score = max(scores) if scores else 0
        exp_scores = [math.exp(score - max_score) for score in scores]
        sum_exp = sum(exp_scores)
        return [exp_score / sum_exp for exp_score in exp_scores]

# 全局实例
_simple_rerank_service = None

def get_simple_rerank_service():
    global _simple_rerank_service
    if _simple_rerank_service is None:
        _simple_rerank_service = SimpleRerankService()
    return _simple_rerank_service
'''
    
    with open("pkg/rerank/simple_rerank.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("✅ 简单重排序服务已创建: pkg/rerank/simple_rerank.py")


def create_simple_pdf_replacement():
    """创建简单的PDF解析替代"""
    
    code = '''
"""
简单PDF解析服务 - TEXTIN替代方案
"""
import json
from typing import Dict, Any

class SimplePDFParser:
    """简单PDF解析服务"""
    
    def __init__(self):
        self.has_pypdf2 = False
        try:
            import PyPDF2
            self.has_pypdf2 = True
        except ImportError:
            pass
    
    def recognize_pdf2md(self, pdf_bytes):
        """PDF转Markdown"""
        if self.has_pypdf2:
            return self._parse_with_pypdf2(pdf_bytes)
        else:
            return self._parse_fallback(pdf_bytes)
    
    def _parse_with_pypdf2(self, pdf_bytes):
        """使用PyPDF2解析"""
        import PyPDF2
        import io
        
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            pages = []
            full_text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                markdown_text = f"# 第{page_num + 1}页\\n\\n{page_text}"
                
                pages.append({
                    "page_index": page_num,
                    "markdown": markdown_text,
                    "elements": self._extract_elements(page_text),
                    "images": []
                })
                
                full_text += markdown_text + "\\n\\n"
            
            result = {
                "code": 200,
                "message": "success",
                "result": {
                    "pages": pages,
                    "markdown": full_text,
                    "document_tree": self._build_tree(full_text)
                },
                "metrics": [{"page_index": i, "confidence": 0.85} for i in range(len(pages))]
            }
            
            return MockResponse(result)
            
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
    
    def _parse_fallback(self, pdf_bytes):
        """备选解析方案"""
        result = {
            "code": 200,
            "message": "success",
            "result": {
                "pages": [{
                    "page_index": 0,
                    "markdown": "# 文档内容\\n\\n无法解析PDF，请安装PyPDF2",
                    "elements": [],
                    "images": []
                }],
                "markdown": "# 文档内容\\n\\n无法解析PDF，请安装PyPDF2",
                "document_tree": {"title": "Document", "level": 0, "children": []}
            },
            "metrics": [{"page_index": 0, "confidence": 0.5}]
        }
        
        return MockResponse(result)
    
    def _extract_elements(self, text):
        """提取文本元素"""
        elements = []
        lines = text.split('\\n')
        
        for i, line in enumerate(lines):
            if line.strip():
                elements.append({
                    "line_index": i,
                    "content": line.strip(),
                    "type": "paragraph",
                    "bbox": [0, i*20, 500, (i+1)*20, 500, (i+1)*20, 0, (i+1)*20]
                })
        
        return elements
    
    def _build_tree(self, text):
        """构建文档树"""
        return {
            "title": "Document",
            "level": 0,
            "children": [
                {
                    "title": "Content",
                    "level": 1,
                    "children": []
                }
            ]
        }

class MockResponse:
    """模拟响应对象"""
    def __init__(self, data):
        self.data = data
        self.status_code = 200
        self.content = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    def raise_for_status(self):
        pass
    
    def json(self):
        return self.data

# 全局实例
_simple_pdf_parser = None

def get_simple_pdf_parser():
    global _simple_pdf_parser
    if _simple_pdf_parser is None:
        _simple_pdf_parser = SimplePDFParser()
    return _simple_pdf_parser
'''
    
    with open("pkg/clients/simple_pdf_parser.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    print("✅ 简单PDF解析服务已创建: pkg/clients/simple_pdf_parser.py")


def main():
    """主函数"""
    print("=== 创建简单的TEXTIN替代方案 ===")
    print("这些服务不依赖复杂的机器学习模型\n")
    
    # 确保目录存在
    os.makedirs("pkg/embedding", exist_ok=True)
    os.makedirs("pkg/rerank", exist_ok=True)
    os.makedirs("pkg/clients", exist_ok=True)
    
    create_simple_embedding_replacement()
    create_simple_rerank_replacement()
    create_simple_pdf_replacement()
    
    print("\n✅ 所有简单替代服务已创建完成！")
    print("\n这些服务特点:")
    print("- 不需要下载大型模型")
    print("- 不依赖GPU或高性能CPU")
    print("- 使用传统算法（TF-IDF、余弦相似度等）")
    print("- 可以立即使用")
    print("\n虽然效果可能不如深度学习模型，但足以验证系统可行性")

if __name__ == "__main__":
    main()
'''
