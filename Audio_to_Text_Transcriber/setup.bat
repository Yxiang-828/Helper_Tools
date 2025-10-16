@echo off
REM Audio to Text Transcriber Setup Script
REM This script installs the required dependencies for the Audio to Text Transcriber

echo Audio to Text Transcriber Setup
echo ===============================
echo.

echo Installing PyTorch (CPU version)...
py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
if %errorlevel% neq 0 (
    echo Error installing PyTorch. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo Installing OpenAI Whisper...
py -m pip install openai-whisper
if %errorlevel% neq 0 (
    echo Error installing OpenAI Whisper. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo Setup complete! You can now use the Audio to Text Transcriber.
echo.

echo Would you like to pre-download all Whisper models now? (Recommended)
echo This will download ~4GB of models and take several minutes.
echo You can skip this and models will download as needed during first use.
echo.
set /p download_choice="Download all models now? (y/n, default: n): "
if /i "%download_choice%"=="y" goto :download_models
if /i "%download_choice%"=="yes" goto :download_models

echo.
echo Setup finished! Run mp3-to-txt.bat from the root helper_tools directory to transcribe audio files.
echo Models will be downloaded automatically when first used.
pause
exit /b 0

:download_models
echo.
echo Downloading all Whisper models... This may take 10-15 minutes.
echo.

echo Downloading tiny model (39 MB)...
py -c "import whisper; whisper.load_model('tiny')"
if %errorlevel% neq 0 (
    echo Error downloading tiny model.
    pause
    exit /b 1
)

echo Downloading base model (74 MB)...
py -c "import whisper; whisper.load_model('base')"
if %errorlevel% neq 0 (
    echo Error downloading base model.
    pause
    exit /b 1
)

echo Downloading small model (244 MB)...
py -c "import whisper; whisper.load_model('small')"
if %errorlevel% neq 0 (
    echo Error downloading small model.
    pause
    exit /b 1
)

echo Downloading medium model (769 MB)...
py -c "import whisper; whisper.load_model('medium')"
if %errorlevel% neq 0 (
    echo Error downloading medium model.
    pause
    exit /b 1
)

echo Downloading large model (2.9 GB)... This will take the longest.
py -c "import whisper; whisper.load_model('large')"
if %errorlevel% neq 0 (
    echo Error downloading large model.
    pause
    exit /b 1
)

echo.
echo All models downloaded successfully!
echo You can now use the Audio to Text Transcriber without any download delays.
pause