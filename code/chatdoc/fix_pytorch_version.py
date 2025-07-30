#!/usr/bin/env python3
"""
修复PyTorch版本兼容性问题
Author: AI Assistant
Date: 2025-07-28
"""
import subprocess
import sys

def main():
    """主函数"""
    print("=== 修复PyTorch版本兼容性问题 ===")
    print("将升级PyTorch到2.1.0+cpu版本\n")
    
    # 先卸载旧版本
    print("1. 卸载旧版本PyTorch...")
    packages_to_uninstall = ["torch", "torchvision", "torchaudio"]
    
    for package in packages_to_uninstall:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])
            print(f"✅ {package} 卸载成功")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} 卸载失败或未安装")
    
    # 安装新版本
    print("\n2. 安装新版本PyTorch...")
    torch_packages = [
        "torch==2.1.0+cpu",
        "torchvision==0.16.0+cpu", 
        "torchaudio==2.1.0+cpu"
    ]
    
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
            return False
    
    # 验证安装
    print("\n3. 验证安装...")
    try:
        import torch
        print(f"✅ PyTorch版本: {torch.__version__}")
        print(f"✅ CUDA可用: {torch.cuda.is_available()}")
        
        # 检查是否有compiler属性
        if hasattr(torch, 'compiler'):
            print("✅ torch.compiler 可用")
        else:
            print("⚠️ torch.compiler 不可用，但这是正常的")
        
        return True
        
    except ImportError as e:
        print(f"❌ PyTorch导入失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 PyTorch版本修复完成！")
        print("现在可以重新运行: python test_cpu_version.py")
    else:
        print("\n❌ PyTorch版本修复失败")
        sys.exit(1)
