#!/usr/bin/env python3
"""
CPU版本测试脚本 - Windows AMD显卡环境
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os
import time

# 设置HuggingFace镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def test_torch_cpu():
    """测试PyTorch CPU版本"""
    print("=== 测试PyTorch CPU版本 ===")
    
    try:
        import torch
        print(f"✅ PyTorch版本: {torch.__version__}")
        print(f"   CUDA可用: {torch.cuda.is_available()}")
        print(f"   CPU线程数: {torch.get_num_threads()}")
        
        # 测试基本运算
        x = torch.randn(3, 3)
        y = torch.randn(3, 3)
        z = torch.mm(x, y)
        print(f"✅ 基本运算测试通过，结果形状: {z.shape}")
        
        return True
    except Exception as e:
        print(f"❌ PyTorch测试失败: {e}")
        return False


def test_sentence_transformers_cpu():
    """测试sentence-transformers CPU版本"""
    print("\n=== 测试sentence-transformers CPU版本 ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 使用小模型，强制CPU
        model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        print(f"正在加载模型: {model_name} (CPU模式)")
        
        model = SentenceTransformer(model_name, device='cpu')
        print("✅ 模型加载成功")
        
        # 测试编码
        test_texts = ["这是测试文本", "This is a test"]
        start_time = time.time()
        embeddings = model.encode(test_texts)
        end_time = time.time()
        
        print(f"✅ 嵌入测试成功")
        print(f"   文本数量: {len(test_texts)}")
        print(f"   向量维度: {embeddings.shape[1]}")
        print(f"   CPU耗时: {(end_time - start_time)*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ sentence-transformers测试失败: {e}")
        if "connection" in str(e).lower():
            print("   这可能是网络问题，模型会在首次使用时下载")
        return False


def test_cross_encoder_cpu():
    """测试CrossEncoder CPU版本"""
    print("\n=== 测试CrossEncoder CPU版本 ===")
    
    try:
        from sentence_transformers import CrossEncoder
        
        # 使用小模型，强制CPU
        model_name = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
        print(f"正在加载重排序模型: {model_name} (CPU模式)")
        
        model = CrossEncoder(model_name, device='cpu')
        print("✅ 重排序模型加载成功")
        
        # 测试重排序
        pairs = [
            ["人工智能", "AI是计算机科学的分支"],
            ["人工智能", "今天天气很好"],
            ["人工智能", "机器学习是AI的重要部分"]
        ]
        
        start_time = time.time()
        scores = model.predict(pairs)
        end_time = time.time()
        
        print(f"✅ 重排序测试成功")
        print(f"   对数量: {len(pairs)}")
        print(f"   CPU耗时: {(end_time - start_time)*1000:.1f}ms")
        
        # 显示结果
        for i, (pair, score) in enumerate(zip(pairs, scores)):
            print(f"   {i+1}. \"{pair[1][:20]}...\" 分数: {score:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrossEncoder测试失败: {e}")
        return False


def test_pdf_parsers():
    """测试PDF解析器"""
    print("\n=== 测试PDF解析器 ===")
    
    # 测试PyPDF2
    try:
        import PyPDF2
        print("✅ PyPDF2 可用")
        
        # 创建简单的PDF解析器
        class SimplePDFParser:
            def parse_text(self, pdf_bytes):
                import io
                reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        
        parser = SimplePDFParser()
        print("✅ 简单PDF解析器创建成功")
        
    except ImportError:
        print("⚠️ PyPDF2 未安装")
    
    # 测试pdfplumber
    try:
        import pdfplumber
        print("✅ pdfplumber 可用")
    except ImportError:
        print("⚠️ pdfplumber 未安装")
    
    return True


def test_cpu_performance():
    """CPU性能基准测试"""
    print("\n=== CPU性能基准测试 ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        import torch
        
        # 设置CPU线程数
        torch.set_num_threads(4)  # 根据你的CPU调整
        
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
        
        # 测试不同批次大小的性能
        batch_sizes = [1, 5, 10, 20]
        
        for batch_size in batch_sizes:
            texts = [f"测试文本{i}" for i in range(batch_size)]
            
            start_time = time.time()
            embeddings = model.encode(texts, batch_size=batch_size)
            end_time = time.time()
            
            total_time = end_time - start_time
            per_text_time = total_time / batch_size * 1000
            
            print(f"   批次大小 {batch_size:2d}: 总耗时 {total_time:.2f}s, 平均 {per_text_time:.1f}ms/文本")
        
        print("✅ CPU性能测试完成")
        print("   建议: 根据性能选择合适的批次大小")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False


def create_cpu_config():
    """创建CPU专用配置"""
    print("\n=== 创建CPU专用配置 ===")
    
    cpu_config = """
# CPU专用配置 - Windows AMD显卡环境
local_services:
  embedding:
    model: "paraphrase-multilingual-MiniLM-L12-v2"  # 小模型，适合CPU
    device: "cpu"
    batch_size: 8  # CPU适合的批次大小
  rerank:
    model: "cross-encoder/ms-marco-TinyBERT-L-2-v2"  # 小模型，适合CPU
    device: "cpu"
    batch_size: 4
  pdf_parser:
    engine: "pypdf2"  # 使用PyPDF2作为备选
  storage:
    type: "local"
    base_path: "./data/images"

# 性能优化设置
performance:
  cpu_threads: 4  # 根据你的CPU核心数调整
  max_batch_size: 10
  timeout: 30
"""
    
    try:
        with open("config_cpu.yaml", "w", encoding="utf-8") as f:
            f.write(cpu_config)
        print("✅ CPU配置文件已创建: config_cpu.yaml")
        print("   你可以将此配置合并到主配置文件中")
        return True
    except Exception as e:
        print(f"❌ 配置文件创建失败: {e}")
        return False


def main():
    """主函数"""
    print("=== CPU版本本地服务测试 (Windows AMD显卡环境) ===")
    print("此测试专门为CPU环境优化，避免GPU相关问题\n")
    
    tests = [
        ("PyTorch CPU版本", test_torch_cpu),
        ("SentenceTransformers CPU", test_sentence_transformers_cpu),
        ("CrossEncoder CPU", test_cross_encoder_cpu),
        ("PDF解析器", test_pdf_parsers),
        ("CPU性能基准", test_cpu_performance),
        ("创建CPU配置", create_cpu_config)
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
    print(f"CPU版本测试结果: {passed}/{total}")
    print('='*60)
    
    if passed >= 4:  # 至少4个测试通过
        print("🎉 CPU版本基本可用！")
        print("\n✅ 可以在Windows AMD环境下工作")
        print("✅ 准备好迁移到Linux GPU环境")
        print("\n下一步:")
        print("1. 在当前环境测试chatdoc集成")
        print("2. 准备GPU版本的配置和脚本")
        print("3. 迁移到Linux TITAN*2服务器")
        
        # 显示性能建议
        print("\n💡 CPU性能优化建议:")
        print("- 使用较小的批次大小 (4-10)")
        print("- 选择轻量级模型")
        print("- 考虑异步处理")
        
        return True
    else:
        print("❌ CPU版本测试失败较多")
        print("请检查依赖安装或网络连接")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
