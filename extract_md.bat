@echo off
title Silver and Blood - Unity3D to Markdown Converter
echo.
echo ========================================
echo  Silver and Blood MD Converter
echo ========================================
echo.
echo Extracting ALL text strings from Unity file...
echo This will convert AllLanguageEN.unity3d to AllLanguageEN.md
echo.

cd /d "%~dp0"
.venv\Scripts\python.exe "S&B_Extractor\unity3d_to_md.py"

echo.
echo ========================================
echo Conversion complete!
echo Check AllLanguageEN.md for your readable strings.
echo ========================================
echo.
pause
