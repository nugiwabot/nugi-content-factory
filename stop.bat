@echo off
setlocal enabledelayedexpansion
title Nugi Content Factory - Stopper

echo ===================================================
echo   NUGI CONTENT FACTORY - STOP PROCESS
echo ===================================================
echo.

cd /d "%~dp0"

set "FOUND=0"

rem 1. Kill process listening on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set "TARGET_PID=%%a"
    if defined TARGET_PID (
        set "FOUND=1"
        echo [INFO] Menghentikan proses server PID !TARGET_PID! pada port 8000...
        taskkill /F /PID !TARGET_PID! >nul 2>&1
    )
)

rem 2. Also close any window titled Nugi Content Factory Server
taskkill /F /FI "WINDOWTITLE eq Nugi Content Factory Server*" >nul 2>&1

rem 3. Verify port 8000 is released
ping 127.0.0.1 -n 2 >nul
netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Port 8000 masih digunakan oleh proses lain.
) else (
    if "!FOUND!"=="1" (
        echo [BERHASIL] Server Nugi Content Factory telah dihentikan.
        echo [BERHASIL] Port 8000 telah dilepaskan dengan bersih.
    ) else (
        echo [INFO] Tidak ada server Nugi Content Factory yang sedang berjalan di port 8000.
    )
)

echo.
ping 127.0.0.1 -n 3 >nul
exit /b 0
