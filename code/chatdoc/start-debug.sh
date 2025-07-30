#!/bin/bash

echo "Starting ChatDoc in Debug Mode..."
echo

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python version: $($PYTHON_CMD --version)"

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=1
export PYTHONPATH=.
export PYTHONDONTWRITEBYTECODE=1

# 加载本地环境变量
if [ -f .env.local ]; then
    echo "Loading environment variables from .env.local..."
    export $(grep -v '^#' .env.local | xargs)
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# 激活虚拟环境
echo "Activating virtual environment..."
source venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# 安装调试工具
pip install debugpy

# 创建数据目录
mkdir -p data/file
mkdir -p parse/doc-paser
mkdir -p parse/catalog

# 启动调试模式
echo
echo "Starting ChatDoc in debug mode..."
echo "Service will be available at: http://localhost:5000"
echo "Debug port: 5678"
echo
echo "You can set breakpoints in your Python IDE and attach debugger"
echo

python -m debugpy --listen 5678 --wait-for-client main.py
