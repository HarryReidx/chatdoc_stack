#!/usr/bin/env python3
"""
最小化测试脚本 - 只测试核心本地服务功能
Author: AI Assistant
Date: 2025-07-29
"""
import os
import sys

# 设置环境变量
os.environ['SKIP_ES_INIT'] = '1'

def test_core_services_only():
    """只测试核心服务，不导入完整的chatdoc"""
    print("=== 测试核心本地服务 ===")
    print("此测试只验证TEXTIN替代功能，不启动完整chatdoc\n")
    
    # 测试1: 配置加载
    print("1. 测试配置加载...")
    try:
        from pkg.config import config
        print("✅ 配置加载成功")
        
        local_services = config.get("local_services", {})
        if local_services:
            print("✅ 本地服务配置存在")
        else:
            print("⚠️ 本地服务配置不存在")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 测试2: 兼容性嵌入服务
    print("\n2. 测试兼容性嵌入服务...")
    try:
        from pkg.compatibility_adapter import get_compatibility_embedding_service
        embedding_service = get_compatibility_embedding_service()
        
        # 测试单文本嵌入
        embedding = embedding_service.encode_single("这是一个测试文本")
        print(f"✅ 单文本嵌入成功，维度: {len(embedding)}")
        
        # 测试批量嵌入
        embeddings = embedding_service.encode_batch(["文本1", "文本2", "文本3"])
        print(f"✅ 批量嵌入成功，数量: {len(embeddings)}")
        
    except Exception as e:
        print(f"❌ 嵌入服务测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 测试3: 兼容性重排序服务
    print("\n3. 测试兼容性重排序服务...")
    try:
        from pkg.compatibility_adapter import get_compatibility_rerank_service
        rerank_service = get_compatibility_rerank_service()
        
        # 测试重排序
        pairs = [
            ["人工智能", "AI是计算机科学的分支"],
            ["人工智能", "今天天气很好"],
            ["人工智能", "机器学习是AI的重要部分"]
        ]
        
        scores = rerank_service.rerank_pairs(pairs)
        print(f"✅ 重排序成功，分数: {scores}")
        
        # 显示排序结果
        sorted_pairs = sorted(zip(pairs, scores), key=lambda x: x[1], reverse=True)
        print("   排序结果:")
        for i, ((query, doc), score) in enumerate(sorted_pairs):
            print(f"     {i+1}. \"{doc[:30]}...\" 分数: {score:.4f}")
        
    except Exception as e:
        print(f"❌ 重排序服务测试失败: {e}")
        return False
    
    # 测试4: PDF解析服务
    print("\n4. 测试PDF解析服务...")
    try:
        from pkg.clients.simple_pdf_client import SimplePDFClient
        pdf_client = SimplePDFClient()
        
        # 创建模拟PDF数据
        fake_pdf_data = b"fake pdf content for testing"
        response = pdf_client.recognize_pdf2md(fake_pdf_data)
        result = response.json()
        
        print(f"✅ PDF解析成功，返回代码: {result['code']}")
        print(f"   页面数量: {len(result['result']['pages'])}")
        
    except Exception as e:
        print(f"❌ PDF解析测试失败: {e}")
        return False
    
    # 测试5: 原有接口兼容性（不导入完整模块）
    print("\n5. 测试接口兼容性...")
    try:
        # 直接测试兼容性适配器
        embedding_service = get_compatibility_embedding_service()
        rerank_service = get_compatibility_rerank_service()
        
        # 模拟原有接口调用
        test_embedding = embedding_service.encode_single("测试文本", dimension=1024, digit=8)
        print(f"✅ 嵌入接口兼容，维度: {len(test_embedding)}")
        
        test_scores = rerank_service.rerank_pairs([["查询", "文档1"], ["查询", "文档2"]], if_softmax=0)
        print(f"✅ 重排序接口兼容，分数: {test_scores}")
        
    except Exception as e:
        print(f"❌ 接口兼容性测试失败: {e}")
        return False
    
    # 测试6: 性能测试
    print("\n6. 性能测试...")
    try:
        import time
        
        # 嵌入性能
        texts = [f"测试文本{i}" for i in range(10)]
        start_time = time.time()
        embeddings = embedding_service.encode_batch(texts)
        end_time = time.time()
        
        embedding_time = end_time - start_time
        print(f"✅ 10个文本嵌入耗时: {embedding_time:.2f}s")
        print(f"   平均每个文本: {embedding_time/10*1000:.1f}ms")
        
        # 重排序性能
        query = "测试查询"
        documents = [f"测试文档{i}" for i in range(5)]
        pairs = [[query, doc] for doc in documents]
        
        start_time = time.time()
        scores = rerank_service.rerank_pairs(pairs)
        end_time = time.time()
        
        rerank_time = end_time - start_time
        print(f"✅ 5个文档重排序耗时: {rerank_time:.2f}s")
        print(f"   平均每个文档: {rerank_time/5*1000:.1f}ms")
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("=== ChatDoc核心服务测试 ===")
    print("此测试验证TEXTIN替代功能是否正常工作")
    print("不会启动完整的chatdoc系统\n")
    
    if test_core_services_only():
        print("\n🎉 核心服务测试全部通过！")
        print("\n✅ TEXTIN替代功能正常工作")
        print("✅ 嵌入服务：使用兼容性实现")
        print("✅ 重排序服务：使用简单相似度算法")
        print("✅ PDF解析：使用PyPDF2")
        print("✅ 完全离线运行")
        
        print("\n📊 性能特点:")
        print("- 嵌入速度：适中（CPU环境）")
        print("- 重排序速度：快速（简单算法）")
        print("- PDF解析：基本文本提取")
        print("- 内存使用：较低")
        
        print("\n🚀 下一步:")
        print("1. 核心功能已验证可用")
        print("2. 可以尝试集成到完整系统")
        print("3. 如需完整功能，请解决依赖问题")
        print("4. 后续可迁移到GPU环境获得更好性能")
        
        return True
    else:
        print("\n❌ 核心服务测试失败")
        print("\n建议:")
        print("1. 运行 python install_all_deps.py 安装依赖")
        print("2. 检查网络连接（首次运行需要下载模型）")
        print("3. 查看详细错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
