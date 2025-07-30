#!/usr/bin/env python3
"""
简单的依赖安装脚本
Author: AI Assistant
Date: 2025-07-28
"""
import subprocess
import sys
import os

def main():
    """主函数"""
    print("=== 安装本地服务依赖 ===")
    
    # 需要安装的包列表
    packages = [
        "pdfminer.six>=20231228",  # 修复pdfminer版本
        "megaparse>=0.0.55",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "opentelemetry-api==1.23.0",
        "opentelemetry-sdk==1.23.0",
        "opentelemetry-exporter-jaeger==1.21.0",
        "opentelemetry-instrumentation-flask==0.44b0",
        "opentelemetry-instrumentation-requests==0.44b0"
    ]
    
    for package in packages:
        print(f"正在安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            print("请手动安装或检查网络连接")
    
    print("\n=== 安装完成 ===")
    print("现在可以运行 python test_local_services.py 测试服务")

if __name__ == "__main__":
    main()
