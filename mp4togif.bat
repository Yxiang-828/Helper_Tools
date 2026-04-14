@echo off
echo 🎬 Advanced MP4 to GIF Converter
echo =================================
echo.
echo This script runs the advanced GIF converter with custom constraints.
echo.
echo Usage:
echo   mp4togif.bat [video_file] [size_mb] [speed_ratio]
echo.
echo Parameters:
echo   video_file  - Path to MP4 video file (optional - will prompt if not provided)
echo   size_mb     - Size limit in MB (optional - will prompt if not provided)
echo   speed_ratio - Speed ratio (1.0 = original speed) (optional - will prompt if not provided)
echo.
echo Examples:
echo   mp4togif.bat
echo   mp4togif.bat "C:\path\to\video.mp4" 10 2.0
echo   mp4togif.bat "video.mp4" 5 0.5
echo.

cd /d "%~dp0"

REM Check if arguments were provided
if "%~1"=="" (
    echo No arguments provided. Running in interactive mode...
    python "Video_to_GIF_Converter/converter.py"
) else (
    echo Running with provided arguments...
    python "Video_to_GIF_Converter/converter.py" "%~1" -s %2 -p %3
)

echo.
echo Conversion complete! Press any key to exit...
pause > nul