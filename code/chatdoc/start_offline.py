#!/usr/bin/env python3
"""
完全离线启动脚本
Author: AI Assistant
Date: 2025-07-29
"""
import os
import sys

# 设置环境变量
os.environ['SKIP_ES_INIT'] = '1'
os.environ['CONFIG_PATH'] = './config_offline.yaml'

def install_missing_deps():
    """安装缺失的依赖"""
    print("=== 检查并安装缺失依赖 ===")
    
    import subprocess
    
    required_packages = [
        "opentelemetry-api",
        "opentelemetry-sdk", 
        "opentelemetry-exporter-jaeger",
        "opentelemetry-instrumentation-flask",
        "opentelemetry-instrumentation-requests",
        "redis",
        "PyPDF2"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"⚠️ {package} 未安装，正在安装...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"❌ {package} 安装失败")

def test_core_functionality():
    """测试核心功能"""
    print("\n=== 测试核心功能 ===")
    
    try:
        # 测试配置加载
        from pkg.config import config
        print("✅ 配置加载成功")
        
        # 测试兼容性服务
        from pkg.compatibility_adapter import get_compatibility_embedding_service, get_compatibility_rerank_service
        
        embedding_service = get_compatibility_embedding_service()
        print("✅ 嵌入服务初始化成功")
        
        rerank_service = get_compatibility_rerank_service()
        print("✅ 重排序服务初始化成功")
        
        # 快速功能测试
        embedding = embedding_service.encode_single("测试")
        print(f"✅ 嵌入测试成功，维度: {len(embedding)}")
        
        scores = rerank_service.rerank_pairs([["查询", "文档"]])
        print(f"✅ 重排序测试成功，分数: {scores}")
        
        return True
        
    except Exception as e:
        print(f"❌ 核心功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def mock_external_services():
    """模拟外部服务"""
    print("\n=== 模拟外部服务 ===")
    
    import sys
    from unittest.mock import MagicMock
    
    # 模拟redis
    mock_redis = MagicMock()
    mock_redis.Redis = MagicMock()
    sys.modules['redis'] = mock_redis
    
    # 模拟elasticsearch
    mock_es = MagicMock()
    mock_es.Elasticsearch = MagicMock()
    sys.modules['elasticsearch'] = mock_es
    
    print("✅ 外部服务已模拟")

def start_chatdoc():
    """启动ChatDoc"""
    print("\n=== 启动ChatDoc ===")
    
    try:
        # 模拟外部服务
        mock_external_services()
        
        # 导入pre_import
        print("正在导入pre_import...")
        import pre_import
        print("✅ pre_import导入成功")
        
        # 启动主程序
        print("正在启动main.py...")
        import main
        print("✅ ChatDoc启动成功")
        
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"❌ ChatDoc启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 可能的解决方案:")
        print("1. 检查是否还有其他依赖问题")
        print("2. 查看详细错误信息")
        print("3. 尝试逐步调试")

def main():
    """主函数"""
    print("=== ChatDoc完全离线启动 ===")
    print("此版本使用离线配置，模拟所有外部服务\n")
    
    # 步骤1：安装依赖
    install_missing_deps()
    
    # 步骤2：测试核心功能
    if not test_core_functionality():
        print("\n❌ 核心功能测试失败，无法继续")
        return
    
    print("\n🎉 核心功能测试通过！")
    
    # 步骤3：询问是否继续启动
    try:
        response = input("\n是否继续启动完整ChatDoc系统？(y/n): ").lower().strip()
        if response in ['y', 'yes', '']:
            start_chatdoc()
        else:
            print("👋 用户选择不启动完整系统")
            print("\n✅ 核心TEXTIN替代功能已验证可用")
            print("✅ 可以在需要时启动完整系统")
    except KeyboardInterrupt:
        print("\n👋 用户中断")

if __name__ == "__main__":
    main()
