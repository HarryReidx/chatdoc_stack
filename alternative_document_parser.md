# ChatDoc 文档解析替代方案

## 🎯 目标
替换 TEXTIN API，使用开源方案实现文档解析功能。

## 🔧 替代方案

### 方案 1：使用 PyMuPDF + Unstructured
```python
# 安装依赖
pip install pymupdf unstructured[pdf] python-docx

# 文档解析实现
import fitz  # PyMuPDF
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx

def parse_pdf_to_markdown(file_path):
    """PDF 转 Markdown"""
    elements = partition_pdf(file_path)
    markdown_content = ""
    
    for element in elements:
        if element.category == "Title":
            markdown_content += f"# {element.text}\n\n"
        elif element.category == "NarrativeText":
            markdown_content += f"{element.text}\n\n"
        elif element.category == "Table":
            # 表格处理
            markdown_content += f"| {element.text} |\n\n"
    
    return markdown_content
```

### 方案 2：使用 Marker + Surya
```bash
# 安装 Marker (高质量 PDF 转 Markdown)
pip install marker-pdf

# 使用示例
from marker.convert import convert_single_pdf
from marker.models import load_all_models

model_lst = load_all_models()
full_text, images, out_meta = convert_single_pdf("document.pdf", model_lst)
```

### 方案 3：使用 LlamaParse (免费额度)
```python
# LlamaParse - LlamaIndex 的文档解析服务
pip install llama-parse

from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="your_llama_cloud_api_key",  # 免费额度
    result_type="markdown"
)

documents = parser.load_data("document.pdf")
```

## 🔄 修改步骤

### 1. 创建自定义解析服务

创建一个 FastAPI 服务替代 TEXTIN API：

```python
# custom_parser_service.py
from fastapi import FastAPI, File, UploadFile
import tempfile
import os

app = FastAPI()

@app.post("/api/v1/pdf_to_markdown")
async def pdf_to_markdown(file: UploadFile = File(...)):
    """替代 TEXTIN PDF2MD API"""
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # 使用开源工具解析
        markdown_content = parse_pdf_to_markdown(tmp_file_path)
        
        # 返回兼容格式
        return {
            "code": 200,
            "data": {
                "markdown": markdown_content,
                "pages": [],  # 页面信息
                "images": []  # 图片信息
            }
        }
    finally:
        os.unlink(tmp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 2. 修改 Docker 配置

```yaml
# 在 docker-compose.yml 中添加自定义解析服务
custom-parser:
  build: ./custom-parser
  container_name: custom-parser
  restart: always
  ports:
    - "8080:8080"
  networks:
    - chatdoc

# 修改 chatdoc 服务环境变量
chatdoc:
  environment:
    - PDF2MD_URL=http://custom-parser:8080/api/v1/pdf_to_markdown
    # 移除 TEXTIN 相关配置
    # - TEXTIN_APP_ID=xxxxx
    # - TEXTIN_APP_SECRET=xxxxx
```

### 3. 修改配置文件

```yaml
# config.yaml
pdf2md:
  url: http://custom-parser:8080/api/v1/pdf_to_markdown
  # 移除 TEXTIN 相关配置
  # download_url: 'https://api.textin.com/ocr_image/download'
```

## 🚀 推荐方案

### 最佳选择：Marker + 自建服务

1. **优点**：
   - 完全开源，无 API 限制
   - 高质量的 PDF 解析
   - 支持表格、公式、图片
   - 可本地部署

2. **实施步骤**：
   - 使用 Marker 构建解析服务
   - 创建兼容 TEXTIN API 的接口
   - 修改 Docker 配置
   - 测试文档解析功能

## 📊 对比分析

| 方案 | 成本 | 质量 | 维护难度 | 推荐度 |
|------|------|------|----------|--------|
| TEXTIN API | 付费 | 高 | 低 | ⭐⭐⭐⭐ |
| Marker | 免费 | 高 | 中 | ⭐⭐⭐⭐⭐ |
| PyMuPDF | 免费 | 中 | 中 | ⭐⭐⭐ |
| LlamaParse | 免费额度 | 高 | 低 | ⭐⭐⭐⭐ |

## 🔧 实施建议

1. **短期方案**：使用 LlamaParse 的免费额度
2. **长期方案**：基于 Marker 构建自定义解析服务
3. **备选方案**：PyMuPDF + Unstructured 组合
