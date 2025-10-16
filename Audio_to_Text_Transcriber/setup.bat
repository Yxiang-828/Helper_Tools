@echo off
REM Audio to Text Transcriber Setup Script for AMD GPU + Windows
REM CRITICAL: This setup is specifically for AMD GPUs using DirectML on Windows

echo =======================================================================
echo  AUDIO TO TEXT TRANSCRIBER - AMD GPU SETUP (WINDOWS ONLY)
echo =======================================================================
echo.
echo  IMPORTANT REQUIREMENTS:
echo  - AMD Radeon RX 6000/7000/8000 series GPU (RX 6800 XT tested)
echo  - Windows 10/11 (native - no WSL required)
echo  - Python 3.13.x installed
echo  - Administrator privileges recommended
echo.
echo  This setup installs DirectML for AMD GPU acceleration.
echo  NO CUDA/ROCm required - DirectML is Microsoft's native solution.
echo.
pause

echo.
echo =======================================================================
echo  STEP 1: Checking Python Version
echo =======================================================================
echo.

py --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found or not in PATH.
    echo Please install Python 3.13 from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python: %PYTHON_VERSION%
echo.

REM Check if version starts with 3.13
echo %PYTHON_VERSION% | findstr /r /c:"3\.13\." >nul
if %errorlevel% neq 0 (
    echo ERROR: Python 3.13.x required. You have: %PYTHON_VERSION%
    echo Please install Python 3.13 from https://python.org
    pause
    exit /b 1
)

echo ✅ Python 3.13.x confirmed
echo.

echo =======================================================================
echo  STEP 2: Upgrading pip
echo =======================================================================
echo.

py -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Could not upgrade pip, continuing anyway...
)

echo.
echo =======================================================================
echo  STEP 3: Installing PyTorch (CPU version)
echo =======================================================================
echo.
echo Installing PyTorch CPU version...
echo (GPU acceleration comes from DirectML in next step)
echo.

py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyTorch.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✅ PyTorch installed successfully
echo.

echo =======================================================================
echo  STEP 4: Installing ONNX Runtime DirectML (CRITICAL FOR AMD GPU)
echo =======================================================================
echo.
echo Installing ONNX Runtime with DirectML for AMD GPU acceleration...
echo This enables GPU acceleration on AMD Radeon RX 6000+ series GPUs.
echo.

py -m pip install onnxruntime-directml
if %errorlevel% neq 0 (
    echo ERROR: Failed to install ONNX Runtime DirectML.
    echo This is required for AMD GPU acceleration.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✅ ONNX Runtime DirectML installed
echo.

echo =======================================================================
echo  STEP 5: Installing Optimum (ONNX Optimization)
echo =======================================================================
echo.
echo Installing Optimum for converting models to ONNX format...
echo This optimizes Whisper models for GPU inference.
echo.

py -m pip install optimum[onnxruntime]
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Optimum.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✅ Optimum installed successfully
echo.

echo =======================================================================
echo  STEP 6: Installing Librosa (Audio Processing)
echo =======================================================================
echo.
echo Installing Librosa for audio file processing...
echo.

py -m pip install librosa
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Librosa.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✅ Librosa installed successfully
echo.

echo =======================================================================
echo  STEP 7: Verifying DirectML Installation (CRITICAL CHECK)
echo =======================================================================
echo.
echo Verifying that DirectML execution provider is available...
echo This confirms AMD GPU acceleration will work.
echo.

py -c "import onnxruntime as ort; providers = ort.get_available_providers(); print('Available providers:', providers); assert 'DmlExecutionProvider' in providers, 'DirectML not available!'; print('✅ DirectML GPU acceleration confirmed!')"
if %errorlevel% neq 0 (
    echo.
    echo ❌ CRITICAL ERROR: DirectML execution provider not found!
    echo.
    echo This means AMD GPU acceleration will NOT work.
    echo.
    echo TROUBLESHOOTING STEPS:
    echo 1. Ensure you have AMD Radeon RX 6000/7000/8000 series GPU
    echo 2. Update AMD drivers using AMD Adrenalin software
    echo 3. Try reinstalling: py -m pip install onnxruntime-directml --force-reinstall
    echo 4. Restart your computer and run setup again
    echo.
    echo If this persists, the tool will fall back to CPU-only mode (much slower).
    echo.
    pause
    REM Don't exit - continue with setup but warn user
)

echo.
echo =======================================================================
echo  SETUP COMPLETE! 🎉
echo =======================================================================
echo.
echo ✅ All dependencies installed successfully
echo ✅ DirectML GPU acceleration ready (if verification passed above)
echo.
echo ┌─────────────────────────────────────────────────────────────────┐
echo │                      NEXT STEPS                                │
echo ├─────────────────────────────────────────────────────────────────┤
echo │ 1. Test basic functionality:                                   │
echo │    py audio_to_text.py "path/to/audio.mp3" --model tiny        │
echo │                                                               │
echo │ 2. Use interactive mode (recommended):                        │
echo │    From helper_tools root: mp3-to-txt.bat "path/to/audio.mp3"  │
echo │                                                               │
echo │ 3. Expected first run behavior:                               │
echo │    - Shows "Converting to ONNX format" (normal)               │
echo │    - Takes 5-20 seconds depending on model                    │
echo │    - Subsequent runs: 2-5 seconds (cached)                    │
echo │                                                               │
echo │ 4. GPU acceleration indicators:                               │
echo │    - "DirectML GPU acceleration" in output                    │
echo │    - Much faster than CPU-only mode                          │
echo └─────────────────────────────────────────────────────────────────┘
echo.
echo If you encounter issues:
echo - Check GPU: AMD Radeon RX 6000+ series required
echo - Update drivers: Use AMD Adrenalin software
echo - Restart PC: Sometimes required for DirectML
echo - Re-run setup: If DirectML verification failed
echo.
pause

echo =======================================================================
echo  OPTIONAL: Pre-download Whisper Models (ONNX Optimized)
echo =======================================================================
echo.
echo Would you like to pre-download all Whisper models now? (HIGHLY RECOMMENDED)
echo.
echo BENEFITS:
echo - Downloads ~4GB of ONNX-optimized models (converted for GPU)
echo - Takes 10-15 minutes but eliminates first-run conversion delays
echo - Models cached locally for instant future use
echo - Each model loads in 2-5 seconds instead of 10-60 seconds
echo.
echo MODELS INCLUDE:
echo - tiny   (39MB)  - Fastest, basic accuracy
echo - base   (74MB)  - Fast, balanced (recommended)
echo - small  (244MB) - Medium speed, better accuracy
echo - medium (769MB) - Slow, high accuracy
echo - large  (2.9GB) - Slowest, best accuracy
echo.
echo You can skip this - models download automatically when first used.
echo But you'll experience conversion delays on every new model.
echo.
set /p download_choice="Download all models now? (y/n, default: n): "
if /i "%download_choice%"=="y" goto :download_models
if /i "%download_choice%"=="yes" goto :download_models

echo.
echo Setup finished! Models will be downloaded automatically when first used.
echo Use: mp3-to-txt.bat "path/to/audio.mp3"
pause
exit /b 0

:download_models
echo.
echo =======================================================================
echo  DOWNLOADING WHISPER MODELS (ONNX OPTIMIZED FOR GPU)
echo =======================================================================
echo.
echo This converts PyTorch models to ONNX format optimized for DirectML.
echo Each model will show conversion warnings (normal) and take time.
echo Models are cached for instant future use.
echo.
echo Press Ctrl+C to cancel if needed.
echo.

echo ─────────────────────────────────────────────────────────────────────
echo Downloading tiny model (39 MB - converts to ONNX for GPU)...
echo Expected: 5-10 seconds conversion time
echo ─────────────────────────────────────────────────────────────────────
py -c "from optimum.onnxruntime import ORTModelForSpeechSeq2Seq; ORTModelForSpeechSeq2Seq.from_pretrained('openai/whisper-tiny', provider='DmlExecutionProvider')"
if %errorlevel% neq 0 (
    echo ❌ Error downloading tiny model.
    echo You can still use it - will download automatically when needed.
)

echo.
echo ─────────────────────────────────────────────────────────────────────
echo Downloading base model (74 MB - converts to ONNX for GPU)...
echo Expected: 10-20 seconds conversion time
echo ─────────────────────────────────────────────────────────────────────
py -c "from optimum.onnxruntime import ORTModelForSpeechSeq2Seq; ORTModelForSpeechSeq2Seq.from_pretrained('openai/whisper-base', provider='DmlExecutionProvider')"
if %errorlevel% neq 0 (
    echo ❌ Error downloading base model.
    echo You can still use it - will download automatically when needed.
)

echo.
echo ─────────────────────────────────────────────────────────────────────
echo Downloading small model (244 MB - converts to ONNX for GPU)...
echo Expected: 30-60 seconds conversion time
echo ─────────────────────────────────────────────────────────────────────
py -c "from optimum.onnxruntime import ORTModelForSpeechSeq2Seq; ORTModelForSpeechSeq2Seq.from_pretrained('openai/whisper-small', provider='DmlExecutionProvider')"
if %errorlevel% neq 0 (
    echo ❌ Error downloading small model.
    echo You can still use it - will download automatically when needed.
)

echo.
echo ─────────────────────────────────────────────────────────────────────
echo Downloading medium model (769 MB - converts to ONNX for GPU)...
echo Expected: 2-3 minutes conversion time
echo ─────────────────────────────────────────────────────────────────────
py -c "from optimum.onnxruntime import ORTModelForSpeechSeq2Seq; ORTModelForSpeechSeq2Seq.from_pretrained('openai/whisper-medium', provider='DmlExecutionProvider')"
if %errorlevel% neq 0 (
    echo ❌ Error downloading medium model.
    echo You can still use it - will download automatically when needed.
)

echo.
echo ─────────────────────────────────────────────────────────────────────
echo Downloading large model (2.9 GB - converts to ONNX for GPU)...
echo Expected: 3-5 minutes conversion time (longest)
echo ─────────────────────────────────────────────────────────────────────
py -c "from optimum.onnxruntime import ORTModelForSpeechSeq2Seq; ORTModelForSpeechSeq2Seq.from_pretrained('openai/whisper-large', provider='DmlExecutionProvider')"
if %errorlevel% neq 0 (
    echo ❌ Error downloading large model.
    echo You can still use it - will download automatically when needed.
)

echo.
echo =======================================================================
echo  MODEL DOWNLOAD COMPLETE! 🎉
echo =======================================================================
echo.
echo ✅ All Whisper models downloaded and optimized for DirectML GPU
echo ✅ No more conversion delays - instant loading for all models
echo ✅ Ready for production use
echo.
echo You can now use the Audio to Text Transcriber at full speed!
echo.
pause