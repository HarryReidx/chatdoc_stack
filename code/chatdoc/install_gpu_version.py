#!/usr/bin/env python3
"""
GPU版本依赖安装脚本 - 适用于Linux TITAN*2环境
Author: AI Assistant
Date: 2025-07-28
"""
import subprocess
import sys
import os

def check_cuda():
    """检查CUDA环境"""
    print("=== 检查CUDA环境 ===")
    
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ NVIDIA驱动正常")
            print(result.stdout.split('\n')[0])  # 显示第一行信息
        else:
            print("❌ nvidia-smi 命令失败")
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi 未找到，请检查NVIDIA驱动")
        return False
    
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA编译器可用")
            for line in result.stdout.split('\n'):
                if 'release' in line:
                    print(f"   {line.strip()}")
        else:
            print("⚠️ nvcc 未找到，但不影响PyTorch使用")
    except FileNotFoundError:
        print("⚠️ nvcc 未找到，但不影响PyTorch使用")
    
    return True


def main():
    """主函数"""
    print("=== 安装GPU版本依赖 (Linux TITAN*2环境) ===")
    print("此版本专门为GPU环境优化，支持CUDA加速\n")
    
    # 检查CUDA环境
    if not check_cuda():
        print("CUDA环境检查失败，但仍可继续安装")
    
    # GPU版本的包列表
    packages = [
        # 基础依赖
        "pdfminer.six>=20231228",
        
        # PyTorch GPU版本
        "torch>=2.0.0",
        "torchvision>=0.15.0", 
        "torchaudio>=2.0.0",
        
        # 文本处理（GPU加速）
        "sentence-transformers>=2.2.0",
        "transformers>=4.30.0",
        
        # 高性能PDF解析
        "megaparse>=0.0.55",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
        
        # OpenTelemetry依赖
        "opentelemetry-api==1.23.0",
        "opentelemetry-sdk==1.23.0",
        "opentelemetry-exporter-jaeger==1.21.0",
        "opentelemetry-instrumentation-flask==0.44b0",
        "opentelemetry-instrumentation-requests==0.44b0",
        
        # GPU加速库
        "accelerate>=0.20.0",
        "optimum>=1.8.0",
        
        # 其他工具
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "faiss-gpu>=1.7.0"  # GPU版本的向量搜索
    ]
    
    print("将安装以下包:")
    for pkg in packages:
        print(f"  - {pkg}")
    print()
    
    # 安装包
    for package in packages:
        print(f"正在安装 {package}...")
        try:
            if package == "faiss-gpu>=1.7.0":
                # faiss-gpu需要特殊处理
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package,
                    "--no-cache-dir"
                ])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            if "faiss-gpu" in package:
                print("   尝试安装CPU版本的faiss...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])
                    print("✅ faiss-cpu 安装成功")
                except:
                    print("❌ faiss安装失败，将跳过")
    
    print("\n=== GPU版本安装完成 ===")
    print("现在可以运行 python test_gpu_version.py 测试GPU版本")

if __name__ == "__main__":
    main()
