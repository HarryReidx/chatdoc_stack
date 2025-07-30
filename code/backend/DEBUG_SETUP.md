# Backend本地调试配置指南

## 概述

本配置允许您在本地运行backend服务进行调试，而其他服务（MySQL、Redis、ES、ChatDoc等）继续在Docker容器中运行。

## 前置条件

1. **Node.js**: 版本 >= 18
2. **包管理器**: yarn 或 npm
3. **Docker**: 用于运行其他服务
4. **IDE**: 推荐使用VS Code

## 启动步骤

### 1. 启动Docker服务

首先启动除backend外的所有服务：

```bash
cd compose
docker-compose up -d
```

这将启动：
- MySQL (端口: 3307)
- Redis (端口: 6379) 
- ElasticSearch (端口: 9200)
- ChatDoc服务 (端口: 5000)
- ChatDoc-Proxy (端口: 8000)
- Frontend (端口: 48091)
- Custom-Parser (端口: 8080)

### 2. 启动Backend调试模式

#### 方法一：使用启动脚本

**Windows:**
```cmd
cd code/backend
start-debug.bat
```

**Linux/Mac:**
```bash
cd code/backend
chmod +x start-debug.sh
./start-debug.sh
```

#### 方法二：手动启动

```bash
cd code/backend

# 安装依赖
yarn install

# 运行数据库迁移
yarn migration:run

# 启动调试模式
yarn start:debug
```

### 3. VS Code调试

1. 在VS Code中打开 `code/backend` 目录
2. 按 `F5` 或使用调试面板选择 "Debug Backend"
3. 设置断点并开始调试

#### 或者附加到已运行的进程：

1. 先手动启动backend: `yarn start:debug`
2. 在VS Code中选择 "Attach to Backend" 配置
3. 按 `F5` 附加调试器

## 调试端口

- **Backend服务**: http://localhost:3000
- **调试端口**: 9229 (用于调试器连接)
- **Swagger文档**: http://localhost:3000/api

## 环境配置

环境变量配置在 `.env.development` 文件中：

```env
# 数据库连接到Docker MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_PASSWORD=Pwd_250309

# Redis连接到Docker Redis  
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=Pwd_250309

# 其他服务地址
CHATDOC_PROXY_URL=http://127.0.0.1:8000
BACKEND_URL=http://127.0.0.1:5000
```

## 常见问题

### 1. 数据库连接失败
- 确保Docker中的MySQL服务已启动
- 检查端口3307是否被占用
- 验证密码是否正确

### 2. Redis连接失败
- 确保Docker中的Redis服务已启动
- 检查端口6379是否被占用

### 3. 调试器无法连接
- 确保使用 `yarn start:debug` 启动
- 检查端口9229是否被占用
- 重启VS Code和调试进程

### 4. 前端无法访问后端
- 确保backend在端口3000运行
- 检查CORS配置是否正确

## 开发工作流

1. **修改代码**: 在VS Code中编辑代码
2. **设置断点**: 在需要调试的行设置断点
3. **触发请求**: 通过前端或API工具发送请求
4. **调试**: 在断点处检查变量、调用栈等
5. **热重载**: 代码修改后自动重启（watch模式）

## 性能优化

- 使用 `--inspect` 而不是 `--inspect-brk` 避免启动时暂停
- 启用source maps以便调试TypeScript代码
- 使用 `--nolazy` 提高调试性能

## 停止服务

```bash
# 停止backend
Ctrl+C

# 停止Docker服务
cd compose
docker-compose down
```
