@echo off
echo Starting ChatDoc in Simple Debug Mode...
echo.

REM 设置环境变量
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=.
set BASE_PATH=config.local.yaml

REM 激活虚拟环境（如果存在）
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM 启动Flask应用
echo Starting ChatDoc...
echo Service will be available at: http://localhost:5000
echo.

python main.py

pause
