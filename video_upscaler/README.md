# Video Upscaler and Sharpener

**AI-Powered Video Enhancement** - Upscale and sharpen videos using EDSR models or classical methods. Processes each frame individually for maximum quality.

## 🎯 **Features**

### **✅ AI Video Upscaling**
- **EDSR Models:** Uses the same AI models as image upscaler
- **Frame-by-Frame Processing:** Each video frame gets individual enhancement
- **Multiple Scales:** 2x, 3x, or 4x upscaling
- **Fallback Support:** Automatically falls back to classical methods if AI fails

### **⚡ Classical Enhancement**
- **CLAHE Contrast:** Adaptive contrast enhancement
- **Lanczos Interpolation:** High-quality upsampling
- **Unsharp Mask:** Intelligent sharpening without artifacts

### **📊 Progress Tracking**
- **Real-Time Progress:** Visual progress bar shows frame processing
- **Frame Counter:** Current frame / total frames
- **Resolution Display:** Shows input → output dimensions
- **Time Estimation:** Based on total frame count

## 🚀 **Setup**

### **Prerequisites**
- ✅ OpenCV installed (same as image upscaler)
- ✅ EDSR models (automatically copied from image_upscaler)
- ✅ FFmpeg (for video codec support)

### **Directory Structure**
```
video_upscaler/
├── video_upscaler.py    # Main script
├── models/             # EDSR model files
│   ├── EDSR_x2.pb
│   ├── EDSR_x3.pb
│   └── EDSR_x4.pb
├── input/              # Input videos
├── output/             # Enhanced videos
└── README.md          # This file
```

### **Models Setup**
Models are automatically copied from `../image_upscaler/models/`. If missing:
```cmd
copy "..\image_upscaler\models\*" "models\"
```

## 📊 **Performance**

| Scale | Method | Processing Speed | Quality |
| ----- | ------ | ---------------- | ------- |
| **2x** | AI EDSR | ~5-10 fps | Excellent |
| **3x** | AI EDSR | ~2-5 fps  | Excellent |
| **4x** | AI EDSR | ~1-3 fps  | Excellent |
| **2x** | Classical | ~15-30 fps | Good |
| **3x** | Classical | ~10-20 fps | Good |
| **4x** | Classical | ~5-15 fps | Good |

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

| Aspect | Image Upscaler | Video Upscaler |
| ------ | -------------- | -------------- |
| **Input** | Single image | Video file |
| **Processing** | One image | Frame-by-frame |
| **Time** | Seconds | Minutes/hours |
| **Output** | Enhanced image | Enhanced video |
| **Audio** | N/A | Preserved |
| **Models** | Same EDSR | Same EDSR |
| **Methods** | AI + Classical | AI + Classical |

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