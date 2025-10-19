@echo off
echo 🎬 Frame to Video/GIF Converter
echo ================================
echo.
echo This tool combines image frames from a folder into MP4 or GIF files.
echo Supports PNG, JPG, JPEG, BMP, TIFF formats.
echo Uses GPU acceleration for MP4 creation.
echo.
echo Usage: frame_to_video.bat
echo.
echo The script will prompt you for:
echo - Folder containing image frames
echo - Output format (MP4 or GIF)
echo - Timing mode (FPS or Duration per frame)
echo - Timing value with helpful tips
echo.
echo Press any key to start...
pause > nul

cd /d "%~dp0Frame_to_Video_Converter"
py frame_to_video.py

echo.
echo Conversion complete! Press any key to exit...
pause > nul