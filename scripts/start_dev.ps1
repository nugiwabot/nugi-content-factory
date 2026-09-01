# ==============================================================================
# NUGI CONTENT FACTORY - LOCAL DEVELOPMENT STARTER
# ==============================================================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Starting Nugi Content Factory Development Servers" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$RootPath = (Get-Item -Path $PSScriptRoot\..).FullName
$BackendPath = Join-Path $RootPath "backend"
$FrontendPath = Join-Path $RootPath "frontend"

Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
$BackendProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -WorkingDirectory $BackendPath -PassThru

Write-Host "[2/2] Starting Vite React Frontend on http://localhost:5173..." -ForegroundColor Yellow
$FrontendProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory $FrontendPath -PassThru

Write-Host "`n✔ Development servers launched successfully!" -ForegroundColor Green
Write-Host "• Frontend UI: http://localhost:5173" -ForegroundColor White
Write-Host "• Backend API: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "• Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "`nTekan CTRL+C atau tutup jendela PowerShell untuk menghentikan proses." -ForegroundColor Gray
