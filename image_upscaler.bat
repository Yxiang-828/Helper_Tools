@echo off
setlocal enabledelayedexpansion

REM AMD GPU Image Upscaler - Interactive Mode
REM Usage: image_upscaler.bat "input_file"

if "%~1"=="" (
    echo ========================================
    echo      AMD GPU Image Upscaler
    echo ========================================
    echo.
    echo ERROR: No input file specified!
    echo.
    echo Usage: image_upscaler.bat "path\to\image_file"
    echo.
    echo Then choose method and scale interactively.
    echo.
    pause
    exit /b 1
)

REM Set input file
set INPUT_FILE=%~1

REM Check if file exists
if not exist "%INPUT_FILE%" (
    echo ERROR: File not found: %INPUT_FILE%
    echo.
    pause
    exit /b 1
)

echo ========================================
echo      AMD GPU Image Upscaler
echo ========================================
echo Input: %INPUT_FILE%
echo.

REM Choose method
echo Choose upscaling method:
echo 1. Real-ESRGAN Vulkan (GPU - fast, good quality)
echo 2. EDSR OpenCV (CPU - slower, sharper)
echo.
set /p METHOD_CHOICE="Enter 1 or 2: "

if "%METHOD_CHOICE%"=="1" (
    set METHOD=realesrgan
) else if "%METHOD_CHOICE%"=="2" (
    set METHOD=edsr
) else (
    echo Invalid choice. Defaulting to Real-ESRGAN.
    set METHOD=realesrgan
)

REM Choose scale
echo.
echo Choose scale factor (2, 3, or 4):
set /p SCALE="Enter scale (default 4): "
if "%SCALE%"=="" set SCALE=4

echo.
echo Method: %METHOD%
echo Scale: %SCALE%x
echo Processing...
echo.

REM Get full path
for %%F in ("%INPUT_FILE%") do (
    set FILENAME=%%~nF
    set FILEEXT=%%~xF
)

REM Output path
set OUTPUT_DIR=%~dp0image_upscaler\output
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
set WIN_OUTPUT=%OUTPUT_DIR%\%FILENAME%_%METHOD%_x%SCALE%%FILEEXT%
echo.

if /i "%METHOD%"=="realesrgan" (
    echo Running Real-ESRGAN Vulkan...
    "%~dp0image_upscaler\realesrgan-windows\realesrgan-ncnn-vulkan.exe" -i "%INPUT_FILE%" -o "%WIN_OUTPUT%" -s %SCALE% -v
) else if /i "%METHOD%"=="edsr" (
    echo Running EDSR OpenCV on Windows...
    py "%~dp0image_upscaler\opencv_edsr.py" "%INPUT_FILE%" --scale %SCALE% --output "%WIN_OUTPUT%"
) else (
    echo ERROR: Invalid method: %METHOD%
    echo Use --method realesrgan or --method edsr
    pause
    exit /b 1
)

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo           SUCCESS!
    echo ========================================
    echo Output: "%WIN_OUTPUT%"
    echo.
) else (
    echo.
    echo ========================================
    echo           ERROR!
    echo ========================================
    echo Check error messages above.
    echo.
)

pause
endlocal