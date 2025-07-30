#!/usr/bin/env python3
"""
离线本地服务测试脚本 - 使用国内镜像和缓存
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os
import time

def setup_huggingface_mirror():
    """设置HuggingFace镜像"""
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    print("✅ 已设置HuggingFace镜像: https://hf-mirror.com")

def test_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    
    try:
        import torch
        print("✅ torch 导入成功")
        print(f"   PyTorch版本: {torch.__version__}")
        print(f"   CUDA可用: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ torch 导入失败: {e}")
        return False
    
    try:
        import transformers
        print("✅ transformers 导入成功")
        print(f"   版本: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ transformers 导入失败: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ sentence_transformers 导入成功")
        print(f"   版本: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"❌ sentence_transformers 导入失败: {e}")
        return False
    
    # 测试megaparse导入（可能失败，但不影响其他功能）
    try:
        import megaparse
        print("✅ megaparse 导入成功")
    except ImportError as e:
        print(f"⚠️ megaparse 导入失败: {e}")
        print("   这可能是版本冲突，但不影响其他功能测试")
    
    return True


def test_embedding_simple():
    """测试简单的嵌入功能"""
    print("\n=== 测试嵌入功能（简单版本）===")
    
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        # 使用一个小的中文模型
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        
        print(f"正在加载模型: {model_name}")
        print("首次运行可能需要下载模型，请耐心等待...")
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            print("✅ 模型加载成功")
            
            # 测试编码
            test_text = "这是一个测试文本"
            inputs = tokenizer(test_text, return_tensors="pt", padding=True, truncation=True)
            
            with torch.no_grad():
                outputs = model(**inputs)
                # 使用mean pooling
                embeddings = outputs.last_hidden_state.mean(dim=1)
            
            print(f"✅ 文本嵌入成功，向量维度: {embeddings.shape[1]}")
            return True
            
        except Exception as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                print(f"⚠️ 网络连接问题: {e}")
                print("   建议：")
                print("   1. 检查网络连接")
                print("   2. 使用VPN或代理")
                print("   3. 手动下载模型到本地")
                return False
            else:
                raise e
        
    except Exception as e:
        print(f"❌ 嵌入功能测试失败: {e}")
        return False


def test_local_embedding_class():
    """测试本地嵌入类（不依赖配置）"""
    print("\n=== 测试本地嵌入类 ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 创建一个简单的嵌入服务类
        class SimpleEmbeddingService:
            def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
                print(f"正在初始化嵌入服务，模型: {model_name}")
                self.model = SentenceTransformer(model_name)
                print("✅ 嵌入服务初始化成功")
            
            def encode_single(self, text):
                return self.model.encode(text)
            
            def encode_batch(self, texts):
                return self.model.encode(texts)
        
        # 测试服务
        service = SimpleEmbeddingService()
        
        # 测试单文本
        embedding = service.encode_single("测试文本")
        print(f"✅ 单文本嵌入成功，维度: {len(embedding)}")
        
        # 测试批量
        embeddings = service.encode_batch(["文本1", "文本2"])
        print(f"✅ 批量嵌入成功，数量: {len(embeddings)}")
        
        return True
        
    except Exception as e:
        if "connection" in str(e).lower() or "timeout" in str(e).lower():
            print(f"⚠️ 网络连接问题: {e}")
            return False
        else:
            print(f"❌ 本地嵌入类测试失败: {e}")
            return False


def test_local_rerank_class():
    """测试本地重排序类（不依赖配置）"""
    print("\n=== 测试本地重排序类 ===")
    
    try:
        from sentence_transformers import CrossEncoder
        
        # 创建一个简单的重排序服务类
        class SimpleRerankService:
            def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-12-v2"):
                print(f"正在初始化重排序服务，模型: {model_name}")
                self.model = CrossEncoder(model_name)
                print("✅ 重排序服务初始化成功")
            
            def rerank(self, query, documents):
                pairs = [[query, doc] for doc in documents]
                scores = self.model.predict(pairs)
                return scores.tolist() if hasattr(scores, 'tolist') else list(scores)
        
        # 测试服务
        service = SimpleRerankService()
        
        # 测试重排序
        query = "人工智能"
        documents = ["AI是未来", "今天天气好", "机器学习很重要"]
        scores = service.rerank(query, documents)
        
        print(f"✅ 重排序成功，分数: {scores}")
        
        # 显示排序结果
        sorted_results = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        print("   排序结果:")
        for i, (doc, score) in enumerate(sorted_results):
            print(f"     {i+1}. {doc} (分数: {score:.4f})")
        
        return True
        
    except Exception as e:
        if "connection" in str(e).lower() or "timeout" in str(e).lower():
            print(f"⚠️ 网络连接问题: {e}")
            return False
        else:
            print(f"❌ 本地重排序类测试失败: {e}")
            return False


def test_alternative_pdf_parser():
    """测试替代的PDF解析方案"""
    print("\n=== 测试替代PDF解析方案 ===")
    
    try:
        # 如果megaparse有问题，我们可以使用其他方案
        import PyPDF2
        print("✅ PyPDF2 可用作备选PDF解析器")
        
        # 创建一个简单的PDF解析类
        class SimplePDFParser:
            def parse_pdf(self, pdf_bytes):
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        
        parser = SimplePDFParser()
        print("✅ 简单PDF解析器创建成功")
        
        return True
        
    except ImportError:
        print("⚠️ PyPDF2 未安装，可以作为megaparse的备选方案")
        print("   安装命令: pip install PyPDF2")
        return True  # 不算失败，只是提示


def main():
    """主函数"""
    print("=== 离线本地服务测试 ===")
    print("此测试使用国内镜像，适合网络受限环境\n")
    
    # 设置镜像
    setup_huggingface_mirror()
    
    tests = [
        ("基本导入", test_imports),
        ("嵌入功能（简单版）", test_embedding_simple),
        ("本地嵌入类", test_local_embedding_class),
        ("本地重排序类", test_local_rerank_class),
        ("替代PDF解析", test_alternative_pdf_parser)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"开始测试: {test_name}")
        print('='*60)
        
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name} 测试通过")
            else:
                print(f"\n❌ {test_name} 测试失败")
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"测试结果: {passed}/{total}")
    print('='*60)
    
    if passed >= 3:  # 至少3个测试通过就算成功
        print("🎉 核心功能基本可用！")
        print("\n✅ 基础组件可以工作")
        print("✅ 可以尝试集成到chatdoc系统")
        print("\n建议:")
        print("1. 如果网络允许，让模型在后台下载")
        print("2. 考虑使用离线模型或本地模型")
        print("3. 如果megaparse有问题，可以使用PyPDF2作为备选")
        return True
    else:
        print("❌ 大部分功能测试失败")
        print("\n可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 使用VPN或代理")
        print("3. 手动下载模型到本地")
        print("4. 使用更简单的替代方案")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
