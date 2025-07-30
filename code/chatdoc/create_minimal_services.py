#!/usr/bin/env python3
"""
创建最小化的本地服务 - 不依赖外部模型下载
Author: AI Assistant
Date: 2025-07-28
"""
import os
import numpy as np
from typing import List

def create_minimal_embedding_service():
    """创建最小化的嵌入服务"""
    
    class MinimalEmbeddingService:
        """最小化嵌入服务 - 使用简单的文本特征"""
        
        def __init__(self):
            print("初始化最小化嵌入服务（不需要下载模型）")
        
        def _text_to_features(self, text: str) -> List[float]:
            """将文本转换为简单的特征向量"""
            # 简单的文本特征提取
            features = []
            
            # 文本长度特征
            features.append(len(text) / 100.0)
            
            # 字符频率特征
            char_counts = {}
            for char in text:
                char_counts[char] = char_counts.get(char, 0) + 1
            
            # 常见字符的频率
            common_chars = '的是在了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'"
            
            for char in common_chars[:50]:  # 取前50个常见字符
                freq = char_counts.get(char, 0) / len(text) if len(text) > 0 else 0
                features.append(freq)
            
            # 补齐到固定维度
            while len(features) < 128:
                features.append(0.0)
            
            return features[:128]  # 返回128维向量
        
        def encode_single(self, text: str) -> List[float]:
            """单文本嵌入"""
            return self._text_to_features(text)
        
        def encode_batch(self, texts: List[str]) -> List[List[float]]:
            """批量文本嵌入"""
            return [self._text_to_features(text) for text in texts]
    
    return MinimalEmbeddingService()


def create_minimal_rerank_service():
    """创建最小化的重排序服务"""
    
    class MinimalRerankService:
        """最小化重排序服务 - 使用简单的文本相似度"""
        
        def __init__(self):
            print("初始化最小化重排序服务（不需要下载模型）")
        
        def _calculate_similarity(self, text1: str, text2: str) -> float:
            """计算两个文本的简单相似度"""
            # 转换为小写
            text1 = text1.lower()
            text2 = text2.lower()
            
            # 简单的词重叠相似度
            words1 = set(text1.split())
            words2 = set(text2.split())
            
            if len(words1) == 0 and len(words2) == 0:
                return 1.0
            
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            jaccard_sim = intersection / union if union > 0 else 0.0
            
            # 字符级别的相似度
            chars1 = set(text1)
            chars2 = set(text2)
            char_intersection = len(chars1.intersection(chars2))
            char_union = len(chars1.union(chars2))
            char_sim = char_intersection / char_union if char_union > 0 else 0.0
            
            # 组合相似度
            return 0.7 * jaccard_sim + 0.3 * char_sim
        
        def rerank(self, query: str, documents: List[str]) -> List[float]:
            """重排序文档"""
            scores = []
            for doc in documents:
                score = self._calculate_similarity(query, doc)
                scores.append(score)
            return scores
        
        def rerank_pairs(self, pairs: List[List[str]]) -> List[float]:
            """直接对查询-文档对进行重排序"""
            scores = []
            for pair in pairs:
                if len(pair) >= 2:
                    score = self._calculate_similarity(pair[0], pair[1])
                    scores.append(score)
                else:
                    scores.append(0.0)
            return scores
    
    return MinimalRerankService()


def create_minimal_pdf_parser():
    """创建最小化的PDF解析服务"""
    
    class MinimalPDFParser:
        """最小化PDF解析服务 - 使用PyPDF2"""
        
        def __init__(self):
            print("初始化最小化PDF解析服务")
            try:
                import PyPDF2
                self.has_pypdf2 = True
                print("✅ PyPDF2 可用")
            except ImportError:
                self.has_pypdf2 = False
                print("⚠️ PyPDF2 不可用，将使用文本模式")
        
        def recognize_pdf2md(self, pdf_bytes: bytes):
            """PDF转Markdown"""
            if self.has_pypdf2:
                return self._parse_with_pypdf2(pdf_bytes)
            else:
                return self._parse_as_text(pdf_bytes)
        
        def _parse_with_pypdf2(self, pdf_bytes: bytes):
            """使用PyPDF2解析"""
            import PyPDF2
            import io
            
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n\n# 第{page_num + 1}页\n\n{page_text}"
                
                # 构造兼容的响应格式
                result = {
                    "code": 200,
                    "message": "success",
                    "result": {
                        "pages": [{
                            "page_index": i,
                            "markdown": f"# 第{i+1}页\n\n{page.extract_text()}",
                            "elements": [],
                            "images": []
                        } for i, page in enumerate(pdf_reader.pages)],
                        "markdown": text,
                        "document_tree": {"title": "Document", "level": 0, "children": []},
                    },
                    "metrics": [{"page_index": i, "confidence": 0.8} for i in range(len(pdf_reader.pages))]
                }
                
                return MockResponse(result)
                
            except Exception as e:
                raise Exception(f"PDF解析失败: {str(e)}")
        
        def _parse_as_text(self, pdf_bytes: bytes):
            """作为文本处理（备选方案）"""
            # 如果无法解析PDF，返回一个默认结果
            result = {
                "code": 200,
                "message": "success",
                "result": {
                    "pages": [{
                        "page_index": 0,
                        "markdown": "# 文档内容\n\n无法解析PDF内容，请安装PyPDF2或使用其他PDF解析器。",
                        "elements": [],
                        "images": []
                    }],
                    "markdown": "# 文档内容\n\n无法解析PDF内容，请安装PyPDF2或使用其他PDF解析器。",
                    "document_tree": {"title": "Document", "level": 0, "children": []},
                },
                "metrics": [{"page_index": 0, "confidence": 0.5}]
            }
            
            return MockResponse(result)
    
    return MinimalPDFParser()


class MockResponse:
    """模拟响应对象"""
    def __init__(self, data):
        self.data = data
        self.status_code = 200
        import json
        self.content = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    def raise_for_status(self):
        pass
    
    def json(self):
        return self.data


def test_minimal_services():
    """测试最小化服务"""
    print("=== 测试最小化服务 ===")
    
    # 测试嵌入服务
    print("\n1. 测试嵌入服务")
    embedding_service = create_minimal_embedding_service()
    embedding = embedding_service.encode_single("这是一个测试文本")
    print(f"✅ 嵌入成功，维度: {len(embedding)}")
    
    embeddings = embedding_service.encode_batch(["文本1", "文本2"])
    print(f"✅ 批量嵌入成功，数量: {len(embeddings)}")
    
    # 测试重排序服务
    print("\n2. 测试重排序服务")
    rerank_service = create_minimal_rerank_service()
    scores = rerank_service.rerank("人工智能", ["AI技术", "天气预报", "机器学习"])
    print(f"✅ 重排序成功，分数: {scores}")
    
    # 测试PDF解析服务
    print("\n3. 测试PDF解析服务")
    pdf_parser = create_minimal_pdf_parser()
    
    # 创建一个简单的测试PDF字节
    test_pdf = b"fake pdf content"  # 这只是测试，实际使用需要真实PDF
    try:
        response = pdf_parser.recognize_pdf2md(test_pdf)
        result = response.json()
        print(f"✅ PDF解析服务初始化成功，代码: {result['code']}")
    except Exception as e:
        print(f"⚠️ PDF解析测试: {e}")
    
    print("\n✅ 所有最小化服务测试完成！")
    print("这些服务可以作为临时替代方案使用。")


if __name__ == "__main__":
    test_minimal_services()
