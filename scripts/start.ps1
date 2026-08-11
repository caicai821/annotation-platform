# 一键启动数据标注平台（后端 + 前端）
# 双击 scripts\start.bat 或在 PowerShell 中执行 scripts\start.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

Write-Host "===== 启动数据标注平台 =====" -ForegroundColor Cyan

# 1. 后端：首次自动创建虚拟环境
if (-not (Test-Path (Join-Path $backend ".venv"))) {
    Write-Host "[1/4] 首次启动，正在创建后端虚拟环境..." -ForegroundColor Cyan
    python -m venv (Join-Path $backend ".venv")
    if ($LASTEXITCODE -ne 0) { Write-Host "创建虚拟环境失败，请确认已安装 Python 并加入 PATH" -ForegroundColor Red; exit 1 }
}
$pip = Join-Path $backend ".venv\Scripts\pip.exe"

# 2. 后端依赖与 .env（已装好时秒过）
Write-Host "[2/4] 检查后端依赖..." -ForegroundColor Cyan
& $pip install -r (Join-Path $backend "requirements.txt") -q
if (-not (Test-Path (Join-Path $backend ".env"))) {
    Copy-Item (Join-Path $backend ".env.example") (Join-Path $backend ".env")
}

# 3. 前端：首次自动安装依赖
Write-Host "[3/4] 检查前端依赖..." -ForegroundColor Cyan
if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Push-Location $frontend
    npm install
    Pop-Location
}

# 4. 启动：后端开新窗口，前端在当前窗口
Write-Host "[4/4] 启动服务..." -ForegroundColor Cyan
$uvicorn = Join-Path $backend ".venv\Scripts\uvicorn.exe"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backend'; & '$uvicorn' app.main:app --reload --port 8000"

Write-Host "后端已在新窗口启动：http://localhost:8000/docs" -ForegroundColor Green
Write-Host "前端正在启动：http://localhost:5173 （Ctrl+C 可停止）" -ForegroundColor Green
Push-Location $frontend
npm run dev
Pop-Location