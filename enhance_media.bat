@echo off
REM Media Resolution Enhancer - User Friendly Version
REM Supports drag & drop or interactive mode

setlocal enabledelayedexpansion

REM Check if file was dragged onto the batch file
if "%~1"=="" goto :interactive_mode

REM File was provided via drag & drop or command line
set "input_file=%~1"
goto :process_file

:interactive_mode
cls
echo ========================================
echo    Media Resolution Enhancer v2.0
echo ========================================
echo.
echo Welcome! This tool enhances image and video resolution using AI.
echo.
echo How would you like to provide your file?
echo.
echo 1. Drag and drop a file onto this batch file
echo 2. Enter the file path manually
echo 3. Browse for a file (opens file explorer)
echo.
set /p choice="Enter your choice (1-3) or press Enter for help: "

if "%choice%"=="1" goto :drag_drop_help
if "%choice%"=="2" goto :manual_input
if "%choice%"=="3" goto :browse_file
if "%choice%"=="" goto :show_help
goto :interactive_mode

:drag_drop_help
cls
echo ========================================
echo         Drag & Drop Instructions
echo ========================================
echo.
echo To use drag and drop:
echo.
echo 1. Close this window
echo 2. Find your image or video file in File Explorer
echo 3. Drag the file and drop it onto this batch file
echo    (enhance_media.bat)
echo.
echo The enhancement will start automatically!
echo.
echo Supported formats:
echo Images: PNG, JPG, JPEG, BMP, TIFF, GIF
echo Videos: MP4, MOV, AVI, MKV, WebM, FLV
echo.
pause
goto :interactive_mode

:manual_input
cls
echo ========================================
echo         Manual File Input
echo ========================================
echo.
echo Enter the full path to your media file:
echo (Example: C:\Photos\my_image.jpg)
echo.
set /p input_file="File path: "

if "%input_file%"=="" (
    echo No file specified. Returning to menu...
    timeout /t 2 >nul
    goto :interactive_mode
)

REM Remove quotes if present
set input_file=%input_file:"=%

if not exist "%input_file%" (
    echo.
    echo ERROR: File not found: %input_file%
    echo.
    echo Make sure the path is correct and the file exists.
    echo.
    pause
    goto :interactive_mode
)

goto :process_file

:browse_file
cls
echo ========================================
echo         File Browser
echo ========================================
echo.
echo Opening file browser...
echo Select your image or video file.
echo.
echo Press any key to continue...
pause >nul

REM Create a temporary VBScript to open file dialog
echo Set objShell = CreateObject("Shell.Application") > "%temp%\file_dialog.vbs"
echo Set objFolder = objShell.BrowseForFolder(0, "Select a media file to enhance:", &H4000, 0) >> "%temp%\file_dialog.vbs"
echo If Not objFolder Is Nothing Then >> "%temp%\file_dialog.vbs"
echo     Set objFolderItem = objFolder.Self >> "%temp%\file_dialog.vbs"
echo     WScript.Echo objFolderItem.Path >> "%temp%\file_dialog.vbs"
echo End If >> "%temp%\file_dialog.vbs"

for /f "delims=" %%i in ('cscript //nologo "%temp%\file_dialog.vbs"') do set "selected_path=%%i"

REM Clean up temp file
del "%temp%\file_dialog.vbs" 2>nul

if "%selected_path%"=="" (
    echo No file selected. Returning to menu...
    timeout /t 2 >nul
    goto :interactive_mode
)

REM Ask user to select a specific file from the folder
echo Selected folder: %selected_path%
echo.
echo Please enter the filename (with extension) from this folder:
set /p filename="Filename: "

if "%filename%"=="" (
    echo No filename specified. Returning to menu...
    timeout /t 2 >nul
    goto :interactive_mode
)

set "input_file=%selected_path%\%filename%"

if not exist "%input_file%" (
    echo.
    echo ERROR: File not found: %input_file%
    echo.
    pause
    goto :interactive_mode
)

goto :process_file

:show_help
cls
echo ========================================
echo           Help & Usage Guide
echo ========================================
echo.
echo BASIC USAGE:
echo -----------
echo 1. Drag and drop any image or video file onto enhance_media.bat
echo 2. The file will be enhanced automatically using AI (recommended)
echo.
echo SUPPORTED FORMATS:
echo -----------------
echo Images: PNG, JPG, JPEG, BMP, TIFF, GIF
echo Videos: MP4, MOV, AVI, MKV, WebM, FLV
echo.
echo ENHANCEMENT METHODS:
echo -------------------
echo AI (Recommended): Uses neural networks for natural, high-quality results
echo Classical: Traditional computer vision methods (fallback)
echo.
echo OUTPUT:
echo ------
echo Enhanced files are saved to: Media_Resolution_Enhancer\enhanced_media\
echo Original files are never modified.
echo.
echo ADVANCED USAGE:
echo --------------
echo enhance_media.bat "file.jpg" --scale 4 --method ai
echo enhance_media.bat "video.mp4" --scale 2 --method classical
echo.
echo Scale options: 2, 3, 4 (default: 2)
echo Method options: ai, classical (default: ai)
echo.
pause
goto :interactive_mode

:process_file
cls
echo ========================================
echo        Processing Your File
echo ========================================
echo.
echo File: %input_file%
echo.

REM Check if file exists
if not exist "%input_file%" (
    echo ERROR: File not found: %input_file%
    echo.
    pause
    exit /b 1
)

REM Get file extension
for %%i in ("%input_file%") do set "ext=%%~xi"
set "ext=%ext:~1%"

REM Validate file type
set "valid_image=0"
set "valid_video=0"

REM Check image extensions
if /i "%ext%"=="png" set valid_image=1
if /i "%ext%"=="jpg" set valid_image=1
if /i "%ext%"=="jpeg" set valid_image=1
if /i "%ext%"=="bmp" set valid_image=1
if /i "%ext%"=="tiff" set valid_image=1
if /i "%ext%"=="tif" set valid_image=1
if /i "%ext%"=="gif" set valid_image=1

REM Check video extensions
if /i "%ext%"=="mp4" set valid_video=1
if /i "%ext%"=="mov" set valid_video=1
if /i "%ext%"=="avi" set valid_video=1
if /i "%ext%"=="mkv" set valid_video=1
if /i "%ext%"=="webm" set valid_video=1
if /i "%ext%"=="flv" set valid_video=1

if %valid_image%==0 if %valid_video%==0 (
    echo ERROR: Unsupported file type: %ext%
    echo.
    echo Supported formats:
    echo Images: PNG, JPG, JPEG, BMP, TIFF, GIF
    echo Videos: MP4, MOV, AVI, MKV, WebM, FLV
    echo.
    pause
    exit /b 1
)

REM Ask for enhancement options
echo Choose enhancement options:
echo.
echo 1. Quick Enhance (AI, 2x scale - Recommended)
echo 2. High Quality (AI, 4x scale)
echo 3. Custom settings
echo 4. Classical method (traditional enhancement)
echo.
set /p enhance_choice="Enter your choice (1-4) or press Enter for default: "

if "%enhance_choice%"=="1" (
    set "scale=2"
    set "method=ai"
) else if "%enhance_choice%"=="2" (
    set "scale=4"
    set "method=ai"
) else if "%enhance_choice%"=="3" (
    goto :custom_settings
) else if "%enhance_choice%"=="4" (
    set "scale=2"
    set "method=classical"
) else (
    REM Default
    set "scale=2"
    set "method=ai"
)

goto :start_enhancement

:custom_settings
echo.
echo CUSTOM SETTINGS:
echo ===============
echo.
echo Scale factor (2, 3, or 4):
set /p scale="Scale: "
if "%scale%"=="" set "scale=2"

echo.
echo Enhancement method (ai or classical):
set /p method="Method: "
if "%method%"=="" set "method=ai"

:start_enhancement
echo.
echo ========================================
echo        Starting Enhancement
echo ========================================
echo.
echo Settings:
echo - Scale: %scale%x
echo - Method: %method%
echo - Input: %input_file%
echo.
echo Processing... This may take a few minutes.
echo.

REM Run the enhancement
py "%~dp0Media_Resolution_Enhancer\media_enhancer.py" "%input_file%" --scale %scale% --method %method%

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo           SUCCESS!
    echo ========================================
    echo.
    echo Your enhanced file has been saved to:
    echo Media_Resolution_Enhancer\enhanced_media\
    echo.
    echo Original file: %input_file%
    echo.
    echo Thank you for using Media Resolution Enhancer!
    echo.
) else (
    echo.
    echo ========================================
    echo           ERROR
    echo ========================================
    echo.
    echo Enhancement failed. Please check the error messages above.
    echo.
    echo Possible solutions:
    echo - Make sure you have installed the required dependencies
    echo - Check that FFmpeg is installed (for videos)
    echo - Try using a different file format
    echo.
)

echo Press any key to exit...
pause >nul
exit /b %errorlevel%