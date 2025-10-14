@echo off
REM Simple Audio to Text Transcriber
REM Usage: mp3-to-txt.bat "audio_file.mp3"

if "%~1"=="" (
    echo ERROR: No audio file specified!
    echo.
    echo Usage: mp3-to-txt.bat "path\to\audio_file.mp3"
    echo.
    echo Supported formats: MP3, WAV, M4A, FLAC, etc.
    echo Output will be saved as transcript.txt in the output_transcripts folder.
    echo.
    pause
    exit /b 1
)

echo Converting audio to text...
echo Input: %~1
echo.

py "%~dp0Audio_to_Text_Transcriber\audio_to_text.py" "%~1"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Check the Audio_to_Text_Transcriber\output_transcripts folder for your transcript.
) else (
    echo.
    echo ERROR: Conversion failed. Check the error messages above.
)

echo.
pause