#!/usr/bin/env python3
"""
CPU版本依赖安装脚本 - 适用于Windows AMD显卡环境
Author: AI Assistant
Date: 2025-07-28
"""
import subprocess
import sys
import os

def main():
    """主函数"""
    print("=== 安装CPU版本依赖 (Windows AMD显卡环境) ===")
    print("这个版本专门为CPU环境优化，避免CUDA相关问题\n")
    
    # CPU版本的包列表
    packages = [
        # 基础依赖
        "pdfminer.six>=20231228",
        
        # PyTorch CPU版本（避免CUDA问题）
        "torch==2.1.0+cpu",
        "torchvision==0.16.0+cpu",
        "torchaudio==2.1.0+cpu",
        
        # 文本处理
        "sentence-transformers>=2.2.0",
        "transformers>=4.30.0",
        
        # PDF解析备选方案
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
        
        # OpenTelemetry依赖
        "opentelemetry-api==1.23.0",
        "opentelemetry-sdk==1.23.0",
        "opentelemetry-exporter-jaeger==1.21.0",
        "opentelemetry-instrumentation-flask==0.44b0",
        "opentelemetry-instrumentation-requests==0.44b0",
        
        # 其他工具
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0"
    ]
    
    print("将安装以下包:")
    for pkg in packages:
        print(f"  - {pkg}")
    print()
    
    # 设置PyTorch CPU版本的索引
    torch_packages = ["torch==2.1.0+cpu", "torchvision==0.16.0+cpu", "torchaudio==2.1.0+cpu"]
    other_packages = [pkg for pkg in packages if not pkg.startswith("torch")]
    
    # 先安装PyTorch CPU版本
    print("1. 安装PyTorch CPU版本...")
    for package in torch_packages:
        print(f"正在安装 {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package,
                "--index-url", "https://download.pytorch.org/whl/cpu"
            ])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
    
    # 安装其他包
    print("\n2. 安装其他依赖...")
    for package in other_packages:
        print(f"正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            if "megaparse" in package:
                print("   megaparse可能有版本冲突，我们将使用备选方案")
    
    print("\n=== 安装完成 ===")
    print("现在可以运行 python test_cpu_version.py 测试CPU版本")

if __name__ == "__main__":
    main()
