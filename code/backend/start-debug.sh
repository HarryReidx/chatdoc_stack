#!/bin/bash

echo "Starting Backend in Debug Mode..."
echo

# 检查Node.js版本
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed or not in PATH"
    exit 1
fi

echo "Node.js version: $(node --version)"

# 检查包管理器
if command -v yarn &> /dev/null; then
    echo "Using yarn..."
    PACKAGE_MANAGER="yarn"
else
    echo "Yarn not found, using npm instead..."
    PACKAGE_MANAGER="npm"
fi

# 安装依赖
echo "Installing dependencies..."
if [ "$PACKAGE_MANAGER" = "yarn" ]; then
    yarn install
else
    npm install
fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# 运行数据库迁移
echo "Running database migrations..."
if [ "$PACKAGE_MANAGER" = "yarn" ]; then
    yarn migration:run
else
    npm run migration:run
fi

# 启动调试模式
echo
echo "Starting in debug mode..."
echo "You can now attach your debugger to port 9229"
echo

if [ "$PACKAGE_MANAGER" = "yarn" ]; then
    yarn start:debug
else
    npm run start:debug
fi
