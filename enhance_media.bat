@echo off
REM Media Resolution Enhancer - Simple Version
REM Usage: enhance_media.bat "input_file"

if "%~1"=="" (
    echo ERROR: No input file specified!
    echo.
    echo Usage: enhance_media.bat "path\to\media_file"
    echo.
    echo Example: enhance_media.bat "C:\Photos\image.jpg"
    echo.
    pause
    exit /b 1
)

set "input_file=%~1"

REM Check if file exists
if not exist "%input_file%" (
    echo ERROR: File not found: %input_file%
    echo.
    pause
    exit /b 1
)

echo ========================================
echo    Media Resolution Enhancer
echo ========================================
echo.
echo File: %input_file%
echo.

REM Ask for scale
echo Choose scale factor:
echo 2. 2x (recommended)
echo 3. 3x
echo 4. 4x (high quality)
echo.
set /p scale_choice="Enter scale (2-4) or press Enter for 2x: "

if "%scale_choice%"=="2" (
    set "scale=2"
) else if "%scale_choice%"=="3" (
    set "scale=3"
) else if "%scale_choice%"=="4" (
    set "scale=4"
) else (
    set "scale=2"
)

echo.
echo Processing with %scale%x scale using AI enhancement...
echo.

py "%~dp0Media_Resolution_Enhancer\media_enhancer.py" "%input_file%" --scale %scale% --method ai

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo           SUCCESS!
    echo ========================================
    echo.
    echo Enhanced file saved to: Media_Resolution_Enhancer\enhanced_media\
    echo.
) else (
    echo.
    echo ERROR: Enhancement failed.
    echo.
)

echo Press any key to exit...
pause >nul