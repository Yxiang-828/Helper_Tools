@echo off
echo 🎬 Advanced MP4 to GIF Converter
echo =================================
echo.
echo This script runs the advanced GIF converter with custom constraints.
echo.
echo Usage: advanced_converter.bat
echo.
echo The script will prompt you for:
echo - MP4 video file path
echo - Size limit in MB (e.g., 10)
echo - Speed ratio (1.0 = original speed)
echo.
echo Press any key to start...
pause > nul

cd /d "%~dp0"
py ./"mp4 to gif converter"/converter.py

echo.
echo Conversion complete! Press any key to exit...
pause > nul