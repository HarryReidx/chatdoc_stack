#!/usr/bin/env python3
"""
独立的本地服务测试脚本 - 不依赖项目配置
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os
import time

def test_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    
    try:
        import megaparse
        print("✅ megaparse 导入成功")
    except ImportError as e:
        print(f"❌ megaparse 导入失败: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ sentence_transformers 导入成功")
    except ImportError as e:
        print(f"❌ sentence_transformers 导入失败: {e}")
        return False
    
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
    except ImportError as e:
        print(f"❌ transformers 导入失败: {e}")
        return False
    
    return True


def test_megaparse():
    """测试MegaParse"""
    print("\n=== 测试MegaParse ===")
    
    try:
        from megaparse import MegaParse
        megaparse = MegaParse()
        print("✅ MegaParse 初始化成功")
        
        # 创建一个简单的测试文件
        import tempfile
        test_content = "# 测试文档\n\n这是一个测试文档的内容。\n\n## 章节1\n\n这里是一些内容。"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # 测试加载文件
            result = megaparse.load(temp_file)
            print(f"✅ MegaParse 解析成功，结果长度: {len(result)}")
            return True
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ MegaParse 测试失败: {e}")
        return False


def test_embedding():
    """测试嵌入功能"""
    print("\n=== 测试嵌入功能 ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 使用一个小模型
        print("正在加载嵌入模型...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 测试单文本嵌入
        test_text = "这是一个测试文本"
        start_time = time.time()
        embedding = model.encode(test_text)
        end_time = time.time()
        
        print(f"✅ 单文本嵌入成功")
        print(f"   向量维度: {len(embedding)}")
        print(f"   耗时: {(end_time - start_time)*1000:.1f}ms")
        
        # 测试批量嵌入
        test_texts = ["文本1", "文本2", "文本3"]
        start_time = time.time()
        embeddings = model.encode(test_texts)
        end_time = time.time()
        
        print(f"✅ 批量嵌入成功")
        print(f"   文本数量: {len(embeddings)}")
        print(f"   耗时: {(end_time - start_time)*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ 嵌入功能测试失败: {e}")
        return False


def test_rerank():
    """测试重排序功能"""
    print("\n=== 测试重排序功能 ===")
    
    try:
        from sentence_transformers import CrossEncoder
        
        # 使用一个小模型
        print("正在加载重排序模型...")
        model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2')
        
        # 测试重排序
        query = "人工智能"
        documents = [
            "人工智能是计算机科学的一个分支",
            "今天天气很好",
            "机器学习是人工智能的重要组成部分"
        ]
        
        pairs = [[query, doc] for doc in documents]
        start_time = time.time()
        scores = model.predict(pairs)
        end_time = time.time()
        
        print(f"✅ 重排序成功")
        print(f"   文档数量: {len(documents)}")
        print(f"   耗时: {(end_time - start_time)*1000:.1f}ms")
        
        # 显示排序结果
        sorted_results = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        print("   排序结果:")
        for i, (doc, score) in enumerate(sorted_results):
            print(f"     {i+1}. {doc[:30]}... (分数: {score:.4f})")
        
        return True
        
    except Exception as e:
        print(f"❌ 重排序功能测试失败: {e}")
        return False


def test_performance():
    """性能测试"""
    print("\n=== 性能测试 ===")
    
    try:
        from sentence_transformers import SentenceTransformer, CrossEncoder
        
        # 嵌入性能测试
        print("测试嵌入性能...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        test_texts = [f"测试文本{i}" for i in range(50)]
        
        start_time = time.time()
        embeddings = embedding_model.encode(test_texts)
        end_time = time.time()
        
        embedding_time = end_time - start_time
        print(f"✅ 50个文本嵌入耗时: {embedding_time:.2f}s")
        print(f"   平均每个文本: {embedding_time/50*1000:.1f}ms")
        
        # 重排序性能测试
        print("测试重排序性能...")
        rerank_model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2')
        query = "测试查询"
        documents = [f"测试文档{i}" for i in range(20)]
        pairs = [[query, doc] for doc in documents]
        
        start_time = time.time()
        scores = rerank_model.predict(pairs)
        end_time = time.time()
        
        rerank_time = end_time - start_time
        print(f"✅ 20个文档重排序耗时: {rerank_time:.2f}s")
        print(f"   平均每个文档: {rerank_time/20*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=== 独立本地服务测试 ===")
    print("此测试不依赖项目配置，直接测试核心功能\n")
    
    tests = [
        ("基本导入", test_imports),
        ("MegaParse", test_megaparse),
        ("嵌入功能", test_embedding),
        ("重排序功能", test_rerank),
        ("性能测试", test_performance)
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
    
    if passed == total:
        print("🎉 所有核心功能测试通过！")
        print("\n✅ 本地服务的核心组件都可以正常工作")
        print("✅ 现在可以尝试集成到chatdoc系统中")
        print("\n下一步:")
        print("1. 确保所有opentelemetry依赖已安装")
        print("2. 启动chatdoc服务测试完整功能")
        return True
    else:
        print("❌ 部分核心功能测试失败")
        print("请检查依赖安装或网络连接")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
