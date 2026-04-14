@echo off
REM Background Remover Setup Script
REM Installs required Python packages for background removal

echo ============================================
echo   BACKGROUND REMOVER SETUP
echo ============================================
echo.
echo This setup installs the required dependencies:
echo - rembg (AI Background Removal)
echo - Pillow (Image Processing)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Installing rembg and Pillow...
echo.

pip install rembg pillow

echo.
echo Installation complete!
echo.
pause
