@echo off
REM Media Resolution Enhancer Batch File
REM Usage: enhance_media.bat "input_file" [--scale FACTOR] [--method ai|classical] [--output OUTPUT_FILE]

if "%~1"=="" (
    echo ERROR: No input file specified!
    echo.
    echo Usage: enhance_media.bat "path\to\media_file" [--scale 2.0] [--method ai] [--output "output_path"]
    echo.
    echo Supported formats:
    echo Images: PNG, JPG, JPEG, BMP, TIFF
    echo Videos: MP4, MOV, AVI, MKV, WebM, FLV
    echo.
    echo Scale options: 2, 3, 4 (default: 2)
    echo Method options: ai (recommended), classical (default: ai)
    echo.
    pause
    exit /b 1
)

echo Enhancing media resolution...
echo Input: %~1
echo.

py "%~dp0Media_Resolution_Enhancer\media_enhancer.py" %*

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Check the Media_Resolution_Enhancer\enhanced_media folder for your enhanced file.
) else (
    echo.
    echo ERROR: Enhancement failed. Check the error messages above.
)

echo.
pause