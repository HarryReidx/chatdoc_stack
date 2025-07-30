#!/usr/bin/env python3
"""
修复缺失依赖的脚本
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
    print("=== 修复缺失依赖 ===")
    
    # 需要检查和安装的包
    packages = [
        ("shapely", "shapely==2.0.6"),
        ("geopandas", "geopandas"),  # 可能需要的几何处理库
        ("fiona", "fiona"),  # shapely的依赖
    ]
    
    for package_name, install_name in packages:
        print(f"\n检查 {package_name}...")
        
        if check_package(package_name):
            print(f"✅ {package_name} 已安装")
        else:
            print(f"⚠️ {package_name} 未安装，正在安装...")
            
            # 尝试不同的安装方法
            success = False
            
            # 方法1：直接安装
            if install_package(install_name):
                success = True
            else:
                # 方法2：使用预编译版本
                print(f"尝试使用预编译版本安装 {package_name}...")
                if install_package(f"{install_name} --only-binary={package_name}"):
                    success = True
                else:
                    # 方法3：使用conda（如果可用）
                    print(f"尝试使用conda安装 {package_name}...")
                    try:
                        subprocess.check_call(["conda", "install", "-y", package_name])
                        print(f"✅ {package_name} 通过conda安装成功")
                        success = True
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(f"❌ conda安装也失败")
            
            if not success:
                print(f"⚠️ {package_name} 安装失败，但可能不影响核心功能")
    
    # 验证安装
    print("\n=== 验证安装 ===")
    
    try:
        import shapely
        print("✅ shapely 导入成功")
        print(f"   版本: {shapely.__version__}")
    except ImportError as e:
        print(f"❌ shapely 导入失败: {e}")
        print("   这可能会影响某些几何处理功能")
    
    print("\n=== 修复完成 ===")
    print("现在可以重新运行: python test_startup.py")

if __name__ == "__main__":
    main()
