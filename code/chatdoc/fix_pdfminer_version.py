#!/usr/bin/env python3
"""
修复pdfminer版本冲突问题
Author: AI Assistant
Date: 2025-07-29
"""
import subprocess
import sys

def main():
    """主函数"""
    print("=== 修复pdfminer版本冲突 ===")
    print("megaparse需要特定版本的pdfminer\n")
    
    # 选项1：卸载megaparse相关包
    print("选项1: 卸载有冲突的包...")
    packages_to_uninstall = [
        "megaparse",
        "unstructured",
        "pdfminer.six"
    ]
    
    for package in packages_to_uninstall:
        try:
            print(f"卸载 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])
            print(f"✅ {package} 卸载成功")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} 卸载失败或未安装")
    
    # 选项2：安装兼容版本
    print("\n选项2: 安装兼容版本...")
    compatible_packages = [
        "pdfminer.six==20220319",  # 兼容版本
        # 暂时不重新安装megaparse，使用SimplePDF替代
    ]
    
    for package in compatible_packages:
        try:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
    
    print("\n=== 修复完成 ===")
    print("现在可以运行: python start_simple.py")
    print("或者运行: python test_startup.py")

if __name__ == "__main__":
    main()
