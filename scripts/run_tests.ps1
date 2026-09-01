# ==============================================================================
# NUGI CONTENT FACTORY - AUTOMATED TEST SUITE RUNNER
# ==============================================================================

Write-Host "Running Backend Automated Test Suite..." -ForegroundColor Cyan

$BackendPath = Join-Path (Get-Item -Path $PSScriptRoot\..).FullName "backend"
Set-Location $BackendPath

python -m pytest -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✔ ALL TESTS PASSED SUCCESSFULLY!" -ForegroundColor Green
} else {
    Write-Host "`n❌ TEST SUITE FAILED." -ForegroundColor Red
}
