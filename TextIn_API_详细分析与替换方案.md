# TextIn API 详细分析与 Megaparse 替换方案

## TextIn API 使用详情

### 1. PDF 解析 API 详细分析

#### API 调用实现

<augment_code_snippet path="code/chatdoc/pkg/clients/textin_ocr.py" mode="EXCERPT">
````python
class TextinOcr(object):
    def __init__(self, app_id: str = None, app_secret: str = None):
        self._app_id = app_id or config["textin"]["app_id"]
        self._app_secret = app_secret or config["textin"]["app_secret"]
        self.url = config["pdf2md"]["url"]

    def recognize_pdf2md(self, image):
        headers = {
            'x-ti-app-id': self._app_id,
            'x-ti-secret-code': self._app_secret
        }
        return requests.post(self.url, data=image, headers=headers, params=self.options)
````
</augment_code_snippet>

#### 配置参数详解

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `dpi` | 144 | 图像分辨率，影响解析精度 |
| `page_start` | 0 | 起始页码 |
| `page_count` | 2000 | 解析页数限制 |
| `apply_document_tree` | 1 | 是否应用文档结构树 |
| `markdown_details` | 1 | Markdown 详细程度 |
| `page_details` | 1 | 页面详细信息 |
| `table_flavor` | 'html' | 表格格式 (html/md) |
| `get_image` | 'page' | 图片提取方式 |
| `parse_mode` | 'scan' | 解析模式 |

#### 返回数据结构

```json
{
  "code": 200,
  "message": "success",
  "result": {
    "src_page_count": 10,
    "pages": [
      {
        "num": 1,
        "markdown": "# 标题\n内容...",
        "image": {
          "url": "https://api.textin.com/ocr_image/download?image_id=xxx",
          "base64": "data:image/png;base64,..."
        }
      }
    ]
  }
}
```

### 2. 向量化 API 详细分析

#### API 调用实现

<augment_code_snippet path="code/chatdoc/pkg/embedding/acge_embedding.py" mode="EXCERPT">
````python
@retry_exponential_backoff()
def acge_embedding_multi(text_list, dimension=1024, digit=8, headers=None, url=None):
    json_text = {
        "input": text_list,
        "matryoshka_dim": dimension,
        "digit": digit
    }
    headers = headers or {}
    headers.update({
        "x-ti-app-id": config["textin"]["app_id"],
        "x-ti-secret-code": config["textin"]["app_secret"],
    })
    completion = requests.post(url=url or config["textin"]["embedding_url"],
                               headers=headers, json=json_text)
````
</augment_code_snippet>

#### 缓存机制

项目实现了 LRU 缓存来优化向量化性能：

<augment_code_snippet path="code/chatdoc/pkg/embedding/acge_embedding.py" mode="EXCERPT">
````python
acg_lru_cache = LRUCacheDict(max_size=5000, expiration=60 * 60)
acge_embedding_with_cache = LRUCachedFunction(acge_embedding, acg_lru_cache, cache_key_suffix="acge_embedding")
````
</augment_code_snippet>

### 3. 重排序 API 详细分析

#### API 调用实现

<augment_code_snippet path="code/chatdoc/pkg/rerank/__init__.py" mode="EXCERPT">
````python
@retry_exponential_backoff()
def rerank_api(pairs, headers=None, url='http://xxxx/rerank', if_softmax=0):
    json_text = {
        "input": pairs,
        "if_softmax": if_softmax
    }
    headers = headers or {}
    headers.update({
        "x-ti-app-id": config["textin"]["app_id"],
        "x-ti-secret-code": config["textin"]["app_secret"],
    })
    completion = requests.post(url=url or config["textin"]["rerank_url"],
                               headers=headers, json=json_text)
````
</augment_code_snippet>

#### 使用场景

重排序 API 主要用于：
1. **答案相关性排序** - 对检索到的文档片段进行重排序
2. **检索优化** - 提高最终答案的准确性
3. **多轮对话** - 在对话上下文中优化检索结果

## Megaparse 技术分析

### 1. 核心架构

<augment_code_snippet path="code/megaparse/libs/megaparse/src/megaparse/megaparse.py" mode="EXCERPT">
````python
class MegaParse:
    def __init__(
        self,
        formatters: List[BaseFormatter] | None = None,
        config: MegaParseConfig = MegaParseConfig(),
        unstructured_strategy: StrategyEnum = StrategyEnum.AUTO,
    ) -> None:
        self.config = config
        self.formatters = formatters
        self.doctr_parser = DoctrParser(...)
        self.unstructured_parser = UnstructuredParser()
        self.layout_model = LayoutDetector()
````
</augment_code_snippet>

### 2. 解析策略

Megaparse 支持多种解析策略：

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `AUTO` | 自动选择最佳策略 | 通用场景 |
| `HI_RES` | 高精度 OCR 解析 | 复杂文档、图片文字 |
| `FAST` | 快速解析 | 简单文档、性能优先 |

### 3. 配置选项

<augment_code_snippet path="code/megaparse/libs/megaparse/src/megaparse/configs/auto.py" mode="EXCERPT">
````python
class AutoStrategyConfig(BaseModel):
    page_threshold: float = 0.6
    document_threshold: float = 0.2

class TextDetConfig(BaseModel):
    det_arch: str = "fast_base"
    batch_size: int = 2
    assume_straight_pages: bool = True
````
</augment_code_snippet>

## 替换方案设计

### 1. 架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ChatDoc       │    │  Parse Adapter  │    │   Megaparse     │
│   (现有代码)     │◄──►│   (新增组件)     │◄──►│   (本地服务)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   TextIn API    │
                       │   (备用方案)     │
                       └─────────────────┘
```

### 2. 适配器实现

#### PDF 解析适配器

```python
class DocumentParseAdapter:
    def __init__(self, use_megaparse=True):
        self.use_megaparse = use_megaparse
        if use_megaparse:
            self.megaparse = MegaParse()
        else:
            self.textin_ocr = TextinOcr()
    
    def parse_document(self, file_path: str) -> dict:
        if self.use_megaparse:
            return self._parse_with_megaparse(file_path)
        else:
            return self._parse_with_textin(file_path)
    
    def _parse_with_megaparse(self, file_path: str) -> dict:
        # Megaparse 解析逻辑
        result = self.megaparse.load(file_path)
        return self._convert_megaparse_format(result)
    
    def _convert_megaparse_format(self, result: str) -> dict:
        # 转换为 TextIn 兼容格式
        return {
            "code": 200,
            "result": {
                "src_page_count": 1,  # 需要从 result 中提取
                "pages": [
                    {
                        "num": 1,
                        "markdown": result,
                        "image": {"url": ""}
                    }
                ]
            }
        }
```

#### 向量化适配器

```python
class EmbeddingAdapter:
    def __init__(self, use_local_embedding=False):
        self.use_local_embedding = use_local_embedding
        if use_local_embedding:
            # 可以使用 sentence-transformers 等本地模型
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if self.use_local_embedding:
            return self.model.encode(texts).tolist()
        else:
            return acge_embedding_multi(texts)
```

### 3. 配置管理

#### 新增配置项

```yaml
# config.yaml 新增部分
parse_engine:
  primary: "megaparse"  # megaparse | textin
  fallback: "textin"    # 主引擎失败时的备用方案
  
megaparse:
  strategy: "AUTO"      # AUTO | HI_RES | FAST
  device: "cpu"         # cpu | cuda
  batch_size: 2
  
embedding_engine:
  primary: "textin"     # textin | local
  local_model: "all-MiniLM-L6-v2"
```

### 4. 迁移步骤

#### 第一阶段：准备工作

1. **环境搭建**
```bash
# 安装 Megaparse
pip install megaparse

# 安装依赖
apt-get install poppler-utils tesseract-ocr
```

2. **性能测试**
```python
# 创建测试脚本
def benchmark_parsers():
    test_files = ["test1.pdf", "test2.pdf", "test3.pdf"]
    
    for file in test_files:
        # TextIn 解析
        start_time = time.time()
        textin_result = textin_ocr.recognize_pdf2md(file)
        textin_time = time.time() - start_time
        
        # Megaparse 解析
        start_time = time.time()
        megaparse_result = megaparse.load(file)
        megaparse_time = time.time() - start_time
        
        # 比较结果质量和性能
        compare_results(textin_result, megaparse_result, textin_time, megaparse_time)
```

#### 第二阶段：代码集成

1. **修改文档解析模块**

<augment_code_snippet path="code/chatdoc/pkg/doc/pdf2md.py" mode="EXCERPT">
````python
# 在现有代码中添加适配器
def pdf2md(context: Context) -> Context:
    adapter = DocumentParseAdapter(use_megaparse=config.get("use_megaparse", False))
    
    if not context.params.force_doc_parse and local_or_remote_exist(context.doc_parse_path):
        # 使用缓存
        pass
    else:
        # 使用适配器解析
        context.doc_parse_result = adapter.parse_document(context.org_file_path)
````
</augment_code_snippet>

2. **添加错误处理和降级**

```python
def parse_with_fallback(file_path: str) -> dict:
    try:
        # 尝试主要解析引擎
        if config["parse_engine"]["primary"] == "megaparse":
            return megaparse_adapter.parse(file_path)
        else:
            return textin_adapter.parse(file_path)
    except Exception as e:
        logger.warning(f"Primary parser failed: {e}, falling back...")
        # 使用备用引擎
        if config["parse_engine"]["fallback"] == "textin":
            return textin_adapter.parse(file_path)
        else:
            raise e
```

#### 第三阶段：监控和优化

1. **添加监控指标**
```python
class ParseMetrics:
    def __init__(self):
        self.parse_times = []
        self.success_rates = {}
        self.error_counts = {}
    
    def record_parse(self, engine: str, duration: float, success: bool):
        self.parse_times.append((engine, duration))
        if engine not in self.success_rates:
            self.success_rates[engine] = {"success": 0, "total": 0}
        
        self.success_rates[engine]["total"] += 1
        if success:
            self.success_rates[engine]["success"] += 1
```

2. **质量评估**
```python
def evaluate_parse_quality(original_file: str, textin_result: str, megaparse_result: str):
    # 使用 BLEU、ROUGE 等指标评估解析质量
    # 或者人工评估关键信息提取准确性
    pass
```

## 成本效益分析

### TextIn API 成本

| API 类型 | 计费方式 | 预估成本 |
|----------|----------|----------|
| PDF 解析 | 按页计费 | ¥0.1-0.5/页 |
| 向量化 | 按 token 计费 | ¥0.001/1K tokens |
| 重排序 | 按次计费 | ¥0.01/次 |

### Megaparse 部署成本

| 资源类型 | 配置要求 | 预估成本 |
|----------|----------|----------|
| CPU 服务器 | 8核16G | ¥500-1000/月 |
| GPU 服务器 | Tesla T4 | ¥1500-3000/月 |
| 存储 | 500GB SSD | ¥100-200/月 |

### ROI 分析

假设月处理文档量为 10,000 页：
- **TextIn 成本**: ¥1,000-5,000/月
- **Megaparse 成本**: ¥600-3,200/月（含服务器）
- **节省成本**: 20%-60%

## 风险评估与缓解

### 主要风险

1. **解析精度下降** - Megaparse 可能在某些复杂文档上表现不如 TextIn
2. **性能问题** - 本地部署可能面临性能瓶颈
3. **维护成本** - 需要额外的运维工作

### 缓解策略

1. **双引擎并行** - 保持 TextIn 作为备用方案
2. **渐进式迁移** - 先从简单文档开始，逐步扩展
3. **质量监控** - 建立自动化质量检测机制
4. **性能优化** - 使用 GPU 加速、批处理等技术

## 总结

通过详细的技术分析和方案设计，Megaparse 替换 TextIn API 是可行的。建议采用渐进式迁移策略，在保证服务稳定性的前提下，逐步实现成本优化和技术自主可控。
