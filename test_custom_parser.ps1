# ChatDoc 自定义解析服务测试脚本 (PowerShell)

Write-Host "🚀 开始测试自定义文档解析服务..." -ForegroundColor Blue

# 检查 Docker 是否运行
try {
    docker info | Out-Null
    Write-Host "✅ Docker 运行正常" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker 未运行，请先启动 Docker" -ForegroundColor Red
    exit 1
}

Write-Host "📋 步骤1: 构建自定义解析服务..." -ForegroundColor Blue
Set-Location compose
docker-compose build custom-parser

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 自定义解析服务构建成功" -ForegroundColor Green
} else {
    Write-Host "❌ 自定义解析服务构建失败" -ForegroundColor Red
    exit 1
}

Write-Host "📋 步骤2: 启动自定义解析服务..." -ForegroundColor Blue
docker-compose up -d custom-parser

Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep 15

Write-Host "📋 步骤3: 检查服务状态..." -ForegroundColor Blue
docker-compose ps custom-parser

Write-Host "📋 步骤4: 重启 chatdoc 服务..." -ForegroundColor Blue
docker-compose restart chatdoc

Write-Host "🎉 部署完成！" -ForegroundColor Green
Write-Host "📋 下一步: 访问 http://localhost:48091 测试文档上传功能" -ForegroundColor Yellow
