#!/usr/bin/env python3
"""
模拟文档解析服务器
用于快速验证 TEXTIN API 替换方案
"""

from flask import Flask, request, jsonify
import time
import logging
import os
from werkzeug.utils import secure_filename

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "mock-document-parser",
        "version": "1.0.0",
        "timestamp": time.time()
    })

@app.route('/', methods=['GET'])
def root():
    """根路径"""
    return jsonify({
        "message": "Mock Document Parser Service",
        "version": "1.0.0",
        "endpoints": {
            "parse": "/api/v1/pdf_to_markdown",
            "health": "/health"
        }
    })

@app.route('/api/v1/pdf_to_markdown', methods=['POST'])
def pdf_to_markdown():
    """
    模拟 TEXTIN PDF2MD API
    兼容原有的参数格式
    """
    start_time = time.time()
    
    logger.info("收到文档解析请求")
    
    # 检查文件
    if 'file' not in request.files:
        return jsonify({
            "code": 400,
            "message": "没有上传文件"
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "code": 400,
            "message": "文件名不能为空"
        }), 400
    
    filename = secure_filename(file.filename)
    file_size = len(file.read())
    file.seek(0)  # 重置文件指针
    
    logger.info(f"解析文件: {filename}, 大小: {file_size} bytes")
    
    # 模拟解析延迟
    time.sleep(2)
    
    # 根据文件类型生成不同的模拟内容
    file_ext = filename.lower().split('.')[-1] if '.' in filename else 'unknown'
    
    if file_ext == 'pdf':
        mock_content = f"""# {filename} - PDF文档解析结果

## 文档摘要
这是一个PDF文档的模拟解析结果。

## 主要内容

### 第一章节：概述
本文档包含了重要的业务信息和数据分析。

### 第二章节：数据分析
| 指标 | 数值 | 趋势 |
|------|------|------|
| 营收 | 1000万 | ↗️ 增长 |
| 成本 | 800万 | ↘️ 下降 |
| 利润 | 200万 | ↗️ 增长 |

### 第三章节：结论
- 业务发展稳定
- 盈利能力提升
- 市场前景良好

## 附录
更多详细信息请参考原始文档。

---
*此内容由模拟解析服务生成，用于验证系统功能*
"""
    else:
        mock_content = f"""# {filename} - 文档解析结果

## 文档信息
- 文件名: {filename}
- 文件类型: {file_ext.upper()}
- 文件大小: {file_size} bytes

## 解析内容
这是一个模拟的文档解析结果。

### 主要内容
文档包含了重要信息，已成功解析。

### 结构化数据
| 项目 | 内容 |
|------|------|
| 标题 | 文档标题 |
| 作者 | 未知 |
| 页数 | 估算 {max(1, file_size // 2000)} 页 |

---
*模拟解析服务生成*
"""
    
    # 计算处理时间
    process_time = time.time() - start_time
    estimated_pages = max(1, file_size // 2000)
    
    # 构造兼容 TEXTIN API 的返回格式
    response = {
        "code": 200,
        "result": {
            "detail": mock_content,
            "pages": [
                {
                    "num": i,
                    "content": [],
                    "structured": []
                } for i in range(estimated_pages)
            ],
            "engine": "mock-parser",
            "version": "1.0.0"
        },
        "metrics": [
            {
                "image_id": None,
                "page_num": i
            } for i in range(estimated_pages)
        ],
        "processing_time": round(process_time, 2),
        "file_info": {
            "filename": filename,
            "size": file_size,
            "type": file_ext
        }
    }
    
    logger.info(f"文件解析完成: {filename}, 耗时: {process_time:.2f}s, 页数: {estimated_pages}")
    
    return jsonify(response)

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        "code": 413,
        "message": "文件太大，最大支持16MB"
    }), 413

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"服务器错误: {str(e)}")
    return jsonify({
        "code": 500,
        "message": f"服务器内部错误: {str(e)}"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 启动模拟文档解析服务...")
    print(f"📍 服务地址: http://localhost:{port}")
    print(f"🔗 健康检查: http://localhost:{port}/health")
    print(f"📄 解析接口: http://localhost:{port}/api/v1/pdf_to_markdown")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=True)
