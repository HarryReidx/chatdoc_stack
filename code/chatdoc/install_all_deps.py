#!/usr/bin/env python3
"""
安装所有必需依赖的脚本
Author: AI Assistant
Date: 2025-07-29
"""
import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package} 安装失败: {e}")
        return False

def check_package(package_name):
    """检查包是否已安装"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    """主函数"""
    print("=== 安装ChatDoc所需的所有依赖 ===")
    print("这将安装运行ChatDoc所需的基本依赖\n")
    
    # 从requirements.txt读取依赖
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            requirements = f.read().splitlines()
        
        # 过滤掉注释和空行
        packages = []
        for line in requirements:
            line = line.strip()
            if line and not line.startswith("#"):
                packages.append(line)
        
        print(f"从requirements.txt读取到 {len(packages)} 个依赖包")
        
    except FileNotFoundError:
        print("requirements.txt未找到，使用手动列表")
        # 手动列出关键依赖
        packages = [
            "redis==5.0.8",
            "shapely==2.0.6",
            "PyPDF2>=3.0.0",
            "pdfminer.six==20220319",  # 兼容版本
            "elasticsearch>=8.0.0",
            "numpy>=1.24.0",
            "pandas>=2.0.0",
            "requests>=2.28.0",
            "flask>=2.3.0",
            "pyyaml>=6.0",
            "opentelemetry-api==1.23.0",
            "opentelemetry-sdk==1.23.0",
            "opentelemetry-exporter-jaeger==1.21.0",
            "opentelemetry-instrumentation-flask==0.44b0",
            "opentelemetry-instrumentation-requests==0.44b0",
            # 本地服务依赖（可选）
            "sentence-transformers>=2.2.0",
            "torch>=2.0.0",
            "transformers>=4.30.0",
        ]
    
    # 特别处理的包（可能有问题的）
    problematic_packages = ["megaparse", "unstructured"]
    
    # 过滤掉有问题的包
    safe_packages = [pkg for pkg in packages if not any(prob in pkg for prob in problematic_packages)]
    
    print(f"将安装 {len(safe_packages)} 个安全依赖包")
    print("跳过可能有冲突的包:", problematic_packages)
    print()
    
    success_count = 0
    total_count = len(safe_packages)
    
    for package in safe_packages:
        # 检查包名
        package_name = package.split(">=")[0].split("==")[0].split("[")[0]
        
        if check_package(package_name):
            print(f"✅ {package_name} 已安装，跳过")
            success_count += 1
            continue
        
        # 安装包
        if install_package(package):
            success_count += 1
        else:
            print(f"⚠️ {package} 安装失败，但继续安装其他包")
    
    print(f"\n=== 安装完成 ===")
    print(f"成功安装: {success_count}/{total_count}")
    
    if success_count >= total_count * 0.8:  # 80%以上成功
        print("🎉 大部分依赖安装成功！")
        print("\n下一步:")
        print("1. 运行: python test_startup.py")
        print("2. 如果还有问题，运行: python start_simple.py")
    else:
        print("⚠️ 部分依赖安装失败")
        print("\n建议:")
        print("1. 检查网络连接")
        print("2. 尝试使用conda安装失败的包")
        print("3. 查看具体错误信息")
    
    # 验证关键包
    print("\n=== 验证关键依赖 ===")
    critical_packages = [
        ("redis", "Redis缓存"),
        ("shapely", "几何计算"),
        ("PyPDF2", "PDF解析"),
        ("elasticsearch", "搜索引擎"),
        ("flask", "Web框架"),
        ("numpy", "数值计算"),
        ("requests", "HTTP请求")
    ]
    
    for package_name, description in critical_packages:
        if check_package(package_name):
            print(f"✅ {package_name} ({description})")
        else:
            print(f"❌ {package_name} ({description}) - 缺失")

if __name__ == "__main__":
    main()
