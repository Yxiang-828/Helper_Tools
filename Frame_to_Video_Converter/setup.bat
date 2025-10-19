@echo off
REM Frame to Video/GIF Converter Setup Script
REM Installs required Python packages for frame conversion

echo ============================================
echo  FRAME TO VIDEO/GIF CONVERTER SETUP
echo ============================================
echo.
echo This setup installs the required dependencies:
echo - OpenCV (with GPU acceleration support)
echo - PIL/Pillow (usually already included)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Installing OpenCV with GPU support...
echo.

pip install opencv-python

echo.
echo Setup complete! You can now use the converter.
echo.
echo Run: frame_to_video.bat
echo.
pause