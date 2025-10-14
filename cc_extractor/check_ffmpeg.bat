@echo off
echo 🎬 Closed Caption Extractor - FFmpeg Check
echo ===========================================
echo.
echo Checking if FFmpeg is installed...
echo.

ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg is NOT installed or not in PATH
    echo.
    echo To install FFmpeg:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    echo 2. Extract to C:\ffmpeg\
    echo 3. Add C:\ffmpeg\bin to your system PATH
    echo 4. Or place ffmpeg.exe in: C:\ffmpeg\bin\ffmpeg.exe
    echo.
    echo After installation, run this batch file again.
) else (
    echo ✅ FFmpeg is installed and working!
    echo.
    echo You can now use the CC extractor:
    echo extract_cc.bat "path\to\video.mp4"
)

echo.
pause