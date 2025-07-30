@echo off
echo Starting ChatDoc in Debug Mode...
echo.

REM 检查Python版本
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
python -c "import sys; print('Virtual environment:', hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))"

REM 设置环境变量
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=.
set PYTHONDONTWRITEBYTECODE=1

REM 设置基本环境变量
set BASE_PATH=config.local.yaml
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=.
set PYTHONDONTWRITEBYTECODE=1

REM 检查虚拟环境
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM 激活虚拟环境
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM 安装依赖
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM 创建数据目录
if not exist "data" mkdir data
if not exist "data\file" mkdir data\file
if not exist "parse" mkdir parse
if not exist "parse\doc-paser" mkdir parse\doc-paser
if not exist "parse\catalog" mkdir parse\catalog

REM 启动调试模式
echo.
echo Starting ChatDoc in debug mode...
echo Service will be available at: http://localhost:5000
echo.
echo You can set breakpoints in your Python IDE and attach debugger
echo.

python -m debugpy --listen 5678 --wait-for-client main.py

pause
