@echo off
setlocal enabledelayedexpansion
title Nugi Content Factory - Starter

echo ===================================================
echo   NUGI CONTENT FACTORY - AUTORUN LAUNCHER
echo ===================================================
echo.

cd /d "%~dp0"

rem 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak ditemukan di PATH sistem.
    echo Pastikan Python 3.11+ telah terinstall dan ditambahkan ke PATH.
    pause
    exit /b 1
)

rem 2. Check if already running on port 8000
set "RUNNING_PID="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set "RUNNING_PID=%%a"
)

if defined RUNNING_PID (
    echo [INFO] Nugi Content Factory SUDAH BERJALAN pada PID !RUNNING_PID! di port 8000.
    echo [INFO] Membuka browser ke http://127.0.0.1:8000 ...
    start http://127.0.0.1:8000
    ping 127.0.0.1 -n 3 >nul
    exit /b 0
)

rem 3. Launch FastAPI backend
echo [1/2] Menjalankan server backend FastAPI...
cd /d "%~dp0backend"
start "Nugi Content Factory Server" python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
cd /d "%~dp0"

rem 4. Wait for server readiness (up to 15 seconds)
echo [2/2] Menunggu server siap...
set "SERVER_READY=0"
for /l %%i in (1,1,15) do (
    ping 127.0.0.1 -n 2 >nul
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
        set "SERVER_READY=1"
    )
    if "!SERVER_READY!"=="1" goto :server_up
)

:server_up
if "!SERVER_READY!"=="1" (
    echo.
    echo ===================================================
    echo   [BERHASIL] Nugi Content Factory aktif!
    echo   URL: http://127.0.0.1:8000
    echo ===================================================
    echo.
    echo Membuka aplikasi di browser...
    start http://127.0.0.1:8000
    ping 127.0.0.1 -n 3 >nul
) else (
    echo.
    echo [WARNING] Server membutuhkan waktu lebih lama untuk start.
    echo Membuka browser: http://127.0.0.1:8000 ...
    start http://127.0.0.1:8000
)

exit /b 0
