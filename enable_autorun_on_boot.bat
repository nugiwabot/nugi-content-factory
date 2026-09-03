@echo off
title Nugi Content Factory - Enable Windows Startup
cd /d "%~dp0"

echo ===================================================
echo   Aktifkan Autorun Saat Windows Boot / Startup
echo ===================================================
echo.

set "TARGET_BAT=%~dp0start.bat"
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NugiContentFactory.lnk"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_BAT%'; $s.WorkingDirectory = '%~dp0'; $s.WindowStyle = 7; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo [BERHASIL] Autorun saat Windows boot berhasil diaktifkan!
    echo Shortcut tersimpan di:
    echo %SHORTCUT_PATH%
    echo.
    echo Aplikasi akan otomatis berjalan setiap kali komputer dinyalakan.
) else (
    echo [ERROR] Gagal membuat shortcut startup.
)

echo.
pause
