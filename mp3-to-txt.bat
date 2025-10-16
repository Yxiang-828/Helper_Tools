@echo off
setlocal enabledelayedexpansion

REM Audio to Text Converter Batch File
REM Usage: mp3-to-txt.bat <audio_file>

if "%~1"=="" (
    echo Usage: mp3-to-txt.bat ^<audio_file^>
    echo.
    echo This will start an interactive setup to choose your options.
    echo.
    pause
    exit /b 1
)

REM Store the full path in a variable to avoid expansion issues
set "audio_file=%~1"

REM Check if file exists
if not exist "%audio_file%" (
    echo Error: File "%audio_file%" not found.
    echo Make sure to use quotes around the full file path.
    pause
    exit /b 1
)

echo Audio to Text Transcriber
echo =======================
echo File: "!audio_file!"
echo.

REM Language selection
echo Language Options:
echo 1. English (en) - Recommended for best accuracy
echo 2. Chinese (zh) - Mandarin Chinese
echo 3. Japanese (ja) - Japanese
echo 4. Spanish (es) - Spanish
echo 5. French (fr) - French
echo 6. German (de) - German
echo 7. Korean (ko) - Korean
echo 8. Auto-detect - Let Whisper detect the language automatically
echo.
set /p lang_choice="Choose language (1-8, default: 1): "
if "%lang_choice%"=="1" set language=en
if "%lang_choice%"=="2" set language=zh
if "%lang_choice%"=="3" set language=ja
if "%lang_choice%"=="4" set language=es
if "%lang_choice%"=="5" set language=fr
if "%lang_choice%"=="6" set language=de
if "%lang_choice%"=="7" set language=ko
if "%lang_choice%"=="8" set language=auto
if not defined language set language=en

echo.

REM Model selection
echo Model Options:
echo 1. tiny   - 39 MB, Fastest, Basic accuracy (good for testing)
echo 2. base   - 74 MB, Fast, Balanced speed/accuracy (recommended)
echo 3. small  - 244 MB, Medium, Better accuracy for clear audio
echo 4. medium - 769 MB, Slow, High accuracy for important content
echo 5. large  - 2.9 GB, Slowest, Best accuracy for critical work
echo.
set /p model_choice="Choose model (1-5, default: 2): "
if "%model_choice%"=="1" set model=tiny
if "%model_choice%"=="2" set model=base
if "%model_choice%"=="3" set model=small
if "%model_choice%"=="4" set model=medium
if "%model_choice%"=="5" set model=large
if not defined model set model=base

echo.

REM Output directory
echo Output Directory:
echo Leave blank to use default (Audio_to_Text_Transcriber\output_transcripts\)
set /p output_dir="Output directory (optional): "

echo.
echo Starting transcription...
echo Language: %language%
echo Model: %model%
if defined output_dir echo Output: %output_dir%
echo.

REM Build command
set cmd=py "C:\Program Files (x86)\helper_tools\Audio_to_Text_Transcriber\audio_to_text.py" "!audio_file!" --model %model% --language %language%
if defined output_dir set cmd=%cmd% --output-dir "%output_dir%"

REM Run the command
%cmd%

if %errorlevel% neq 0 (
    echo.
    echo Error occurred during conversion.
    pause
    exit /b 1
)

echo.
echo Transcription completed successfully!
pause