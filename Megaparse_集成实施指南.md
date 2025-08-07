# Megaparse 集成实施指南

## 实施概览

本指南提供了将 Megaparse 集成到现有 ChatDoc Stack 项目中的详细步骤，实现从 TextIn 商业 API 到本地部署解析服务的迁移。

## 前置条件

### 系统要求

- Python 3.11+
- 8GB+ RAM
- 50GB+ 可用磁盘空间
- Ubuntu 20.04+ 或 CentOS 7+

### 依赖安装

```bash
# 系统依赖
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr libmagic1

# Python 依赖
pip install megaparse sentence-transformers torch torchvision
```

## 第一阶段：环境搭建和测试

### 1.1 创建 Megaparse 服务

创建新的服务目录：

```bash
mkdir -p code/megaparse-service
cd code/megaparse-service
```

创建服务主文件 `app.py`：

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from megaparse import MegaParse
import io
import os
from typing import Optional

app = FastAPI(title="Megaparse Service", version="1.0.0")

# 初始化 Megaparse
megaparse = MegaParse()

@app.post("/parse/pdf")
async def parse_pdf(
    file: UploadFile = File(...),
    strategy: Optional[str] = "AUTO"
):
    """
    解析 PDF 文件
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # 读取文件内容
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)
        
        # 解析文档
        result = await megaparse.aload(file=file_stream, file_extension=".pdf")
        
        return {
            "code": 200,
            "message": "success",
            "result": {
                "markdown": result,
                "pages": [{"num": 1, "markdown": result}]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 1.2 创建 Docker 配置

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制应用代码
COPY . .

EXPOSE 8001

CMD ["python", "app.py"]
```

创建 `requirements.txt`：

```
fastapi==0.104.1
uvicorn==0.24.0
megaparse==0.0.25
python-multipart==0.0.6
```

### 1.3 性能基准测试

创建测试脚本 `benchmark.py`：

```python
import time
import requests
import json
from pathlib import Path

class ParseBenchmark:
    def __init__(self):
        self.textin_url = "https://api.textin.com/ai/service/v1/pdf_to_markdown"
        self.megaparse_url = "http://localhost:8001/parse/pdf"
        self.textin_headers = {
            'x-ti-app-id': 'your_app_id',
            'x-ti-secret-code': 'your_app_secret'
        }
    
    def test_textin(self, file_path: str):
        """测试 TextIn API"""
        start_time = time.time()
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    self.textin_url,
                    data=f.read(),
                    headers=self.textin_headers,
                    params={'dpi': 144, 'page_count': 2000}
                )
            duration = time.time() - start_time
            return {
                'success': response.status_code == 200,
                'duration': duration,
                'result': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {'success': False, 'duration': time.time() - start_time, 'error': str(e)}
    
    def test_megaparse(self, file_path: str):
        """测试 Megaparse"""
        start_time = time.time()
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f, 'application/pdf')}
                response = requests.post(self.megaparse_url, files=files)
            duration = time.time() - start_time
            return {
                'success': response.status_code == 200,
                'duration': duration,
                'result': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {'success': False, 'duration': time.time() - start_time, 'error': str(e)}
    
    def run_benchmark(self, test_files: list):
        """运行基准测试"""
        results = []
        for file_path in test_files:
            print(f"Testing {file_path}...")
            
            textin_result = self.test_textin(file_path)
            megaparse_result = self.test_megaparse(file_path)
            
            results.append({
                'file': file_path,
                'textin': textin_result,
                'megaparse': megaparse_result
            })
        
        return results

# 使用示例
if __name__ == "__main__":
    benchmark = ParseBenchmark()
    test_files = ["test1.pdf", "test2.pdf", "test3.pdf"]
    results = benchmark.run_benchmark(test_files)
    
    # 保存结果
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
```

## 第二阶段：代码集成

### 2.1 创建解析适配器

在 `code/chatdoc/pkg/adapters/` 目录下创建 `parse_adapter.py`：

```python
import requests
import json
from typing import Dict, Any, Optional
from pkg.config import config
from pkg.utils.logger import logger
from pkg.clients.textin_ocr import TextinOcr

class ParseAdapter:
    """文档解析适配器，支持 TextIn 和 Megaparse"""
    
    def __init__(self):
        self.use_megaparse = config.get("parse_engine", {}).get("primary") == "megaparse"
        self.fallback_engine = config.get("parse_engine", {}).get("fallback", "textin")
        self.megaparse_url = config.get("megaparse", {}).get("url", "http://localhost:8001")
        self.textin_ocr = TextinOcr()
    
    def parse_document(self, file_path: str, force_engine: Optional[str] = None) -> Dict[str, Any]:
        """
        解析文档
        
        Args:
            file_path: 文档路径
            force_engine: 强制使用指定引擎 ('megaparse' | 'textin')
        
        Returns:
            解析结果字典
        """
        engine = force_engine or ("megaparse" if self.use_megaparse else "textin")
        
        try:
            if engine == "megaparse":
                return self._parse_with_megaparse(file_path)
            else:
                return self._parse_with_textin(file_path)
        except Exception as e:
            logger.error(f"Primary engine {engine} failed: {e}")
            
            # 尝试备用引擎
            if not force_engine and self.fallback_engine != engine:
                logger.info(f"Trying fallback engine: {self.fallback_engine}")
                try:
                    if self.fallback_engine == "megaparse":
                        return self._parse_with_megaparse(file_path)
                    else:
                        return self._parse_with_textin(file_path)
                except Exception as fallback_error:
                    logger.error(f"Fallback engine also failed: {fallback_error}")
            
            raise e
    
    def _parse_with_megaparse(self, file_path: str) -> Dict[str, Any]:
        """使用 Megaparse 解析"""
        url = f"{self.megaparse_url}/parse/pdf"
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            response = requests.post(url, files=files, timeout=300)
        
        response.raise_for_status()
        result = response.json()
        
        # 转换为 TextIn 兼容格式
        return self._convert_megaparse_format(result)
    
    def _parse_with_textin(self, file_path: str) -> Dict[str, Any]:
        """使用 TextIn API 解析"""
        with open(file_path, 'rb') as f:
            response = self.textin_ocr.recognize_pdf2md(f.read())
        
        response.raise_for_status()
        return response.json()
    
    def _convert_megaparse_format(self, megaparse_result: Dict[str, Any]) -> Dict[str, Any]:
        """将 Megaparse 结果转换为 TextIn 兼容格式"""
        markdown_content = megaparse_result.get("result", {}).get("markdown", "")
        
        # 简单的页面分割（可以根据需要优化）
        pages = []
        if markdown_content:
            # 按页面分割符或固定长度分割
            page_content = markdown_content
            pages.append({
                "num": 1,
                "markdown": page_content,
                "image": {"url": ""}
            })
        
        return {
            "code": 200,
            "message": "success",
            "result": {
                "src_page_count": len(pages),
                "pages": pages
            }
        }
```

### 2.2 修改现有解析代码

修改 `code/chatdoc/pkg/doc/pdf2md.py`：

```python
# 在文件顶部添加导入
from pkg.adapters.parse_adapter import ParseAdapter

# 修改 pdf2md 函数
def pdf2md(context: Context) -> Context:
    context.doc_parse_path = config["location"]["base_doc_parse_path"].format(BASE_DIR=BASE_DIR) % context.params.uuid

    if not context.params.force_doc_parse and local_or_remote_exist(context.doc_parse_path):
        with open(context.doc_parse_path, "r", encoding="utf-8") as f:
            context.doc_parse_result = json.load(f)
            context.file_meta.page_number = context.doc_parse_result['result']['src_page_count']
    else:
        # 使用适配器解析
        adapter = ParseAdapter()
        context.doc_parse_result = adapter.parse_document(context.org_file_path)
        
        doc_result_json = json.dumps(context.doc_parse_result, ensure_ascii=False)
        context.file_meta.page_number = context.doc_parse_result['result']['src_page_count']
        logger.info(f'doc parser, page_num: {context.file_meta.page_number}')
        
        # 保存解析结果
        thread = ThreadWithReturnValue(target=upload_doc_parser, args=(doc_result_json, context.doc_parse_path,))
        thread.start()
        context.threads.append(thread)

    return context
```

### 2.3 更新配置文件

在 `code/chatdoc/config.yaml` 中添加新配置：

```yaml
# 解析引擎配置
parse_engine:
  primary: "textin"        # textin | megaparse
  fallback: "textin"       # 备用引擎
  
# Megaparse 配置
megaparse:
  url: "http://localhost:8001"
  timeout: 300
  strategy: "AUTO"         # AUTO | HI_RES | FAST
  
# 现有 TextIn 配置保持不变
textin:
  app_id: 'xxxx'
  app_secret: 'xxxxx'
```

## 第三阶段：监控和优化

### 3.1 添加监控指标

创建 `code/chatdoc/pkg/monitoring/parse_metrics.py`：

```python
import time
import json
from typing import Dict, Any
from collections import defaultdict
from pkg.utils.logger import logger

class ParseMetrics:
    """解析性能监控"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_duration': 0.0,
            'avg_duration': 0.0
        })
    
    def record_parse(self, engine: str, duration: float, success: bool, file_size: int = 0):
        """记录解析指标"""
        metric = self.metrics[engine]
        metric['total_requests'] += 1
        metric['total_duration'] += duration
        
        if success:
            metric['successful_requests'] += 1
        else:
            metric['failed_requests'] += 1
        
        metric['avg_duration'] = metric['total_duration'] / metric['total_requests']
        
        # 记录日志
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"Parse {status}: engine={engine}, duration={duration:.2f}s, size={file_size}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取当前指标"""
        return dict(self.metrics)
    
    def reset_metrics(self):
        """重置指标"""
        self.metrics.clear()

# 全局实例
parse_metrics = ParseMetrics()
```

### 3.2 集成监控到适配器

修改 `ParseAdapter` 类：

```python
from pkg.monitoring.parse_metrics import parse_metrics
import os

class ParseAdapter:
    # ... 现有代码 ...
    
    def parse_document(self, file_path: str, force_engine: Optional[str] = None) -> Dict[str, Any]:
        engine = force_engine or ("megaparse" if self.use_megaparse else "textin")
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        start_time = time.time()
        success = False
        
        try:
            if engine == "megaparse":
                result = self._parse_with_megaparse(file_path)
            else:
                result = self._parse_with_textin(file_path)
            
            success = True
            return result
            
        except Exception as e:
            logger.error(f"Primary engine {engine} failed: {e}")
            
            # 记录主引擎失败
            parse_metrics.record_parse(engine, time.time() - start_time, False, file_size)
            
            # 尝试备用引擎
            if not force_engine and self.fallback_engine != engine:
                fallback_start = time.time()
                try:
                    if self.fallback_engine == "megaparse":
                        result = self._parse_with_megaparse(file_path)
                    else:
                        result = self._parse_with_textin(file_path)
                    
                    # 记录备用引擎成功
                    parse_metrics.record_parse(
                        f"{self.fallback_engine}_fallback", 
                        time.time() - fallback_start, 
                        True, 
                        file_size
                    )
                    return result
                    
                except Exception as fallback_error:
                    parse_metrics.record_parse(
                        f"{self.fallback_engine}_fallback", 
                        time.time() - fallback_start, 
                        False, 
                        file_size
                    )
                    logger.error(f"Fallback engine also failed: {fallback_error}")
            
            raise e
        
        finally:
            if success:
                parse_metrics.record_parse(engine, time.time() - start_time, True, file_size)
```

### 3.3 添加监控接口

在 `code/chatdoc/main.py` 中添加监控端点：

```python
from pkg.monitoring.parse_metrics import parse_metrics

@app.route("/api/v1/metrics/parse", methods=["GET"])
def get_parse_metrics():
    """获取解析性能指标"""
    return return_data(200, parse_metrics.get_metrics())

@app.route("/api/v1/metrics/parse/reset", methods=["POST"])
def reset_parse_metrics():
    """重置解析指标"""
    parse_metrics.reset_metrics()
    return return_data(200, {"message": "Metrics reset successfully"})
```

## 第四阶段：部署和切换

### 4.1 Docker Compose 配置

创建 `docker-compose.megaparse.yml`：

```yaml
version: '3.8'

services:
  megaparse-service:
    build: ./code/megaparse-service
    ports:
      - "8001:8001"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  chatdoc:
    # 现有配置
    depends_on:
      - megaparse-service
    environment:
      - MEGAPARSE_URL=http://megaparse-service:8001
```

### 4.2 渐进式切换策略

1. **阶段 1：并行运行**
   - 保持 TextIn 为主引擎
   - Megaparse 作为备用引擎
   - 收集性能数据

2. **阶段 2：部分切换**
   - 对特定类型文档使用 Megaparse
   - 监控解析质量和性能

3. **阶段 3：完全切换**
   - Megaparse 为主引擎
   - TextIn 作为备用引擎

4. **阶段 4：移除依赖**
   - 确认 Megaparse 稳定运行
   - 移除 TextIn API 依赖

### 4.3 回滚计划

如果出现问题，可以快速回滚：

```bash
# 回滚到 TextIn
kubectl set env deployment/chatdoc PARSE_ENGINE_PRIMARY=textin

# 或者修改配置文件
sed -i 's/primary: "megaparse"/primary: "textin"/' config.yaml
```

## 验收标准

### 功能验收
- [ ] PDF 解析功能正常
- [ ] 解析结果格式兼容
- [ ] 错误处理和降级机制工作正常
- [ ] 监控指标正确记录

### 性能验收
- [ ] 解析速度不低于 TextIn 的 80%
- [ ] 内存使用在可接受范围内
- [ ] 并发处理能力满足需求

### 质量验收
- [ ] 文本提取准确率 > 95%
- [ ] 表格识别准确率 > 90%
- [ ] 文档结构保持完整

## 故障排除

### 常见问题

1. **Megaparse 服务启动失败**
   - 检查依赖安装
   - 确认端口未被占用
   - 查看服务日志

2. **解析结果格式不兼容**
   - 检查格式转换逻辑
   - 对比 TextIn 和 Megaparse 输出

3. **性能问题**
   - 调整批处理大小
   - 考虑使用 GPU 加速
   - 优化并发配置

### 日志分析

```bash
# 查看解析服务日志
docker logs megaparse-service

# 查看 ChatDoc 日志
tail -f code/chatdoc/logs/app.log | grep "parse"

# 监控系统资源
htop
nvidia-smi  # 如果使用 GPU
```

通过以上实施指南，可以系统性地将 Megaparse 集成到现有项目中，实现从商业 API 到本地部署的平滑迁移。
