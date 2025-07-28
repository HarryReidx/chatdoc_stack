# ChatDoc TEXTIN API 快速替换验证方案

## 🎯 验证目标
分阶段替换 TEXTIN API，验证每个功能模块的可替代性。

## 📋 替换优先级

### 阶段1：文档解析替换 (最高优先级)
**影响**：直接影响文档上传和解析
**替换方案**：使用 Marker 或 LlamaParse

### 阶段2：向量嵌入替换 (中等优先级)  
**影响**：影响语义搜索质量
**替换方案**：使用 OpenAI Embeddings 或 HuggingFace

### 阶段3：重排序替换 (中等优先级)
**影响**：影响检索精度
**替换方案**：使用 Cohere Rerank 或本地模型

### 阶段4：图片处理替换 (低优先级)
**影响**：影响图片显示
**替换方案**：本地图片处理

## 🚀 阶段1：文档解析快速验证

### 方案A：使用 LlamaParse (推荐)
```python
# 创建 custom-parser 服务
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
llama-parse==0.4.0
python-multipart==0.0.6

# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from llama_parse import LlamaParse
import tempfile
import os
import json

app = FastAPI()

# 初始化 LlamaParse
parser = LlamaParse(
    api_key="llx-your-api-key",  # 免费额度
    result_type="markdown",
    verbose=True
)

@app.post("/api/v1/pdf_to_markdown")
async def pdf_to_markdown(file: UploadFile = File(...)):
    """替代 TEXTIN PDF2MD API"""
    
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # 使用 LlamaParse 解析
        documents = parser.load_data(tmp_file_path)
        
        # 模拟 TEXTIN API 返回格式
        markdown_content = documents[0].text if documents else ""
        
        return {
            "code": 200,
            "result": {
                "detail": markdown_content,
                "pages": [],  # 简化版本
                "engine": "llamaparse",
                "version": "1.0.0"
            },
            "metrics": [{"image_id": None}]  # 简化版本
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")
    finally:
        os.unlink(tmp_file_path)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### 方案B：使用 Marker (本地部署)
```python
# main.py (Marker版本)
from fastapi import FastAPI, File, UploadFile
from marker.convert import convert_single_pdf
from marker.models import load_all_models
import tempfile
import os

app = FastAPI()

# 加载模型 (启动时加载一次)
model_lst = load_all_models()

@app.post("/api/v1/pdf_to_markdown")
async def pdf_to_markdown(file: UploadFile = File(...)):
    """使用 Marker 解析 PDF"""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # 使用 Marker 转换
        full_text, images, out_meta = convert_single_pdf(tmp_file_path, model_lst)
        
        return {
            "code": 200,
            "result": {
                "detail": full_text,
                "pages": [],
                "engine": "marker",
                "version": "1.0.0"
            },
            "metrics": [{"image_id": None}]
        }
    finally:
        os.unlink(tmp_file_path)
```

## 🔧 部署步骤

### 1. 创建自定义解析服务
```bash
# 创建目录
mkdir custom-parser
cd custom-parser

# 创建文件
# - Dockerfile
# - requirements.txt  
# - main.py (选择方案A或B)
```

### 2. 修改 Docker Compose
```yaml
# 在 docker-compose.yml 中添加
custom-parser:
  build: ./custom-parser
  container_name: custom-parser
  restart: always
  ports:
    - "8080:8080"
  networks:
    - chatdoc

# 修改 chatdoc 服务
chatdoc:
  environment:
    - PDF2MD_URL=http://custom-parser:8080/api/v1/pdf_to_markdown
    # 保留其他 TEXTIN 配置用于其他功能
```

### 3. 测试验证
```bash
# 启动服务
docker-compose up custom-parser

# 测试解析服务
curl -X POST "http://localhost:8080/api/v1/pdf_to_markdown" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.pdf"

# 重启 chatdoc 服务
docker-compose restart chatdoc
```

## 🧪 验证清单

### ✅ 文档解析验证
- [ ] 上传PDF文件
- [ ] 检查解析状态从"解析中"变为"完成"
- [ ] 验证文档内容正确提取
- [ ] 测试表格解析效果
- [ ] 检查中文支持

### ✅ 功能完整性验证
- [ ] 文档搜索功能正常
- [ ] 问答功能正常
- [ ] 文档片段检索正常

## 📊 性能对比

| 指标 | TEXTIN API | LlamaParse | Marker |
|------|------------|------------|--------|
| 成本 | 付费 | 免费额度 | 免费 |
| 质量 | 高 | 高 | 高 |
| 速度 | 快 | 中等 | 慢 |
| 部署 | 无需 | 无需 | 需要GPU |

## 🔄 后续阶段

### 阶段2：向量嵌入替换
```python
# 使用 OpenAI Embeddings
import openai

def openai_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
```

### 阶段3：重排序替换
```python
# 使用 Cohere Rerank
import cohere

co = cohere.Client("your-api-key")
response = co.rerank(
    model="rerank-english-v2.0",
    query=query,
    documents=documents,
    top_n=10
)
```

## 🎯 成功标准

1. **文档解析成功率 > 95%**
2. **解析速度 < 30秒/文档**
3. **中文支持良好**
4. **表格结构保持完整**
5. **系统稳定性不受影响**

## 🚨 回滚方案

如果验证失败，可以快速回滚：
```yaml
# 恢复原配置
chatdoc:
  environment:
    - PDF2MD_URL=https://api.textin.com/ai/service/v1/pdf_to_markdown
```
