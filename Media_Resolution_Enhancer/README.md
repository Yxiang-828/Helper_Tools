# Media Resolution Enhancer

Enhances the resolution of images and videos using AI-powered super resolution and advanced computer vision algorithms. Supports multiple formats including PNG, JPG, MP4, MOV, and more.

## Features

- **AI-Powered Enhancement**: Uses EDSR (Enhanced Deep Super Resolution) neural networks for natural, high-quality upscaling
- **Classical Enhancement**: Improved computer vision algorithms as fallback
- **Image Enhancement**: Upscale and enhance images with AI-like quality
- **Video Enhancement**: Process entire videos frame-by-frame for high quality results
- **Multiple Scales**: Choose from 2x, 3x, or 4x resolution increase
- **Automatic Fallback**: Falls back to classical methods if AI is unavailable
- **Batch Processing**: Easy-to-use batch file interface

## Installation

1. Install Python dependencies:
   ```
   pip install opencv-contrib-python pillow numpy
   ```

2. Download AI models (automatic):
   ```bash
   py download_models.py
   ```

3. Ensure FFmpeg is installed (required for video processing):
   - Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
   - Extract to `C:\ffmpeg\` (create folder if needed)
   - The script automatically uses `C:\ffmpeg\bin\ffmpeg.exe`

## Usage

### Easy Mode (Recommended for beginners)
1. **Drag & Drop**: Simply drag any image or video file onto `enhance_media.bat`
2. **Interactive Menu**: Double-click `enhance_media.bat` and follow the on-screen prompts
3. **Automatic Enhancement**: Uses AI with 2x scaling by default

### Advanced Mode (For power users)
Use `enhance_media_advanced.bat` with command line parameters:
```cmd
enhance_media_advanced.bat "input_file" --scale 4 --method ai --output "custom_output.jpg"
```

### Batch File Options
- **enhance_media.bat**: User-friendly interactive interface
- **enhance_media_advanced.bat**: Command-line interface for scripts and automation

## Supported Formats

### Images
- PNG, JPG, JPEG, BMP, TIFF, TIF, GIF

### Videos
- MP4, MOV, AVI, MKV, WebM, FLV

## Enhancement Methods

### AI Method (Recommended)
- **EDSR Neural Networks**: Deep learning-based super resolution
- **Natural Results**: Produces more realistic and detailed enhancements
- **Multiple Scales**: 2x, 3x, and 4x upscaling available
- **Automatic Model Download**: Models are downloaded automatically on first use

### Classical Method
- **Bicubic Interpolation**: Initial upscaling with high-quality algorithm
- **CLAHE**: Contrast Limited Adaptive Histogram Equalization for better contrast
- **Sharpening**: Edge enhancement using convolution filters
- **Color Enhancement**: LAB color space processing for more natural results

## Output

- Images: Saved as `{filename}_enhanced.{ext}` in `enhanced_media/` folder
- Videos: Processed frame-by-frame and reassembled with high quality encoding
- Original files are never modified

## Performance Notes

- Image processing: Usually completes in seconds
- Video processing: Time depends on video length and resolution
  - Short clips: 1-5 minutes
  - Full movies: 30+ minutes (depending on hardware)
- GPU acceleration recommended for faster processing

## Examples

```cmd
REM Enhance a photo 2x
enhance_media.bat "C:\Photos\vacation.jpg"

REM Enhance a video 1.5x
enhance_media.bat "C:\Videos\tutorial.mp4" --scale 1.5

REM Custom output location
enhance_media.bat "input.png" --output "C:\Output\enhanced.png"
```

## Credits

- **OpenCV**: Computer vision library with DNN super resolution (https://opencv.org/)
- **EDSR**: Enhanced Deep Super Resolution networks (https://github.com/Saafke/EDSR_Tensorflow)
- **Pillow (PIL)**: Python Imaging Library (https://python-pillow.org/)
- **FFmpeg**: Multimedia processing tool (https://ffmpeg.org/)
- **NumPy**: Scientific computing library (https://numpy.org/)