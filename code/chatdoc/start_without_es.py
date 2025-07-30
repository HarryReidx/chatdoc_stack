#!/usr/bin/env python3
"""
不依赖ES的启动脚本 - 用于测试本地服务
Author: AI Assistant
Date: 2025-07-28
"""
import os
import sys

# 设置环境变量，跳过ES初始化
os.environ['SKIP_ES_INIT'] = '1'

def mock_es_module():
    """模拟ES模块，避免初始化错误"""
    import sys
    from unittest.mock import MagicMock
    
    # 创建模拟的ES类
    class MockES:
        def __init__(self, *args, **kwargs):
            print("⚠️ 使用模拟ES服务（仅用于测试本地服务）")
        
        def search(self, *args, **kwargs):
            return {"hits": {"hits": [], "total": {"value": 0}}}
        
        def index(self, *args, **kwargs):
            return {"result": "created"}
        
        def delete(self, *args, **kwargs):
            return {"result": "deleted"}
        
        def exists(self, *args, **kwargs):
            return False
        
        def create(self, *args, **kwargs):
            return {"acknowledged": True}
    
    # 模拟elasticsearch模块
    mock_elasticsearch = MagicMock()
    mock_elasticsearch.Elasticsearch = MockES
    sys.modules['elasticsearch'] = mock_elasticsearch
    
    print("✅ ES模块已模拟")

def main():
    """主函数"""
    print("=== 启动ChatDoc (不依赖ES) ===")
    print("此模式用于测试本地服务，不包含ES搜索功能\n")
    
    # 模拟ES模块
    mock_es_module()
    
    try:
        # 导入并启动主程序
        print("正在启动ChatDoc...")
        
        # 先测试基本导入
        try:
            from pkg.config import config
            print("✅ 配置加载成功")
        except Exception as e:
            print(f"❌ 配置加载失败: {e}")
            return
        
        try:
            from pkg.compatibility_adapter import get_compatibility_embedding_service
            embedding_service = get_compatibility_embedding_service()
            print("✅ 兼容性嵌入服务初始化成功")
        except Exception as e:
            print(f"❌ 嵌入服务初始化失败: {e}")
            return
        
        try:
            from pkg.compatibility_adapter import get_compatibility_rerank_service
            rerank_service = get_compatibility_rerank_service()
            print("✅ 兼容性重排序服务初始化成功")
        except Exception as e:
            print(f"❌ 重排序服务初始化失败: {e}")
            return
        
        # 如果基本服务都正常，尝试启动主程序
        print("\n🚀 基本服务初始化完成，尝试启动主程序...")
        
        # 导入主程序
        import main
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 建议:")
        print("1. 检查是否安装了所有依赖")
        print("2. 运行 python test_integration.py 测试基本功能")
        print("3. 如果需要完整功能，请安装并配置Elasticsearch")

if __name__ == "__main__":
    main()
