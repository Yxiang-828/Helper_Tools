# Media Resolution Enhancer

Enhances the resolution of images and videos using advanced computer vision algorithms. Supports multiple formats including PNG, JPG, MP4, MOV, and more.

## Features

- **Image Enhancement**: Upscale and sharpen images with AI-like quality
- **Video Enhancement**: Process entire videos frame-by-frame for high quality results
- **Multiple Scales**: Choose from 1.5x, 2x, 3x, or 4x resolution increase
- **Advanced Algorithms**: Uses CLAHE, sharpening, and noise reduction
- **Batch Processing**: Easy-to-use batch file interface

## Installation

1. Install Python dependencies:
   ```
   pip install opencv-python pillow numpy
   ```

2. Ensure FFmpeg is installed (required for video processing):
   - Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
   - Extract to `C:\ffmpeg\` (create folder if needed)
   - The script automatically uses `C:\ffmpeg\bin\ffmpeg.exe`

## Usage

### Simple Batch File (Recommended)
```cmd
enhance_media.bat "path\to\image.jpg"
enhance_media.bat "path\to\video.mp4"
```

### With Custom Scale
```cmd
enhance_media.bat "image.png" --scale 3.0
enhance_media.bat "video.mov" --scale 1.5
```

### Command Line
```bash
py media_enhancer.py "input_file" --scale 2.0 --output "output_file"
```

## Supported Formats

### Images
- PNG, JPG, JPEG, BMP, TIFF, TIF, GIF

### Videos
- MP4, MOV, AVI, MKV, WebM, FLV

## Enhancement Techniques

1. **Bicubic Interpolation**: Initial upscaling with high-quality algorithm
2. **CLAHE**: Contrast Limited Adaptive Histogram Equalization for better contrast
3. **Sharpening**: Edge enhancement using convolution filters
4. **Noise Reduction**: Bilateral filtering to preserve edges while reducing noise
5. **Color Enhancement**: LAB color space processing for more natural results

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

- **OpenCV**: Computer vision library for image processing (https://opencv.org/)
- **Pillow (PIL)**: Python Imaging Library (https://python-pillow.org/)
- **FFmpeg**: Multimedia processing tool (https://ffmpeg.org/)
- **NumPy**: Scientific computing library (https://numpy.org/)