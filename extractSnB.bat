@echo off
title Silver and Blood - Comprehensive UI Extractor
echo.
echo ========================================
echo  Silver and Blood UI Extractor
echo ========================================
echo.
echo Extracting ALL UI images from game files...
echo This will extract to: complete_ui_extraction folder
echo Processing both Standard UI and HQ UI folders...
echo.

cd /d "%~dp0S&B_Extractor"
py comprehensive_ui_extractor.py

echo.
echo ========================================
echo Extraction complete!
echo Check the complete_ui_extraction folder for your images.
echo A viewer will also be created automatically.
echo ========================================
echo.
pause
