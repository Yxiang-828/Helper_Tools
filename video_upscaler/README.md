# Video Upscaler

This is my project made for my own efficiency with an AMD GPU and Windows setup. Why did I make this? No such thing as we.

An efficient video upscaling tool optimized for AMD GPUs on Windows, supporting multiple upscaling methods including AI-based Real-ESRGAN and classical FFmpeg approaches. Designed to handle high-resolution videos with automatic fallback to CPU encoding when necessary.

## Features

### Upscaling Methods

- **Real-ESRGAN**: AI-powered upscaling using Vulkan acceleration, processes each frame individually for maximum quality
- **FFmpeg**: Fast classical upscaling using Lanczos interpolation with AMD VCE hardware encoding
- **Extract**: Frame extraction only, for manual processing
- **Process Existing**: Upscale already extracted frames

### Output Formats

- MP4 (default): Hardware-accelerated encoding with audio preservation
- GIF: Animated GIF creation from upscaled frames

### Scaling Options

- 2x, 3x, 4x upscaling factors (default: 4x)

### Hardware Support

- AMD GPU acceleration via AMF (H.264) for encoding
- Vulkan acceleration for Real-ESRGAN AI processing
- Automatic CPU fallback for high-resolution videos (>4000px width or >2000px height)

## CPU Encoding Details

When AMD hardware encoding is unavailable or fails (common with high-resolution outputs), the tool automatically falls back to CPU-based encoding using FFmpeg's libx264 encoder:

- **Preset**: 'fast' for standard resolutions, 'ultrafast' for high resolutions (>4000px)
- **CRF**: 18 for standard quality, 28 for high resolutions to maintain encoding speed
- **QP**: 18-24 depending on resolution for constant quality encoding
- **Timeout**: 10 minutes for reassembly operations

This ensures reliable output even on systems without compatible AMD GPUs.

## Real-ESRGAN Step-by-Step Procedure

Real-ESRGAN bypasses VRAM limitations by processing frames sequentially rather than loading entire videos into memory:

1. **Frame Extraction**: Extract all video frames to PNG files in a temporary directory using FFmpeg
2. **Individual Frame Upscaling**: Process each frame one-by-one with Real-ESRGAN Vulkan executable
   - Each frame is loaded, upscaled, and saved to disk immediately
   - Progress tracking shows current frame/total frames
   - Frames are stored persistently to allow resuming interrupted operations
3. **Frame Verification**: Check dimensions and file integrity of upscaled frames
4. **Video Reassembly**: Combine upscaled frames back into video using FFmpeg
   - Uses original video's audio track
   - Applies appropriate encoding (AMD hardware or CPU fallback)
   - Supports both MP4 and GIF output formats

This frame-by-frame approach ensures low memory usage regardless of video length or resolution.

## Usage

### Basic Usage

```bash
py video_upscaler.py input_video.mp4
```

### Advanced Options

```bash
# AI upscaling with custom scale
py video_upscaler.py input.mp4 --method realesrgan --scale 4

# Fast hardware upscaling
py video_upscaler.py input.mp4 --method ffmpeg --scale 2

# Extract frames only
py video_upscaler.py input.mp4 --method extract

# Process existing frames
py video_upscaler.py input.mp4 --method process_existing --format gif

# Custom output path
py video_upscaler.py input.mp4 --output output.mp4
```

### Batch File Interface

Use the accompanying `video_upscaler.bat` for interactive prompts:

```cmd
./video_upscaler.bat
```

The batch file provides user-friendly prompts for all parameters with numbered options.

## Requirements

- Python 3.13
- FFmpeg (add to PATH or place in script directory)
- Real-ESRGAN Vulkan executable (included in realesrgan-windows/)
- OpenCV (optional, for frame verification)

## Directory Structure

```
video_upscaler/
├── video_upscaler.py          # Main script
├── realesrgan-windows/        # Real-ESRGAN Vulkan executable
│   ├── realesrgan-ncnn-vulkan.exe
│   └── models/
├── input/                     # Input video files
├── output/                    # Output videos and frame folders
└── README.md
```

## Output Management

- Videos are saved to `output/` directory with descriptive names
- Frame folders are created for Real-ESRGAN processing
- Cleanup prompts allow keeping or removing temporary frame data
- High-resolution videos automatically use CPU encoding to ensure compatibility

## Performance Notes

- Real-ESRGAN: Frame-by-frame processing, slower but highest quality
- FFmpeg: Hardware-accelerated when possible, fast processing
- Memory usage: Low due to sequential frame processing
- GPU requirements: AMD GPU with AMF support for hardware encoding

| Scale  | Method    | Processing Speed | Quality   |
| ------ | --------- | ---------------- | --------- |
| **2x** | AI EDSR   | ~5-10 fps        | Excellent |
| **3x** | AI EDSR   | ~2-5 fps         | Excellent |
| **4x** | AI EDSR   | ~1-3 fps         | Excellent |
| **2x** | Classical | ~15-30 fps       | Good      |
| **3x** | Classical | ~10-20 fps       | Good      |
| **4x** | Classical | ~5-15 fps        | Good      |

**Notes:**
- Speed depends on video resolution and hardware
- AI method provides better quality but slower
- Classical method is faster but less detailed
- Processing time = total_frames / fps

## 🎯 **Usage**

### **Basic Upscaling**
```cmd
py video_upscaler.py "input_video.mp4" --scale 4
```

### **Force Classical Method**
```cmd
py video_upscaler.py "input_video.mp4" --scale 4 --classical
```

### **Custom Output Path**
```cmd
py video_upscaler.py "input.mp4" --scale 2 --output "output_enhanced.mp4"
```

### **Scale Options**
- `2` - Double resolution (1920x1080 → 3840x2160)
- `3` - Triple resolution (1920x1080 → 5760x3240)
- `4` - Quadruple resolution (1920x1080 → 7680x4320)

## 🔧 **How It Works**

### **Video Processing Pipeline**
1. **Extract Frames:** OpenCV reads video frame-by-frame
2. **Enhance Each Frame:** Apply AI EDSR or classical enhancement
3. **Reassemble Video:** Write enhanced frames back to MP4
4. **Preserve Audio:** Original audio track maintained

### **AI Enhancement (EDSR)**
- Uses pre-trained EDSR super-resolution models
- Trained on high-quality image datasets
- Maintains details while reducing artifacts
- Automatic fallback to classical if model fails

### **Classical Enhancement**
- **Lanczos Upsampling:** High-quality interpolation
- **CLAHE:** Contrast enhancement in LAB color space
- **Unsharp Mask:** Edge sharpening without noise

## 📁 **Input/Output**

### **Supported Formats**
- **Input:** MP4, AVI, MOV, MKV, WMV
- **Output:** MP4 (H.264 codec)
- **Audio:** Preserved from original (if present)

### **File Naming**
- **Default:** `{original}_upscaled_x{scale}.mp4`
- **Custom:** Specify with `--output` parameter

### **Directory Structure**
```
video_upscaler/
├── input/           # Place input videos here
├── output/          # Enhanced videos saved here
└── models/          # EDSR model files
```

## ⚙️ **Configuration**

### **Video Writer Settings**
- **Codec:** H.264 (MP4)
- **FPS:** Preserved from original
- **Quality:** High quality encoding

### **Memory Usage**
- **Per Frame:** ~50-200MB depending on resolution
- **GPU Memory:** EDSR models use ~1-2GB VRAM
- **System RAM:** Scales with video resolution

## 🔧 **Troubleshooting**

### **"Module not found"**
```cmd
py -m pip install opencv-python
```

### **EDSR Models Missing**
```cmd
copy "..\image_upscaler\models\*" "models\"
```

### **Video Won't Open**
- Check file path and permissions
- Ensure video is not corrupted
- Try different video formats

### **Out of Memory**
- Use lower scale factor (2x instead of 4x)
- Use classical method (`--classical`)
- Process shorter video clips

### **Slow Processing**
- Use classical method for faster results
- Lower scale factor
- Close other applications

## 📈 **Comparison: Image vs Video Upscaling**

| Aspect         | Image Upscaler | Video Upscaler |
| -------------- | -------------- | -------------- |
| **Input**      | Single image   | Video file     |
| **Processing** | One image      | Frame-by-frame |
| **Time**       | Seconds        | Minutes/hours  |
| **Output**     | Enhanced image | Enhanced video |
| **Audio**      | N/A            | Preserved      |
| **Models**     | Same EDSR      | Same EDSR      |
| **Methods**    | AI + Classical | AI + Classical |

## 🎬 **Example Output**

```
======================================================================
🎬 Video Upscaling: sample_video.mp4
Scale: 4x | AI Mode: True
Output: sample_video_upscaled_x4.mp4
======================================================================

📊 Video Info:
   Resolution: 1920x1080
   FPS: 30.0
   Total frames: 900
   Duration: 30.0s (0.5 minutes)
   Target resolution: 7680x4320

⏳ Processing 900 frames...

[████████████████████████████████████████] 100.0% - Frame 900/900 ✅ 7680x4320

======================================================================
✅ VIDEO UPSCALING COMPLETE
======================================================================
Input: sample_video.mp4
Output: sample_video_upscaled_x4.mp4
Scale factor: 4x
Resolution: 1920x1080 → 7680x4320
Frames processed: 900/900
FPS: 30.0
Duration: 30.0s
======================================================================
```

## 🎯 **Use Cases**

- **Old Videos:** Restore low-resolution footage
- **Screen Recordings:** Enhance tutorial videos
- **Surveillance:** Improve CCTV footage quality
- **Animation:** Sharpen hand-drawn or CGI frames
- **Archival:** Restore damaged or compressed videos

## 📝 **Credits**

Built using:
- **OpenCV** - Computer vision and video processing
- **EDSR Models** - AI super-resolution from image upscaler
- **FFmpeg** - Video codec support