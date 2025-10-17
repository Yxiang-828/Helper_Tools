@echo off
REM Video Upscaler Batch File
REM Uses py command for Python execution

@echo off
REM Video Upscaler Batch File
REM Uses py command for Python execution

echo DEBUG: First arg is: "%~1"
if "%~1"=="" (
    echo ========================================
    echo AMD GPU Video Upscaler Tool
    echo ========================================
    echo.
    echo Usage: video_upscaler.bat ^<input_video^> [options]
    echo.
    echo Methods:
    echo   ffmpeg     = Fast Lanczos upscaling with AMD VCE hardware encoding
    echo   realesrgan = AI anime upscaling, processes each frame individually
    echo   extract    = Extract frames only, no upscaling
    echo   process_existing = Upscale already extracted frames
    echo.
    echo Options:
    echo   --scale {2^|3^|4}     Upscale factor (default: 4)
    echo   --method {ffmpeg^|realesrgan^|extract^|process_existing}  Method
    echo   --format {mp4^|gif}   Output format (default: mp4)
    echo.
    echo Examples:
    echo   video_upscaler.bat "input\myvideo.mp4"
    echo   video_upscaler.bat "input\myvideo.mp4" --method realesrgan --scale 4 --format gif
    echo.
    pause
    exit /b 1
)

echo ========================================
echo AMD GPU Video Upscaler Tool
echo ========================================
echo.

REM Run the Python script with all arguments
py video_upscaler\video_upscaler.py %*

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Video upscaling failed with exit code %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo SUCCESS: Video upscaling completed!
echo ========================================
pause