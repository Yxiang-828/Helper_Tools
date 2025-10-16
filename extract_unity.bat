@echo off
echo Unity Image Extractor
echo ====================
echo.
echo Extracts images from Unity3D bundle files
echo.
echo Usage:
echo   extract_unity.bat "path\to\unity3d_file_or_directory"
echo.
echo Options:
echo   -o, --output DIR     Output directory (default: Unity_Image_Extractor\extracted_images)
echo   -r, --recursive      Search subdirectories recursively
echo   --no-recursive       Don't search subdirectories
echo.
echo Examples:
echo   extract_unity.bat "C:\Game\Assets\ui.unity3d"
echo   extract_unity.bat "C:\Game\Assets" -r -o "C:\Extracted"
echo.

echo Output will be saved to: Unity_Image_Extractor\extracted_images\
echo.

py "%~dp0Unity_Image_Extractor\unity_image_extractor.py" %*

echo.
echo ========================================
echo Extraction complete!
echo Check: Unity_Image_Extractor\extracted_images\
echo ========================================