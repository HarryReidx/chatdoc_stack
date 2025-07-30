#!/usr/bin/env python3
"""
测试启动脚本 - 逐步测试各个组件
Author: AI Assistant
Date: 2025-07-28
"""
import os
import sys

# 设置跳过ES初始化
os.environ['SKIP_ES_INIT'] = '1'

def test_step_by_step():
    """逐步测试各个组件"""
    print("=== 逐步测试ChatDoc组件 ===\n")
    
    # 步骤1: 测试配置加载
    print("步骤1: 测试配置加载...")
    try:
        from pkg.config import config
        print("✅ 配置加载成功")
        
        # 检查关键配置
        if config.get("local_services"):
            print("✅ 本地服务配置存在")
        else:
            print("⚠️ 本地服务配置不存在")
            
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 步骤2: 测试ES模块（跳过模式）
    print("\n步骤2: 测试ES模块...")
    try:
        from pkg.es import global_es
        if global_es is None:
            print("✅ ES已跳过（测试模式）")
        else:
            print("✅ ES初始化成功")
    except Exception as e:
        print(f"❌ ES模块加载失败: {e}")
        return False
    
    # 步骤3: 测试兼容性服务
    print("\n步骤3: 测试兼容性服务...")
    try:
        from pkg.compatibility_adapter import get_compatibility_embedding_service, get_compatibility_rerank_service
        
        embedding_service = get_compatibility_embedding_service()
        print("✅ 嵌入服务初始化成功")
        
        rerank_service = get_compatibility_rerank_service()
        print("✅ 重排序服务初始化成功")
        
    except Exception as e:
        print(f"❌ 兼容性服务初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 步骤4: 测试PDF解析
    print("\n步骤4: 测试PDF解析...")
    try:
        from pkg.clients.simple_pdf_client import SimplePDFClient
        pdf_client = SimplePDFClient()
        print("✅ PDF解析客户端初始化成功")
    except Exception as e:
        print(f"❌ PDF解析客户端初始化失败: {e}")
        return False
    
    # 步骤5: 测试主要接口
    print("\n步骤5: 测试主要接口...")
    try:
        # 测试嵌入接口
        from pkg.embedding.acge_embedding import acge_embedding
        embedding = acge_embedding("测试")
        print(f"✅ 嵌入接口正常，维度: {len(embedding)}")
        
        # 测试重排序接口
        from pkg.rerank import rerank_api
        scores = rerank_api([["查询", "文档"]])
        print(f"✅ 重排序接口正常，分数: {scores}")
        
    except Exception as e:
        print(f"❌ 主要接口测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 步骤6: 测试导入主要模块
    print("\n步骤6: 测试导入主要模块...")
    try:
        # 测试导入pre_import
        print("  导入pre_import...")
        import pre_import
        print("✅ pre_import导入成功")
        
    except Exception as e:
        print(f"❌ 主要模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 所有组件测试通过！")
    return True

def try_start_main():
    """尝试启动主程序"""
    print("\n=== 尝试启动主程序 ===")
    
    try:
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
        print("2. 确认所有配置都正确")
        print("3. 查看上面的详细错误信息")

def main():
    """主函数"""
    print("=== ChatDoc启动测试 ===")
    print("此脚本将逐步测试各个组件，然后尝试启动主程序\n")
    
    # 逐步测试
    if test_step_by_step():
        # 如果基本测试通过，尝试启动主程序
        try_start_main()
    else:
        print("\n❌ 基本组件测试失败，无法启动主程序")
        print("\n建议:")
        print("1. 运行 python test_integration.py 进行详细测试")
        print("2. 检查依赖安装")
        print("3. 查看配置文件")

if __name__ == "__main__":
    main()
