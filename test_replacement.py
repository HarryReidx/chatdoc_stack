#!/usr/bin/env python3
"""
测试 TEXTIN API 替换效果
"""

import requests
import json
import time
import tempfile
import os

def create_test_file():
    """创建测试文件"""
    content = """# 测试文档

这是一个用于测试文档解析功能的示例文档。

## 业务概述
本公司专注于人工智能技术的研发和应用。

### 财务数据
| 项目 | 2023年 | 2024年 | 增长率 |
|------|--------|--------|--------|
| 营收 | 1000万 | 1200万 | 20% |
| 利润 | 200万 | 280万 | 40% |

## 发展规划
- 扩大研发团队
- 开拓新市场
- 提升产品质量

### 技术栈
1. Python
2. Docker
3. Elasticsearch
4. Redis

**结论**: 公司发展前景良好。
"""
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name

def test_mock_parser():
    """测试模拟解析服务"""
    print("🧪 测试模拟解析服务...")
    
    # 创建测试文件
    test_file_path = create_test_file()
    
    try:
        # 测试健康检查
        health_response = requests.get("http://localhost:8080/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 模拟服务健康检查通过")
        else:
            print("❌ 模拟服务健康检查失败")
            return False
        
        # 测试文档解析
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_document.txt', f, 'text/plain')}
            response = requests.post(
                "http://localhost:8080/api/v1/pdf_to_markdown",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 文档解析测试成功")
            print(f"📄 解析内容长度: {len(result['result']['detail'])} 字符")
            print(f"📊 页数: {len(result['result']['pages'])} 页")
            print(f"⏱️ 处理时间: {result.get('processing_time', 'N/A')} 秒")
            return True
        else:
            print(f"❌ 文档解析测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {str(e)}")
        return False
    finally:
        # 清理测试文件
        try:
            os.unlink(test_file_path)
        except:
            pass

def test_chatdoc_integration():
    """测试 chatdoc 服务集成"""
    print("🔗 测试 chatdoc 服务集成...")
    
    try:
        # 测试对话功能
        chat_data = {
            "question": "你好，请介绍一下系统功能",
            "stream": False,
            "qa_type": "personal",
            "user_id": "1"
        }
        
        response = requests.post(
            "http://localhost:48092/api/v1/chat/global/infer",
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ chatdoc 服务响应正常")
            return True
        else:
            print(f"⚠️ chatdoc 服务响应异常: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ chatdoc 集成测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试 TEXTIN API 替换效果")
    print("=" * 50)
    
    # 测试模拟解析服务
    mock_test_result = test_mock_parser()
    print()
    
    # 测试 chatdoc 集成
    integration_test_result = test_chatdoc_integration()
    print()
    
    # 总结结果
    print("=" * 50)
    print("📊 测试结果总结:")
    print(f"  模拟解析服务: {'✅ 通过' if mock_test_result else '❌ 失败'}")
    print(f"  chatdoc 集成: {'✅ 通过' if integration_test_result else '❌ 失败'}")
    
    if mock_test_result and integration_test_result:
        print("\n🎉 恭喜！TEXTIN API 替换验证成功！")
        print("📋 下一步可以:")
        print("1. 访问前端 http://localhost:48091 测试文档上传")
        print("2. 替换为真实的解析服务（LlamaParse 或 Marker）")
        print("3. 逐步替换其他 TEXTIN API 功能")
    else:
        print("\n⚠️ 替换验证未完全成功，请检查:")
        print("1. 模拟服务是否正常运行")
        print("2. chatdoc 服务配置是否正确")
        print("3. 网络连接是否正常")

if __name__ == "__main__":
    main()
