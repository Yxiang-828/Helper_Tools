@echo off
REM Media Resolution Enhancer Batch File
REM Usage: enhance_media.bat "input_file" [--scale FACTOR] [--output OUTPUT_FILE]

if "%~1"=="" (
    echo ERROR: No input file specified!
    echo.
    echo Usage: enhance_media.bat "path\to\media_file" [--scale 2.0] [--output "output_path"]
    echo.
    echo Supported formats:
    echo Images: PNG, JPG, JPEG, BMP, TIFF
    echo Videos: MP4, MOV, AVI, MKV, WebM, FLV
    echo.
    echo Scale options: 1.5, 2.0, 3.0, 4.0 (default: 2.0)
    echo.
    pause
    exit /b 1
)

echo Enhancing media resolution...
echo Input: %~1
echo.

py "%~dp0media_enhancer.py" %*

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Check the Media_Resolution_Enhancer\enhanced_media folder for your enhanced file.
) else (
    echo.
    echo ERROR: Enhancement failed. Check the error messages above.
)

echo.
pause