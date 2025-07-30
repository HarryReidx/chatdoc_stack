#!/usr/bin/env python3
"""
测试修复后的重排序功能
Author: AI Assistant
Date: 2025-07-29
"""
import os
import sys

# 设置环境变量
os.environ['SKIP_ES_INIT'] = '1'

def test_rerank_improvement():
    """测试改进后的重排序功能"""
    print("=== 测试改进后的重排序功能 ===\n")
    
    try:
        from pkg.compatibility_adapter import get_compatibility_rerank_service
        rerank_service = get_compatibility_rerank_service()
        
        # 测试用例1：明显相关性不同的文档
        print("测试用例1：AI相关查询")
        query = "人工智能"
        documents = [
            "人工智能是计算机科学的一个重要分支",
            "今天天气很好，阳光明媚",
            "机器学习是人工智能的核心技术",
            "深度学习神经网络算法",
            "我喜欢吃苹果和香蕉"
        ]
        
        pairs = [[query, doc] for doc in documents]
        scores = rerank_service.rerank_pairs(pairs)
        
        print(f"查询: {query}")
        print("重排序结果:")
        
        # 按分数排序
        sorted_results = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        for i, (doc, score) in enumerate(sorted_results):
            print(f"  {i+1}. 分数: {score:.4f} - {doc}")
        
        # 测试用例2：包含关系
        print("\n测试用例2：包含关系")
        query2 = "机器学习"
        documents2 = [
            "机器学习算法",
            "深度学习是机器学习的一种方法",
            "今天下雨了",
            "学习Python编程"
        ]
        
        pairs2 = [[query2, doc] for doc in documents2]
        scores2 = rerank_service.rerank_pairs(pairs2)
        
        print(f"查询: {query2}")
        print("重排序结果:")
        
        sorted_results2 = sorted(zip(documents2, scores2), key=lambda x: x[1], reverse=True)
        for i, (doc, score) in enumerate(sorted_results2):
            print(f"  {i+1}. 分数: {score:.4f} - {doc}")
        
        # 测试用例3：英文查询
        print("\n测试用例3：英文查询")
        query3 = "machine learning"
        documents3 = [
            "machine learning algorithms",
            "deep learning neural networks",
            "today is sunny",
            "artificial intelligence research"
        ]
        
        pairs3 = [[query3, doc] for doc in documents3]
        scores3 = rerank_service.rerank_pairs(pairs3)
        
        print(f"查询: {query3}")
        print("重排序结果:")
        
        sorted_results3 = sorted(zip(documents3, scores3), key=lambda x: x[1], reverse=True)
        for i, (doc, score) in enumerate(sorted_results3):
            print(f"  {i+1}. 分数: {score:.4f} - {doc}")
        
        print("\n✅ 重排序功能测试完成")
        
        # 检查是否有合理的分数分布
        all_scores = scores + scores2 + scores3
        max_score = max(all_scores)
        min_score = min(all_scores)
        
        print(f"\n📊 分数统计:")
        print(f"   最高分: {max_score:.4f}")
        print(f"   最低分: {min_score:.4f}")
        print(f"   分数范围: {max_score - min_score:.4f}")
        
        if max_score > 0.1 and (max_score - min_score) > 0.05:
            print("✅ 重排序算法工作正常，有合理的分数区分度")
            return True
        else:
            print("⚠️ 重排序算法可能需要进一步优化")
            return False
        
    except Exception as e:
        print(f"❌ 重排序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== 重排序功能修复测试 ===")
    
    if test_rerank_improvement():
        print("\n🎉 重排序功能修复成功！")
        print("\n现在可以运行完整测试:")
        print("python test_minimal.py")
    else:
        print("\n❌ 重排序功能仍需优化")

if __name__ == "__main__":
    main()
