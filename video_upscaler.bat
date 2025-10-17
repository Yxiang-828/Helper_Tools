@echo off
REM Video Upscaler Batch File
REM Uses py command for Python execution

echo ========================================
echo AMD GPU Video Upscaler Tool
echo ========================================
echo.

REM Prompt for inputs
set /p input_video="Enter input video path: "
if "%input_video%"=="" (
    echo No input video provided.
    pause
    exit /b 1
)

set /p scale="Enter scale number (1=4x, 2=3x, 3=2x default 1): "
if "%scale%"=="" set scale=1
if "%scale%"=="1" set scale=4
if "%scale%"=="2" set scale=3
if "%scale%"=="3" set scale=2
if "%scale%" neq "2" if "%scale%" neq "3" if "%scale%" neq "4" set scale=4

set /p method="Enter method number (1=realesrgan, 2=ffmpeg, 3=extract, 4=process_existing default 1): "
if "%method%"=="" set method=1
if "%method%"=="1" set method=realesrgan
if "%method%"=="2" set method=ffmpeg
if "%method%"=="3" set method=extract
if "%method%"=="4" set method=process_existing
if "%method%" neq "ffmpeg" if "%method%" neq "realesrgan" if "%method%" neq "extract" if "%method%" neq "process_existing" set method=realesrgan

set /p format="Enter format number (1=mp4, 2=gif default 1): "
if "%format%"=="" set format=1
if "%format%"=="1" set format=mp4
if "%format%"=="2" set format=gif
if "%format%" neq "mp4" if "%format%" neq "gif" set format=mp4

REM Build command
set cmd=py "C:\Program Files (x86)\helper_tools\video_upscaler\video_upscaler.py" "%input_video%" --scale %scale% --method %method% --format %format%

echo.
echo Running: %cmd%
echo.

REM Run the Python script
%cmd%

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Video upscaling failed with exit code %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo SUCCESS: Video upscaling completed!
echo ========================================
pause