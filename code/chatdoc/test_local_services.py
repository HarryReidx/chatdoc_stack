#!/usr/bin/env python3
"""
测试本地服务的脚本
Author: AI Assistant
Date: 2025-07-28
"""
import os
import sys
import time
import tempfile

# 简单的日志函数，避免循环依赖
def log_info(msg):
    print(f"[INFO] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}")

def log_warning(msg):
    print(f"[WARNING] {msg}")


def test_megaparse():
    """测试MegaParse PDF解析"""
    log_info("=== 测试MegaParse PDF解析 ===")

    try:
        from pkg.clients.megaparse_client import MegaParseClient

        # 创建测试PDF内容（简单的文本）
        test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000206 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n299\n%%EOF"

        client = MegaParseClient()

        start_time = time.time()
        response = client.recognize_pdf2md(test_content)
        end_time = time.time()

        log_info(f"MegaParse解析耗时: {(end_time - start_time)*1000:.1f}ms")
        log_info(f"响应状态码: {response.status_code}")

        result = response.json()
        log_info(f"解析结果代码: {result['code']}")
        log_info(f"页面数量: {len(result['result']['pages'])}")

        log_info("✅ MegaParse测试通过")
        return True

    except Exception as e:
        log_error(f"❌ MegaParse测试失败: {e}")
        return False


def test_embedding():
    """测试本地嵌入服务"""
    logger.info("=== 测试本地嵌入服务 ===")
    
    try:
        from pkg.embedding.local_embedding import get_embedding_service
        
        service = get_embedding_service()
        
        # 测试单文本嵌入
        test_text = "这是一个测试文本"
        start_time = time.time()
        embedding = service.encode_single(test_text)
        end_time = time.time()
        
        logger.info(f"单文本嵌入耗时: {(end_time - start_time)*1000:.1f}ms")
        logger.info(f"嵌入向量维度: {len(embedding)}")
        logger.info(f"向量前5个值: {embedding[:5]}")
        
        # 测试批量嵌入
        test_texts = ["文本1", "文本2", "文本3"]
        start_time = time.time()
        embeddings = service.encode_batch(test_texts)
        end_time = time.time()
        
        logger.info(f"批量嵌入耗时: {(end_time - start_time)*1000:.1f}ms")
        logger.info(f"批量嵌入数量: {len(embeddings)}")
        
        logger.info("✅ 嵌入服务测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 嵌入服务测试失败: {e}")
        return False


def test_rerank():
    """测试本地重排序服务"""
    logger.info("=== 测试本地重排序服务 ===")
    
    try:
        from pkg.rerank.local_rerank import get_rerank_service
        
        service = get_rerank_service()
        
        # 测试重排序
        query = "人工智能"
        documents = [
            "人工智能是计算机科学的一个分支",
            "今天天气很好",
            "机器学习是人工智能的重要组成部分",
            "我喜欢吃苹果"
        ]
        
        start_time = time.time()
        scores = service.rerank(query, documents)
        end_time = time.time()
        
        logger.info(f"重排序耗时: {(end_time - start_time)*1000:.1f}ms")
        logger.info(f"重排序分数: {scores}")
        
        # 按分数排序
        sorted_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        logger.info("排序后的文档:")
        for i, (doc, score) in enumerate(sorted_docs):
            logger.info(f"  {i+1}. {doc} (分数: {score:.4f})")
        
        logger.info("✅ 重排序服务测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 重排序服务测试失败: {e}")
        return False


def test_compatibility():
    """测试兼容性接口"""
    logger.info("=== 测试兼容性接口 ===")
    
    try:
        # 测试嵌入兼容接口
        from pkg.embedding.acge_embedding import acge_embedding, acge_embedding_multi
        
        embedding = acge_embedding("测试文本")
        logger.info(f"兼容嵌入接口测试通过，向量维度: {len(embedding)}")
        
        embeddings = acge_embedding_multi(["文本1", "文本2"])
        logger.info(f"兼容批量嵌入接口测试通过，数量: {len(embeddings)}")
        
        # 测试重排序兼容接口
        from pkg.rerank import rerank_api
        
        pairs = [["查询", "文档1"], ["查询", "文档2"]]
        scores = rerank_api(pairs)
        logger.info(f"兼容重排序接口测试通过，分数: {scores}")
        
        logger.info("✅ 兼容性接口测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 兼容性接口测试失败: {e}")
        return False


def test_performance():
    """性能测试"""
    logger.info("=== 性能测试 ===")
    
    try:
        from pkg.embedding.local_embedding import get_embedding_service
        from pkg.rerank.local_rerank import get_rerank_service
        
        embedding_service = get_embedding_service()
        rerank_service = get_rerank_service()
        
        # 嵌入性能测试
        test_texts = [f"测试文本{i}" for i in range(100)]
        start_time = time.time()
        embeddings = embedding_service.encode_batch(test_texts)
        end_time = time.time()
        
        embedding_time = end_time - start_time
        logger.info(f"100个文本嵌入耗时: {embedding_time:.2f}s")
        logger.info(f"平均每个文本: {embedding_time/100*1000:.1f}ms")
        
        # 重排序性能测试
        query = "测试查询"
        documents = [f"测试文档{i}" for i in range(50)]
        start_time = time.time()
        scores = rerank_service.rerank(query, documents)
        end_time = time.time()
        
        rerank_time = end_time - start_time
        logger.info(f"50个文档重排序耗时: {rerank_time:.2f}s")
        logger.info(f"平均每个文档: {rerank_time/50*1000:.1f}ms")
        
        logger.info("✅ 性能测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 性能测试失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("=== 本地服务测试程序 ===")
    
    tests = [
        ("MegaParse", test_megaparse),
        ("嵌入服务", test_embedding),
        ("重排序服务", test_rerank),
        ("兼容性接口", test_compatibility),
        ("性能测试", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n开始测试: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                logger.error(f"测试失败: {test_name}")
        except Exception as e:
            logger.error(f"测试异常: {test_name} - {e}")
    
    logger.info(f"\n=== 测试结果 ===")
    logger.info(f"通过: {passed}/{total}")
    
    if passed == total:
        logger.info("🎉 所有测试通过！本地服务可以正常使用")
        return True
    else:
        logger.error("❌ 部分测试失败，请检查配置和依赖")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
