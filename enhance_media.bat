@echo off
REM Media Resolution Enhancer - Simple Version
REM Usage: enhance_media.bat "file_path" [scale]

if "%~1"=="" (
    echo ERROR: No input file specified!
    echo.
    echo Usage: enhance_media.bat "path\to\your\file.jpg" [2^|3^|4]
    echo.
    echo Supported formats: PNG, JPG, JPEG, BMP, TIFF, GIF, MP4, MOV, AVI, MKV, WebM, FLV
    echo Scale options: 2 (default), 3, 4
    echo.
    pause
    exit /b 1
)

REM Set default scale
set "scale=2"

REM Check if scale was provided as second argument
if not "%~2"=="" (
    set "scale=%~2"
)

echo Processing: %~1 (scale: %scale%x)
echo.

py "%~dp0Media_Resolution_Enhancer\media_enhancer.py" "%~1" --scale %scale% --method ai

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Enhanced file saved to Media_Resolution_Enhancer\enhanced_media\
) else (
    echo.
    echo ERROR: Processing failed.
)

echo.
pause