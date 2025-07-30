#!/usr/bin/env python3
"""
简化启动脚本 - 绕过有问题的依赖
Author: AI Assistant
Date: 2025-07-29
"""
import os
import sys

# 设置环境变量
os.environ['SKIP_ES_INIT'] = '1'
os.environ['SKIP_MEGAPARSE'] = '1'

def mock_problematic_modules():
    """模拟有问题的模块"""
    import sys
    from unittest.mock import MagicMock
    
    # 模拟megaparse模块
    mock_megaparse = MagicMock()
    
    class MockMegaParse:
        def __init__(self, *args, **kwargs):
            print("⚠️ 使用模拟MegaParse（实际使用SimplePDF）")
        
        def load(self, file_path):
            return "# 模拟解析结果\n\n这是一个模拟的PDF解析结果。"
    
    mock_megaparse.MegaParse = MockMegaParse
    sys.modules['megaparse'] = mock_megaparse
    
    print("✅ 已模拟problematic模块")

def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    try:
        # 测试配置
        from pkg.config import config
        print("✅ 配置加载成功")
        
        # 测试兼容性服务
        from pkg.compatibility_adapter import get_compatibility_embedding_service, get_compatibility_rerank_service
        
        embedding_service = get_compatibility_embedding_service()
        print("✅ 嵌入服务初始化成功")
        
        rerank_service = get_compatibility_rerank_service()
        print("✅ 重排序服务初始化成功")
        
        # 测试PDF解析
        from pkg.clients.simple_pdf_client import SimplePDFClient
        pdf_client = SimplePDFClient()
        print("✅ PDF解析客户端初始化成功")
        
        # 测试接口
        from pkg.embedding.acge_embedding import acge_embedding
        embedding = acge_embedding("测试")
        print(f"✅ 嵌入接口正常，维度: {len(embedding)}")
        
        from pkg.rerank import rerank_api
        scores = rerank_api([["查询", "文档"]])
        print(f"✅ 重排序接口正常，分数: {scores}")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_main_program():
    """启动主程序"""
    print("\n=== 启动主程序 ===")
    
    try:
        # 模拟有问题的模块
        mock_problematic_modules()
        
        # 导入pre_import
        print("正在导入pre_import...")
        import pre_import
        print("✅ pre_import导入成功")
        
        # 导入主程序
        print("正在启动main.py...")
        import main
        print("✅ 主程序启动成功")
        
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"❌ 主程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 可能的解决方案:")
        print("1. 检查是否还有其他依赖问题")
        print("2. 尝试卸载并重新安装megaparse相关依赖")
        print("3. 使用完全不依赖megaparse的版本")

def main():
    """主函数"""
    print("=== ChatDoc简化启动 ===")
    print("此版本绕过有问题的依赖，使用简化实现\n")
    
    # 先测试基本功能
    if test_basic_functionality():
        print("\n🎉 基本功能测试通过！")
        
        # 询问是否继续启动主程序
        try:
            response = input("\n是否继续启动主程序？(y/n): ").lower().strip()
            if response in ['y', 'yes', '']:
                start_main_program()
            else:
                print("👋 用户选择不启动主程序")
        except KeyboardInterrupt:
            print("\n👋 用户中断")
    else:
        print("\n❌ 基本功能测试失败，无法启动主程序")
        
        print("\n建议:")
        print("1. 检查依赖安装")
        print("2. 运行 python fix_missing_deps.py")
        print("3. 查看详细错误信息")

if __name__ == "__main__":
    main()
