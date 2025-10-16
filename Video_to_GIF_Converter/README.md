# Video to GIF Converter

Convert MP4 videos to optimized GIFs with exact size and speed constraints.

## Usage

```bash
# Interactive mode
advanced_converter.bat

# Command line
python converter.py "video.mp4" -s 5 -p 1.0 -o "output.gif"
```

## Parameters

| Parameter | Description | Range | Example |
|-----------|-------------|-------|---------|
| `-s, --size` | Max file size (MB) | 1-50 | `-s 10` |
| `-p, --speed` | Playback speed ratio | 0.1-2.0 | `-p 0.5` |
| `-o, --output` | Output path | Optional | `-o result.gif` |

## How It Works

1. **Analysis**: Examines video properties (duration, resolution, frame rate)
2. **Optimization**: Automatically scales resolution/frame rate to meet constraints
3. **Validation**: Ensures output meets exact specifications

## Performance

- **Processing**: 10-60 seconds per video
- **File Sizes**: 1-50MB (recommended for web)
- **Speed Ratios**: 0.1x (slow) to 2.0x (fast)
- **Auto-scaling**: Resolution reduced to meet size limits

## Supported Formats

- **Input**: MP4, AVI, MOV, MKV, WebM
- **Output**: GIF (web-optimized)
- **Codecs**: H.264, H.265, VP8, VP9

## Requirements

- **Python**: 3.7+
- **Dependencies**: `pip install moviepy pillow`
- **Memory**: 4GB+ recommended for large videos
```

### Command Line Mode
```bash
# Basic conversion with 8MB limit
python converter.py "C:\Videos\demo.mp4" -s 8 -p 1.0

# Slow motion GIF (half speed, 5MB limit)
python converter.py "C:\Videos\demo.mp4" -s 5 -p 0.5 -o "slow_demo.gif"

# Fast motion GIF (double speed, 3MB limit)
python converter.py "C:\Videos\demo.mp4" -s 3 -p 2.0 -o "fast_demo.gif"
```

### Batch Processing
```bash
# Convert all MP4 files in current directory
for %f in (*.mp4) do python converter.py "%f" -s 5 -p 1.0
```

## Parameters Guide

| Parameter | Description | Range | Example |
|-----------|-------------|-------|---------|
| `-s, --size` | Maximum file size in MB | 1-50 | `-s 10` |
| `-p, --speed` | Playback speed ratio | 0.1-2.0 | `-p 0.5` |
| `-o, --output` | Output GIF path | Optional | `-o result.gif` |

## How It Works

### 1. Video Analysis
- Examines duration, frame rate, resolution, file size
- Calculates optimal compression parameters
- Validates your constraints are realistic

### 2. Smart Optimization
- **Resolution Scaling**: Automatically reduces resolution to meet size limits
- **Frame Rate Adjustment**: Optimizes FPS for smooth playback
- **Speed Control**: Adjusts playback speed without changing file size
- **Quality Preservation**: Maintains visual quality within constraints

### 3. Constraint Validation
- Ensures output meets your exact specifications
- Provides detailed compliance reporting
- Warns about unrealistic constraints

## Optimization Examples

### Size-Based Scaling
```
Input: 1920x1080 video, 50MB target
Output: 640x360 GIF, ~8MB actual size
Optimization: 75% resolution reduction, frame rate optimization
```

### Speed-Based Adjustment
```
Input: 10-second video at 1.0x speed
Output: 5-second GIF at 2.0x speed (same perceived duration)
Optimization: Faster playback, smaller file size
```

## Performance Guide

- **Processing Speed**: Most videos convert in 10-60 seconds
- **File Size Range**: 1MB-50MB recommended (browser-friendly)
- **Speed Ratios**: 0.1x (very slow) to 2.0x (very fast)
- **Resolution**: Automatically scaled down for smaller files

## Supported Formats

- **Input**: MP4, AVI, MOV, MKV, WebM
- **Output**: GIF (optimized for web compatibility)
- **Codecs**: H.264, H.265, VP8, VP9

## Troubleshooting

### "Size constraint too restrictive"
```
Solution: Increase size limit or reduce speed ratio
Example: Change from 2MB to 5MB, or 1.0x to 0.7x speed
```

### "Video analysis failed"
```
Solution: Ensure video file is not corrupted
Try: Different video file or check file permissions
```

### "Conversion too slow"
```
Solution: Use smaller size limits or shorter videos
Tip: 10MB limit typically processes 2-3x faster than 50MB
```

### Memory Issues
```
Solution: Close other applications
Tip: Videos over 1080p may need more RAM
```

## Technical Details

- **Engine**: MoviePy + PIL/Pillow
- **Algorithm**: Constraint-based optimization with dynamic scaling
- **Compression**: Intelligent frame rate and resolution adjustment
- **Validation**: Real-time constraint checking and reporting

## Use Cases

- 🎬 **Social Media**: Create shareable video clips
- 💼 **Presentations**: Convert demos to GIFs for slides
- 🎮 **Gaming**: Share gameplay highlights
- 📱 **Mobile**: Create app preview animations
- 🌐 **Web**: Optimize videos for websites
- 💬 **Communication**: Visual explanations and tutorials

## Advanced Tips

### Size Optimization
- Smaller size limits = faster processing
- Speed ratios < 1.0 often result in smaller files
- Very short videos may need higher size limits

### Quality Control
- Higher size limits preserve more detail
- Original speed (1.0x) maintains natural timing
- Test different settings to find your sweet spot

### Batch Processing
```bash
# Process multiple videos with different settings
python converter.py "video1.mp4" -s 5 -p 1.0 -o "out1.gif"
python converter.py "video2.mp4" -s 8 -p 0.8 -o "out2.gif"
```

## Credits

- **MoviePy**: https://zulko.github.io/moviepy/
- **Pillow (PIL)**: https://python-pillow.org/

---

**Ready to convert? Run `advanced_converter.bat` and create perfect GIFs instantly!** 🎬➡️🎨