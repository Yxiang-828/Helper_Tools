# Frame to Video/GIF Converter

A quick tool to combine image frames from a folder into MP4 or GIF files with GPU acceleration support.

## Features

- **GPU Acceleration**: Uses OpenCV with OpenCL for fast MP4 creation on AMD GPUs
- **Multiple Formats**: Supports PNG, JPG, JPEG, BMP, TIFF image formats
- **Smart Sorting**: Automatically sorts frames by filename for proper sequence
- **Progress Updates**: Shows real-time progress during conversion
- **Flexible Output**: Choose between MP4 (GPU-accelerated) or GIF (optimized)

## Quick Start

### Windows (Recommended)
```batch
# From helper_tools root directory
frame_to_video.bat
```

### Python Direct
```bash
cd Frame_to_Video_Converter
python frame_to_video.py
```

### Command Line
```bash
# MP4 output
python frame_to_video.py "path/to/frames" -f mp4 -fps 30

# GIF output
python frame_to_video.py "path/to/frames" -f gif -fps 24 -o "output.gif"
```

## Timing Control

Choose between two timing modes:

### FPS Mode (Frames Per Second)
```bash
python frame_to_video.py "frames/" -f mp4 -fps 30
```
- **24 FPS**: Cinematic, smooth playback
- **30 FPS**: Standard video, most compatible
- **60 FPS**: Very smooth, larger files

### Duration Mode (Milliseconds Per Frame)
```bash
python frame_to_video.py "frames/" -f gif -d 100
```
- **100-200ms**: Slow, detailed viewing (presentations, tutorials)
- **50-100ms**: Moderate speed (balanced viewing)
- **20-50ms**: Fast, video-like (animations, time-lapse)

## Timing Tips

### Based on Duration:
- **≥200ms**: Perfect for educational content, each frame clearly visible
- **100-199ms**: Good balance, slideshow feel
- **50-99ms**: Quick transitions, video-like
- **<50ms**: Very fast, almost smooth video

### Based on FPS:
- **≥60 FPS**: Ultra-smooth, high file sizes
- **30-59 FPS**: Standard video quality
- **24-29 FPS**: Cinematic/film quality
- **<24 FPS**: Stop-motion effect

## Examples

```bash
# Slow presentation (2 seconds per frame)
python frame_to_video.py "slides/" -f gif -d 2000

# Standard video (30 FPS)
python frame_to_video.py "frames/" -f mp4 -fps 30

# Fast animation (50ms per frame)
python frame_to_video.py "animation/" -f mp4 -d 50
```