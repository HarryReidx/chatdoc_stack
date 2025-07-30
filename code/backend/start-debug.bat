@echo off
echo Starting Backend in Debug Mode...
echo.

REM 检查Node.js版本
node --version
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM 检查npm是否安装
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: npm is not installed or not in PATH
    pause
    exit /b 1
)

REM 检查yarn是否安装
yarn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Yarn not found, using npm instead...
    set PACKAGE_MANAGER=npm
) else (
    echo Using yarn...
    set PACKAGE_MANAGER=yarn
)

REM 安装依赖
echo Installing dependencies...
if "%PACKAGE_MANAGER%"=="yarn" (
    yarn install
) else (
    npm install
)

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM 运行数据库迁移
echo Running database migrations...
if "%PACKAGE_MANAGER%"=="yarn" (
    yarn migration:run
) else (
    npm run migration:run
)

REM 启动调试模式
echo.
echo Starting in debug mode...
echo You can now attach your debugger to port 9229
echo.
if "%PACKAGE_MANAGER%"=="yarn" (
    yarn start:debug
) else (
    npm run start:debug
)

pause
