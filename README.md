# chatdoc-stack

## 目录
- [项目简介](#项目简介)
- [快速开始](#安装)
- [TextIn替换方案](#textin替换方案)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 项目简介
### 💡chatdoc是什么？
chatdoc是一款基于[TextIn xParse](https://www.textin.com/market/detail/pdf_to_markdown)解析服务构建的开源RAG(Retrieval-Augmented-Generation)引擎。支持解析多种文件格式，为企业和个人轻松打造知识库，通过结合知识检索与大语言模型(LLM)技术，提供可靠的知识问答以及答案溯源功能。

### 👉产品体验
请登陆网址(https://www.textin.com/product/textin_intfinq)

### ⭐️主要功能
- 基于[TextIn xParse](https://www.textin.com/market/detail/pdf_to_markdown),提供通用文档解析服务，一个接口，支持PDF/Word(doc/docx)、常见图片(jpg/png/webp/tiff)、HTML等多种文件格式。一次请求，即可获取文字、表格、标题层级、公式、手写字符、图片信息
- 支持单文档、多文档、知识库全局问答
- 支持前端高亮展示检索原文

### 🚩[acge](https://www.textin.com/market/detail/acge_text_embedding)文本向量模型
- 自研文本向量模型[acge](https://www.textin.com/market/detail/acge_text_embedding)，为检索精度提供保障
- 提供接口调用方式，本地无需显卡资源
- 本地部署调用请参考[此链接](https://github.com/intsig-textin/acge_text_embedding)

### 🌱文档目录树切片策略
- 文本、表格、标题分别处理，应对各类复杂场景
- 标题层级递归切片，保留文档内在逻辑结构的完整性
- small2big兼顾检索准确性与语义完整性，保证答案全面

### 🍱有理有据、减少幻觉
- 多路召回、融合排序等，丰富搜索信息
- 答案溯源，确保答案准确性

## 快速开始

### 系统配置要求

- **CPU**：4核以上。
- **内存**：16G以上。
- **存储空间**：保证至少有40G以上的存储空间可用。

### 环境准备

在开始之前，请确保您的系统已安装以下依赖：

- **Docker**：用于容器化部署。
- **Docker Compose**：用于管理多容器应用。
- **TextIn API Key 和 Secret Key**：用于调用TextIn的解析服务。可以从[TextIn工作台](https://www.textin.com/console/dashboard/setting)获取
- **大模型相关配置**：用于调用大模型的API。

### 步骤 1: 🔨︎克隆仓库

首先，将 `chatdoc_stack` 仓库克隆到本地：

```bash
git clone https://github.com/intsig-textin/chatdoc_stack.git
cd chatdoc_stack
```

### 步骤 2: 🔑︎配置 API Key

1. **TextIn API Key 和 Secret Key：**
- 登录[TextIn工作台](https://www.textin.com/console/dashboard/setting)，获取API Key和Secret Key
- 将API Key和Secret Key填入到`compose/docker-compose.yml`文件中相应位置，涉及到`chatdoc-proxy`、`chatdoc`、`backend`三个服务
  ```docker-compose.yml
    - TEXTIN_APP_ID=your_textin_app_id
    - TEXTIN_APP_SECRET=your_textin_app_secret
  ```

2. **如果使用通义千问 API：**
- 注册[通义千问](https://bailian.console.aliyun.com/)，获取千问api的key
- 将千问api的key填入到`compose/docker-compose.yml`文件中相应位置，涉及到`chatdoc-proxy`、`chatdoc`两个服务
  ```docker-compose.yml
    - TYQWAPI_API_KEY=your_tyqwan_api_key
  ```

3. **如果使用其他大模型 API：**
- 如果是在线大模型，需要获取大模型的API Key；如果是本地大模型，需要自行搭建
- 将大模型配置填入到`compose/docker-compose.yml`文件中相应位置，涉及到`chatdoc-proxy`、`chatdoc`两个服务
  ```docker-compose.yml
    # - LLM_MODEL=tyqwapi
    # - TYQWAPI_MODEL=deepseek-v3
    # - TYQWAPI_API_KEY=sk-xxx
    - LLM_MODEL=deepseek
    - DEEPSEEK_URL=your_url
    - DEEPSEEK_MODEL=deepseek-r1
    - DEEPSEEK_API_KEY=your_api_key
  ```


### 步骤 3: 启动服务

1. **设置 Elasticsearch 路径权限：**
   - 运行以下命令以确保 Elasticsearch 启动不报错：
    ```
    sudo sysctl -w vm.max_map_count=262144
    ```

2. **启动服务：**
   - 运行以下命令启动服务：
    ```bash
    cd compose
    chmod +x initialize.sh
    ./initialize.sh all
    ```
    - 如果需要跨机器访问，请修改 docker-compose.yml 文件中的 KB_API 地址为后端暴露的公网地址。
    - 初始化服务后，修改配置，运行命令 compose/start.sh 即可

### 步骤 4: 🔍︎访问服务

1. **访问前端**
   - 访问 http://localhost:48091 前端地址访问界面，使用默认用户名密码 admin/admin

2. **个人知识库上传文件测试**
   - 使用默认用户名密码 admin/admin 登录后，点击左侧菜单栏的“个人知识库”，上传文件进行测试
   - 如果需要排查日志，可以使用 docker logs 命令查询
    ```
    docker logs -f <container_name>
    ```

### 步骤 5: 修改其他配置

直接修改 docker-compose.yml 中的对应配置，然后运行命令 compose/start.sh 即可

## TextIn替换方案

本项目提供了一个完整的TextIn服务替换方案。TextIn服务主要提供三个功能：文档解析（PDF2MD）、文本嵌入（acge_embedding）和重排序（rerank）。本替换方案通过扩展`custom-parser`服务，集成多种解析引擎和API，实现了对TextIn服务的全面替代。

### 主要组件

#### 1. 多引擎文档解析服务

扩展了`custom-parser`服务，集成了多种文档解析引擎：

- **MegaParse**: 主要解析引擎，提供高质量文档解析
- **LlamaParse**: 备选解析引擎，需要LlamaCloud API密钥
- **通义千问**: 备选解析引擎，需要通义千问API密钥
- **Mock**: 模拟解析器，用于测试和开发

支持多种解析策略（Auto、Fast、Hi-Res）和文件类型（PDF、DOCX、DOC、TXT、MD）。

**API兼容性：**

服务完全兼容TextIn PDF2MD API，支持两种方式上传文件：

1. 标准方式：通过multipart/form-data上传文件
2. 兼容TextIn API方式：直接将文件内容作为请求体发送

这使得ChatDoc服务可以无缝集成，无需修改代码。

#### 2. 文本嵌入服务

提供两种文本嵌入方案：

- **Sentence Transformers**: 开源的文本嵌入模型，如'all-MiniLM-L6-v2'
- **通义千问API**: 通过通义千问API提供的文本嵌入功能

#### 3. 重排序服务

提供两种重排序方案：

- **Cohere API**: 使用Cohere提供的免费重排序API
- **本地重排序模型**: 部署本地重排序模型

### 安装与配置

#### 安装依赖

##### Windows

```powershell
# 运行PowerShell安装脚本
.\setup_parser.ps1
```

##### Linux/Mac

```bash
# 运行Bash安装脚本
chmod +x setup_parser.sh
./setup_parser.sh
```

#### 配置环境变量

在`custom-parser/.env`文件中配置以下选项：

```
DEFAULT_PARSER=megaparse  # 默认解析器类型
MEGAPARSE_ENABLED=true    # 是否启用MegaParse
LLAMA_CLOUD_API_KEY=your_key  # LlamaCloud API密钥
QWEN_API_KEY=your_key     # 通义千问API密钥
PORT=8080                 # 服务端口
TEMP_DIR=./temp           # 临时文件目录
LOG_LEVEL=info            # 日志级别
```

#### 启动服务

##### 直接启动

```bash
cd custom-parser
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

##### 使用Docker

```bash
docker-compose up -d custom-parser
```

#### 测试

##### 测试解析服务

```bash
# 测试所有解析器
python test_multi_parser.py path/to/document.pdf --all

# 测试特定解析器
python test_multi_parser.py path/to/document.pdf --parser megaparse
```

##### 测试与ChatDoc集成

```bash
python test_integration.py path/to/document.pdf
```

#### 与ChatDoc集成

1. 修改ChatDoc配置，将TextIn相关API指向新服务：

```yaml
# 在docker-compose.yml中修改环境变量
services:
  chatdoc:
    environment:
      - PDF2MD_API_URL=http://custom-parser:8080/api/v1/pdf_to_markdown
      - EMBEDDING_API_URL=http://custom-parser:8080/api/v1/embedding
      - RERANK_API_URL=http://custom-parser:8080/api/v1/rerank
```

2. 重启ChatDoc服务：

```bash
docker-compose restart chatdoc
```

## 注意事项
- 除 `question-analysis`镜像外，您可以使用代码仓库中各模块的 `Dockerfile` 文件自行构建镜像。
- 如果需要跨机器访问，请修改 `docker-compose.yml` 文件中的 `frontend` 服务中的 `KB_API` 地址为后端暴露的公网地址。


## 贡献指南
欢迎贡献代码！在开始之前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 以了解贡献流程和指南。

## 许可证
此项目基于 [CC-NC License](LICENSE) 进行许可。