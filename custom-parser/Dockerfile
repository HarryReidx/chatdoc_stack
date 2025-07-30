FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建临时目录
RUN mkdir -p /app/temp

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 如果MegaParse库在项目目录中，则安装它
COPY MegaParse/libs/megaparse /app/MegaParse/libs/megaparse
COPY MegaParse/libs/megaparse_sdk /app/MegaParse/libs/megaparse_sdk
RUN if [ -d "/app/MegaParse/libs/megaparse" ]; then \
    pip install -e /app/MegaParse/libs/megaparse; \
    fi
RUN if [ -d "/app/MegaParse/libs/megaparse_sdk" ]; then \
    pip install -e /app/MegaParse/libs/megaparse_sdk; \
    fi

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
