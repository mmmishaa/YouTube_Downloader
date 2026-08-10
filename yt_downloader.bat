@echo off
setlocal enabledelayedexpansion

echo =====================================================
echo                  YouTube Downloader                    
echo =====================================================
echo.

echo [*] Checking and installing Python dependencies...
echo.
pip install -qq -r requirements.txt --upgrade

if %errorlevel% neq 0 (
    echo.
    echo [!] Error: Failed to install requirements.
    pause
    exit /b
)

if not exist "ffmpeg" (
    echo [*] Extracting ffmpeg.zip...
    powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg' -Force"
    echo [+] FFmpeg extraction complete.
    echo [*] Deleting ffmpeg.zip...
    del /f /q "ffmpeg.zip"
) else (
    echo [i] FFmpeg is already extracted.
)
echo.

if not exist "deno" (
    echo [*] Extracting deno.zip...
    powershell -Command "Expand-Archive -Path 'deno.zip' -DestinationPath 'deno' -Force"
    echo [+] Deno extraction complete.
    echo [*] Deleting deno.zip...
    del /f /q "deno.zip"
) else (
    echo [i] Deno is already extracted.
)
echo.

:DOWNLOAD_LOOP

echo [*] Starting yt_downloader.py...

echo.

python -W ignore yt_downloader.py

echo.

choice /C YN /M "Download another video? (Y - Yes, N - Exit)"

if errorlevel 2 goto EXIT_SCRIPT
if errorlevel 1 goto RESTART_LOOP

:RESTART_LOOP
echo.
echo.
goto DOWNLOAD_LOOP

:EXIT_SCRIPT
echo.
exit /b