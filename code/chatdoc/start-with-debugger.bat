@echo off
chcp 65001 >nul
echo Starting ChatDoc with Remote Debugger...
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

REM 激活虚拟环境（如果存在）
if exist "venv\Scripts\activate.bat" (
    echo.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM 检查debugpy是否安装
python -c "import debugpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing debugpy...
    pip install debugpy
    if %errorlevel% neq 0 (
        echo Error: Failed to install debugpy
        pause
        exit /b 1
    )
)

REM 创建必要的目录
if not exist "data" mkdir data
if not exist "data\file" mkdir data\file
if not exist "parse" mkdir parse
if not exist "parse\doc-paser" mkdir parse\doc-paser
if not exist "parse\catalog" mkdir parse\catalog

REM 启动带调试器的Flask应用
echo.
echo Starting ChatDoc with debugger...
echo Service will be available at: http://localhost:5000
echo Debug port: 5678
echo.
echo Waiting for debugger to attach...
echo In VS Code, use "Attach to ChatDoc" configuration
echo.

python -m debugpy --listen 5678 --wait-for-client main.py

echo.
echo ChatDoc stopped.
pause
