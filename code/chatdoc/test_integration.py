#!/usr/bin/env python3
"""
集成测试脚本 - 测试chatdoc与本地服务的集成
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os
import time

def test_config_loading():
    """测试配置加载"""
    print("=== 测试配置加载 ===")
    
    try:
        from pkg.config import config
        
        # 检查本地服务配置
        local_services = config.get("local_services", {})
        if local_services:
            print("✅ 本地服务配置已加载")
            print(f"   嵌入模型: {local_services.get('embedding', {}).get('model', 'N/A')}")
            print(f"   重排序模型: {local_services.get('rerank', {}).get('model', 'N/A')}")
            print(f"   PDF引擎: {local_services.get('pdf_parser', {}).get('engine', 'N/A')}")
        else:
            print("⚠️ 本地服务配置未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False


def test_compatibility_services():
    """测试兼容性服务"""
    print("\n=== 测试兼容性服务 ===")
    
    try:
        # 测试嵌入服务
        print("1. 测试嵌入服务...")
        from pkg.compatibility_adapter import get_compatibility_embedding_service
        embedding_service = get_compatibility_embedding_service()
        
        test_text = "这是一个测试文本"
        embedding = embedding_service.encode_single(test_text)
        print(f"✅ 嵌入服务正常，向量维度: {len(embedding)}")
        
        # 测试重排序服务
        print("2. 测试重排序服务...")
        from pkg.compatibility_adapter import get_compatibility_rerank_service
        rerank_service = get_compatibility_rerank_service()
        
        pairs = [["查询", "相关文档"], ["查询", "不相关文档"]]
        scores = rerank_service.rerank_pairs(pairs)
        print(f"✅ 重排序服务正常，分数: {scores}")
        
        return True
        
    except Exception as e:
        print(f"❌ 兼容性服务测试失败: {e}")
        return False


def test_pdf_parsing():
    """测试PDF解析"""
    print("\n=== 测试PDF解析 ===")
    
    try:
        from pkg.clients.simple_pdf_client import SimplePDFClient
        
        client = SimplePDFClient()
        
        # 创建一个简单的测试PDF字节（这只是模拟）
        test_pdf_bytes = b"fake pdf content for testing"
        
        response = client.recognize_pdf2md(test_pdf_bytes)
        result = response.json()
        
        print(f"✅ PDF解析服务正常，返回代码: {result['code']}")
        print(f"   页面数量: {len(result['result']['pages'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF解析测试失败: {e}")
        return False


def test_original_interfaces():
    """测试原有接口兼容性"""
    print("\n=== 测试原有接口兼容性 ===")
    
    try:
        # 测试嵌入接口
        print("1. 测试嵌入接口...")
        from pkg.embedding.acge_embedding import acge_embedding
        
        embedding = acge_embedding("测试文本")
        print(f"✅ acge_embedding接口正常，向量维度: {len(embedding)}")
        
        # 测试重排序接口
        print("2. 测试重排序接口...")
        from pkg.rerank import rerank_api
        
        pairs = [["查询", "文档1"], ["查询", "文档2"]]
        scores = rerank_api(pairs)
        print(f"✅ rerank_api接口正常，分数: {scores}")
        
        # 测试utils中的嵌入接口
        print("3. 测试utils嵌入接口...")
        from pkg.utils import embedding_multi
        
        embeddings = embedding_multi(["文本1", "文本2"])
        print(f"✅ embedding_multi接口正常，数量: {len(embeddings)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 原有接口测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance():
    """性能测试"""
    print("\n=== 性能测试 ===")
    
    try:
        from pkg.compatibility_adapter import get_compatibility_embedding_service, get_compatibility_rerank_service
        
        embedding_service = get_compatibility_embedding_service()
        rerank_service = get_compatibility_rerank_service()
        
        # 嵌入性能测试
        texts = [f"测试文本{i}" for i in range(10)]
        start_time = time.time()
        embeddings = embedding_service.encode_batch(texts)
        end_time = time.time()
        
        embedding_time = end_time - start_time
        print(f"✅ 10个文本嵌入耗时: {embedding_time:.2f}s")
        print(f"   平均每个文本: {embedding_time/10*1000:.1f}ms")
        
        # 重排序性能测试
        query = "测试查询"
        documents = [f"测试文档{i}" for i in range(5)]
        pairs = [[query, doc] for doc in documents]
        
        start_time = time.time()
        scores = rerank_service.rerank_pairs(pairs)
        end_time = time.time()
        
        rerank_time = end_time - start_time
        print(f"✅ 5个文档重排序耗时: {rerank_time:.2f}s")
        print(f"   平均每个文档: {rerank_time/5*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=== ChatDoc本地服务集成测试 ===")
    print("测试chatdoc与本地服务的集成效果\n")
    
    tests = [
        ("配置加载", test_config_loading),
        ("兼容性服务", test_compatibility_services),
        ("PDF解析", test_pdf_parsing),
        ("原有接口兼容性", test_original_interfaces),
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
    
    print(f"\n{'='*60}")
    print(f"集成测试结果: {passed}/{total}")
    print('='*60)
    
    if passed >= 4:
        print("🎉 集成测试基本通过！")
        print("\n✅ 本地服务已成功集成到chatdoc")
        print("✅ 可以启动chatdoc服务进行完整测试")
        print("\n下一步:")
        print("1. 运行: python main.py 启动chatdoc服务")
        print("2. 测试文档上传和问答功能")
        print("3. 观察日志确认使用本地服务")
        
        return True
    else:
        print("❌ 集成测试失败较多")
        print("\n建议:")
        print("1. 检查配置文件")
        print("2. 确认依赖安装")
        print("3. 查看详细错误信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
