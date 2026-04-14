@echo off
setlocal enabledelayedexpansion

REM Background Remover Tool
REM Usage: Place images in "Background_Remover\input" folder and run this script.

echo ========================================
echo       AI Background Remover Tool
echo ========================================
echo.
echo Make sure your images are in the "Background_Remover\input" folder.
echo.

REM Check for Python
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install Python first.
    pause
    exit /b 1
)

REM Check if input folder has files
if not exist "Background_Remover\input" (
    mkdir "Background_Remover\input"
    echo Created input folder: Background_Remover\input
    echo Please place your images there and run this script again.
    pause
    exit /b
)

REM Run the python script
echo Starting background removal process...
echo This may take a while, especially for the first run (downloading models).
echo.

pushd "Background_Remover"
py remove_background.py
popd

echo.
echo Process complete!
echo Check "Background_Remover\output" for results.
echo.
pause
