#!/usr/bin/env python3
"""
简单的本地服务测试脚本
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        return True
    except Exception as e:
        print(f"❌ MegaParse 测试失败: {e}")
        return False


def test_sentence_transformers():
    """测试sentence-transformers"""
    print("\n=== 测试sentence-transformers ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 使用一个小模型进行测试
        print("正在加载模型...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 测试编码
        test_text = "这是一个测试文本"
        embedding = model.encode(test_text)
        
        print(f"✅ 嵌入测试成功，向量维度: {len(embedding)}")
        return True
        
    except Exception as e:
        print(f"❌ sentence-transformers 测试失败: {e}")
        return False


def test_cross_encoder():
    """测试CrossEncoder"""
    print("\n=== 测试CrossEncoder ===")
    
    try:
        from sentence_transformers import CrossEncoder
        
        # 使用一个小模型进行测试
        print("正在加载重排序模型...")
        model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2')
        
        # 测试重排序
        pairs = [['查询', '相关文档'], ['查询', '不相关文档']]
        scores = model.predict(pairs)
        
        print(f"✅ 重排序测试成功，分数: {scores}")
        return True
        
    except Exception as e:
        print(f"❌ CrossEncoder 测试失败: {e}")
        return False


def test_local_services():
    """测试本地服务类"""
    print("\n=== 测试本地服务类 ===")
    
    # 先设置一个简单的配置
    import tempfile
    import yaml
    
    config_content = {
        'local_services': {
            'embedding': {
                'model': 'all-MiniLM-L6-v2',
                'device': 'cpu'
            },
            'rerank': {
                'model': 'cross-encoder/ms-marco-TinyBERT-L-2-v2',
                'device': 'cpu'
            }
        }
    }
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_content, f)
        temp_config_path = f.name
    
    try:
        # 设置配置路径环境变量
        os.environ['CONFIG_PATH'] = temp_config_path
        
        # 测试本地嵌入服务
        try:
            from pkg.embedding.local_embedding import LocalEmbeddingService
            embedding_service = LocalEmbeddingService(model_name='all-MiniLM-L6-v2', device='cpu')
            test_embedding = embedding_service.encode_single("测试文本")
            print(f"✅ 本地嵌入服务测试成功，向量维度: {len(test_embedding)}")
        except Exception as e:
            print(f"❌ 本地嵌入服务测试失败: {e}")
            return False
        
        # 测试本地重排序服务
        try:
            from pkg.rerank.local_rerank import LocalRerankService
            rerank_service = LocalRerankService(model_name='cross-encoder/ms-marco-TinyBERT-L-2-v2', device='cpu')
            test_scores = rerank_service.rerank("查询", ["文档1", "文档2"])
            print(f"✅ 本地重排序服务测试成功，分数: {test_scores}")
        except Exception as e:
            print(f"❌ 本地重排序服务测试失败: {e}")
            return False
        
        return True
        
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_config_path)
        except:
            pass


def main():
    """主函数"""
    print("=== 本地服务简单测试 ===")
    
    tests = [
        ("基本导入", test_imports),
        ("MegaParse", test_megaparse),
        ("SentenceTransformers", test_sentence_transformers),
        ("CrossEncoder", test_cross_encoder),
        ("本地服务类", test_local_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"开始测试: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed}/{total}")
    print('='*50)
    
    if passed == total:
        print("🎉 所有测试通过！本地服务可以正常使用")
        print("\n下一步:")
        print("1. 确保 config.yaml 中的 local_services 配置正确")
        print("2. 启动 chatdoc 服务测试完整功能")
        return True
    else:
        print("❌ 部分测试失败，请检查依赖安装")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
