@echo off
title Nugi Content Factory - Disable Windows Startup
cd /d "%~dp0"

echo ===================================================
echo   Nonaktifkan Autorun Saat Windows Boot / Startup
echo ===================================================
echo.

set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NugiContentFactory.lnk"

if exist "%SHORTCUT_PATH%" (
    del /f /q "%SHORTCUT_PATH%"
    echo [BERHASIL] Autorun saat Windows boot telah dinonaktifkan.
) else (
    echo [INFO] Shortcut autorun tidak ditemukan atau sudah dinonaktifkan sebelumnya.
)

echo.
pause
