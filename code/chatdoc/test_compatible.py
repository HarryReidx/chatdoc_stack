#!/usr/bin/env python3
"""
兼容性测试脚本 - 处理版本问题
Author: AI Assistant
Date: 2025-07-28
"""
import sys
import os
import time

# 设置HuggingFace镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def test_torch_version():
    """测试PyTorch版本兼容性"""
    print("=== 测试PyTorch版本兼容性 ===")
    
    try:
        import torch
        print(f"✅ PyTorch版本: {torch.__version__}")
        print(f"   CUDA可用: {torch.cuda.is_available()}")
        print(f"   CPU线程数: {torch.get_num_threads()}")
        
        # 检查版本
        version = torch.__version__
        major, minor = map(int, version.split('.')[:2])
        
        if major >= 2 and minor >= 1:
            print("✅ PyTorch版本满足要求 (>=2.1)")
            return True
        else:
            print(f"⚠️ PyTorch版本过低 ({version})，需要 >=2.1")
            print("   请运行: python fix_pytorch_version.py")
            return False
            
    except Exception as e:
        print(f"❌ PyTorch测试失败: {e}")
        return False


def test_transformers_basic():
    """测试transformers基本功能"""
    print("\n=== 测试transformers基本功能 ===")
    
    try:
        import transformers
        print(f"✅ transformers版本: {transformers.__version__}")
        
        # 测试基本导入
        from transformers import AutoTokenizer
        print("✅ AutoTokenizer 导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ transformers测试失败: {e}")
        return False


def test_sentence_transformers_compatible():
    """测试sentence-transformers兼容性"""
    print("\n=== 测试sentence-transformers兼容性 ===")
    
    try:
        # 检查PyTorch版本
        import torch
        version = torch.__version__
        major, minor = map(int, version.split('.')[:2])
        
        if major < 2 or (major == 2 and minor < 1):
            print(f"⚠️ PyTorch版本 {version} 可能不兼容")
            print("   尝试使用兼容模式...")
            
            # 尝试使用transformers直接实现
            return test_manual_embedding()
        
        # 正常测试sentence-transformers
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers 导入成功")
        
        # 使用小模型测试
        model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        print(f"正在加载模型: {model_name}")
        
        model = SentenceTransformer(model_name, device='cpu')
        print("✅ 模型加载成功")
        
        # 测试编码
        text = "测试文本"
        embedding = model.encode(text)
        print(f"✅ 编码成功，维度: {len(embedding)}")
        
        return True
        
    except Exception as e:
        print(f"❌ sentence-transformers测试失败: {e}")
        print("   尝试手动实现...")
        return test_manual_embedding()


def test_manual_embedding():
    """手动实现嵌入功能（兼容性备选方案）"""
    print("\n=== 测试手动嵌入实现 ===")
    
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        print(f"正在加载模型: {model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        print("✅ 模型加载成功")
        
        # 手动实现mean pooling
        def mean_pooling(model_output, attention_mask):
            token_embeddings = model_output[0]
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        # 测试编码
        text = "这是一个测试文本"
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        
        with torch.no_grad():
            model_output = model(**encoded_input)
            sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        
        print(f"✅ 手动嵌入成功，维度: {sentence_embeddings.shape[1]}")
        return True
        
    except Exception as e:
        print(f"❌ 手动嵌入测试失败: {e}")
        return False


def test_simple_services():
    """测试简化的服务实现"""
    print("\n=== 测试简化服务实现 ===")
    
    try:
        # 创建简化的嵌入服务
        class SimpleEmbeddingService:
            def __init__(self):
                from transformers import AutoTokenizer, AutoModel
                import torch
                
                model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                self.device = 'cpu'
                
            def encode_single(self, text):
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
            
            def encode_batch(self, texts):
                return [self.encode_single(text) for text in texts]
        
        print("正在初始化简化嵌入服务...")
        service = SimpleEmbeddingService()
        print("✅ 简化嵌入服务初始化成功")
        
        # 测试
        embedding = service.encode_single("测试文本")
        print(f"✅ 单文本嵌入成功，维度: {len(embedding)}")
        
        embeddings = service.encode_batch(["文本1", "文本2"])
        print(f"✅ 批量嵌入成功，数量: {len(embeddings)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 简化服务测试失败: {e}")
        return False


def create_fallback_config():
    """创建备选配置"""
    print("\n=== 创建备选配置 ===")
    
    config_content = """
# 兼容性配置 - 适用于版本问题环境
local_services:
  embedding:
    model: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    device: "cpu"
    batch_size: 4  # 小批次，避免内存问题
    implementation: "manual"  # 使用手动实现
  rerank:
    model: "simple"  # 使用简单相似度计算
    device: "cpu"
    implementation: "manual"
  pdf_parser:
    engine: "pypdf2"  # 使用稳定的PyPDF2
  storage:
    type: "local"
    base_path: "./data/images"

# 兼容性设置
compatibility:
  use_manual_implementation: true
  fallback_to_simple: true
  max_retries: 3
"""
    
    try:
        with open("config_compatible.yaml", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("✅ 兼容性配置文件已创建: config_compatible.yaml")
        return True
    except Exception as e:
        print(f"❌ 配置文件创建失败: {e}")
        return False


def main():
    """主函数"""
    print("=== 兼容性测试 ===")
    print("此测试处理版本兼容性问题\n")
    
    tests = [
        ("PyTorch版本", test_torch_version),
        ("transformers基本功能", test_transformers_basic),
        ("sentence-transformers兼容性", test_sentence_transformers_compatible),
        ("简化服务实现", test_simple_services),
        ("创建备选配置", create_fallback_config)
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
    print(f"兼容性测试结果: {passed}/{total}")
    print('='*60)
    
    if passed >= 3:
        print("🎉 基本兼容性测试通过！")
        print("\n✅ 可以使用备选方案")
        print("✅ 建议使用 config_compatible.yaml 配置")
        print("\n下一步:")
        print("1. 如果PyTorch版本有问题，运行: python fix_pytorch_version.py")
        print("2. 使用兼容性配置启动chatdoc")
        return True
    else:
        print("❌ 兼容性测试失败")
        print("\n建议:")
        print("1. 运行: python fix_pytorch_version.py")
        print("2. 检查网络连接")
        print("3. 考虑使用更简单的替代方案")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
