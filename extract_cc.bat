@echo off
echo 🎬 Closed Caption Extractor for MP4/MOV Videos
echo ===============================================
echo.
echo Checking FFmpeg installation...
echo.

"C:\ffmpeg\bin\ffmpeg.exe" -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg is required but not found!
    echo.
    echo Please install FFmpeg:
    echo 1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    echo 2. Extract to C:\ffmpeg\
    echo 3. Add C:\ffmpeg\bin to PATH, or place ffmpeg.exe in C:\ffmpeg\bin\
    echo.
    echo Run 'check_ffmpeg.bat' to verify installation.
    echo.
    pause
    exit /b 1
)

echo ✅ FFmpeg found! Proceeding with extraction...
echo.

if "%~1"=="" (
    echo ❌ Error: No video file specified
    echo.
    echo Usage: extract_cc.bat "path\to\video.mp4" [output_directory]
    pause
    exit /b 1
)

py "Video-subtitle&mp3-extractor/cc_extractor.py" %*

echo.
echo ===============================================
echo Extraction complete!
if %errorlevel% neq 0 (
    echo Press any key to exit...
    pause > nul
)