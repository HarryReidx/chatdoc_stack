@echo off
chcp 65001 >nul
echo Starting ChatDoc in Local Debug Mode...
echo.

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Python version:
python --version

REM 设置环境变量
set BASE_PATH=config.local.yaml
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=.
set PYTHONDONTWRITEBYTECODE=1

echo.
echo Environment variables set:
echo BASE_PATH=%BASE_PATH%
echo FLASK_ENV=%FLASK_ENV%
echo PYTHONPATH=%PYTHONPATH%

REM 检查虚拟环境
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM 安装调试工具
echo Installing debugpy...
pip install debugpy
if %errorlevel% neq 0 (
    echo Warning: Failed to install debugpy, continuing without remote debugging
)

REM 创建必要的目录
echo.
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "data\file" mkdir data\file
if not exist "parse" mkdir parse
if not exist "parse\doc-paser" mkdir parse\doc-paser
if not exist "parse\catalog" mkdir parse\catalog

REM 检查配置文件
if not exist "config.local.yaml" (
    echo Warning: config.local.yaml not found, using default config.yaml
    set BASE_PATH=config.yaml
)

REM 启动Flask应用
echo.
echo Starting ChatDoc...
echo Service will be available at: http://localhost:5000
echo Press Ctrl+C to stop the service
echo.

python main.py

echo.
echo ChatDoc stopped.
pause
