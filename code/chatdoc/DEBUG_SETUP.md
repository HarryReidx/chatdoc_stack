# ChatDoc本地调试配置指南

## 概述

本配置允许您在本地运行ChatDoc服务进行Python调试，而其他服务（MySQL、Redis、ES、Backend等）继续在Docker容器中运行。

## 前置条件

1. **Python**: 版本 >= 3.9
2. **pip**: Python包管理器
3. **Docker**: 用于运行其他服务
4. **IDE**: 推荐使用VS Code + Python扩展

## 启动步骤

### 1. 启动Docker服务

首先启动除ChatDoc外的所有服务：

```bash
cd compose
docker-compose up -d
```

这将启动：
- MySQL (端口: 3307)
- Redis (端口: 6379) 
- ElasticSearch (端口: 9200)
- ChatDoc-Proxy (端口: 8000)
- Frontend (端口: 48091)
- Custom-Parser (端口: 8080)
- Query-Analysis (端口: 30006)

### 2. 启动ChatDoc调试模式

#### 方法一：使用启动脚本（推荐）

**Windows:**
```cmd
cd code/chatdoc
start-debug.bat
```

**Linux/Mac:**
```bash
cd code/chatdoc
chmod +x start-debug.sh
./start-debug.sh
```

#### 方法二：简单启动（不等待调试器）

```cmd
cd code/chatdoc
start-simple.bat
```

#### 方法三：手动启动

```bash
cd code/chatdoc

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install debugpy

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=1
export PYTHONPATH=.
export BASE_PATH=config.local.yaml

# 启动调试模式
python -m debugpy --listen 5678 --wait-for-client main.py
```

### 3. VS Code调试

#### 直接启动调试：
1. 在VS Code中打开 `code/chatdoc` 目录
2. 按 `F5` 或使用调试面板选择 "Debug ChatDoc"
3. 设置断点并开始调试

#### 附加到已运行的进程：
1. 先手动启动ChatDoc: `start-debug.bat`
2. 在VS Code中选择 "Attach to ChatDoc" 配置
3. 按 `F5` 附加调试器

## 调试端口和地址

- **ChatDoc服务**: http://localhost:5000
- **调试端口**: 5678 (用于debugpy连接)
- **API端点**:
  - 分析师文档解析: `POST /api/v1/analyst/parse`
  - 个人文档解析: `POST /api/v1/personal/parse`
  - 分析师推理: `POST /api/v1/analyst/infer`
  - 个人推理: `POST /api/v1/personal/infer`
  - 全局推理: `POST /api/v1/global/infer`

## 环境配置

### 配置文件
- `config.local.yaml`: 主配置文件，连接到Docker服务
- `.env.local`: 环境变量配置

### 关键配置项
```yaml
# 连接到Docker中的服务
es:
  hosts: 'http://127.0.0.1:9200'
  password: 'Pwd_250309'

redis:
  host: "127.0.0.1"
  port: 6379
  password: 'Pwd_250309'

proxy:
  url: http://127.0.0.1:8000

backend:
  node_url: 'http://127.0.0.1:3000'
```

## 常见问题

### 1. Python依赖安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 如果某些包安装失败，可以尝试：
pip install --no-cache-dir -r requirements.txt
```

### 2. 连接Docker服务失败
- 确保Docker服务已启动: `docker-compose ps`
- 检查端口是否正确映射
- 验证防火墙设置

### 3. 调试器无法连接
- 确保使用debugpy启动: `python -m debugpy --listen 5678 --wait-for-client main.py`
- 检查端口5678是否被占用
- 重启VS Code和调试进程

### 4. 配置文件路径问题
- 确保 `BASE_PATH=config.local.yaml` 环境变量设置正确
- 检查配置文件是否存在

## 开发工作流

1. **修改代码**: 在VS Code中编辑Python代码
2. **设置断点**: 在需要调试的行设置断点
3. **发送请求**: 通过前端或API工具发送请求到ChatDoc
4. **调试**: 在断点处检查变量、调用栈等
5. **热重载**: Flask开发模式支持代码修改后自动重启

## API测试

可以使用以下工具测试ChatDoc API：

### 使用curl测试
```bash
# 测试个人推理接口
curl -X POST http://localhost:5000/api/v1/personal/infer \
  -H "Content-Type: application/json" \
  -d '{
    "question": "测试问题",
    "user_id": "test_user",
    "file_uuids": []
  }'
```

### 使用Postman
导入以下请求到Postman：
- URL: `http://localhost:5000/api/v1/personal/infer`
- Method: POST
- Headers: `Content-Type: application/json`
- Body: JSON格式的请求参数

## 性能优化

- 使用虚拟环境隔离依赖
- 启用Flask调试模式获得详细错误信息
- 使用debugpy进行高效调试
- 配置合适的日志级别

## 停止服务

```bash
# 停止ChatDoc
Ctrl+C

# 停止Docker服务
cd compose
docker-compose down
```

## 日志查看

ChatDoc的日志会输出到控制台，包括：
- 请求日志
- 错误信息
- 调试信息
- 性能指标

在调试模式下，所有日志都会显示在VS Code的集成终端中。
