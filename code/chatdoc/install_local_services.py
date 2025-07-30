#!/usr/bin/env python3
"""
安装本地服务依赖的脚本
Author: AI Assistant
Date: 2025-07-28
"""
import subprocess
import sys
import os

# 简单的日志函数，避免循环依赖
def log_info(msg):
    print(f"[INFO] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}")

def log_warning(msg):
    print(f"[WARNING] {msg}")


def install_package(package):
    """安装Python包"""
    try:
        log_info(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        log_info(f"{package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"安装 {package} 失败: {e}")
        return False


def check_package(package):
    """检查包是否已安装"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def install_local_services():
    """安装本地服务所需的依赖"""
    log_info("开始安装本地服务依赖...")

    # 需要安装的包列表
    packages = [
        "megaparse>=0.0.55",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
        "transformers>=4.30.0"
    ]

    success_count = 0

    for package in packages:
        package_name = package.split(">=")[0].split("==")[0]

        # 检查是否已安装
        if check_package(package_name):
            log_info(f"{package_name} 已安装，跳过")
            success_count += 1
            continue

        # 安装包
        if install_package(package):
            success_count += 1

    if success_count == len(packages):
        log_info("所有依赖安装成功！")
        return True
    else:
        log_error(f"安装完成，成功: {success_count}/{len(packages)}")
        return False


def download_models():
    """下载预训练模型"""
    log_info("开始下载预训练模型...")

    try:
        from sentence_transformers import SentenceTransformer, CrossEncoder

        # 下载嵌入模型
        log_info("下载嵌入模型: all-mpnet-base-v2")
        SentenceTransformer("all-mpnet-base-v2")
        log_info("嵌入模型下载完成")

        # 下载重排序模型
        log_info("下载重排序模型: cross-encoder/ms-marco-MiniLM-L-12-v2")
        CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
        log_info("重排序模型下载完成")

        log_info("所有模型下载完成！")
        return True

    except Exception as e:
        log_error(f"模型下载失败: {e}")
        return False


def test_services():
    """测试本地服务"""
    log_info("开始测试本地服务...")

    try:
        # 测试MegaParse
        log_info("测试MegaParse...")
        from pkg.clients.megaparse_client import MegaParseClient
        client = MegaParseClient()
        log_info("MegaParse 初始化成功")

        # 测试嵌入服务
        log_info("测试嵌入服务...")
        from pkg.embedding.local_embedding import get_embedding_service
        embedding_service = get_embedding_service()
        test_embedding = embedding_service.encode_single("测试文本")
        log_info(f"嵌入服务测试成功，向量维度: {len(test_embedding)}")

        # 测试重排序服务
        log_info("测试重排序服务...")
        from pkg.rerank.local_rerank import get_rerank_service
        rerank_service = get_rerank_service()
        test_scores = rerank_service.rerank("查询", ["文档1", "文档2"])
        log_info(f"重排序服务测试成功，分数: {test_scores}")

        log_info("所有服务测试通过！")
        return True

    except Exception as e:
        log_error(f"服务测试失败: {e}")
        return False


def main():
    """主函数"""
    log_info("=== 本地服务安装程序 ===")

    # 步骤1: 安装依赖
    if not install_local_services():
        log_error("依赖安装失败，退出")
        sys.exit(1)

    # 步骤2: 下载模型
    if not download_models():
        log_warning("模型下载失败，但可以继续使用（首次使用时会自动下载）")

    # 步骤3: 测试服务
    if not test_services():
        log_error("服务测试失败，请检查配置")
        sys.exit(1)

    log_info("=== 安装完成 ===")
    log_info("现在可以使用本地服务替代TEXTIN了！")
    log_info("请确保config.yaml中的local_services配置正确")


if __name__ == "__main__":
    main()
