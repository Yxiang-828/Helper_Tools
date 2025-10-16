@echo off
REM Media Resolution Enhancer - Simple Version
REM Usage: enhance_media.bat "file_path"

if "%~1"=="" (
    echo ERROR: No input file specified!
    echo.
    echo Usage: enhance_media.bat "path\to\your\file.jpg"
    echo.
    echo Supported formats: PNG, JPG, JPEG, BMP, TIFF, GIF, MP4, MOV, AVI, MKV, WebM, FLV
    echo.
    echo Uses AI enhancement with 2x scaling by default.
    echo.
    pause
    exit /b 1
)

echo Processing: %~1
echo.

py "%~dp0Media_Resolution_Enhancer\media_enhancer.py" "%~1" --scale 2 --method ai

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Enhanced file saved to Media_Resolution_Enhancer\enhanced_media\
) else (
    echo.
    echo ERROR: Processing failed.
)

echo.
pause