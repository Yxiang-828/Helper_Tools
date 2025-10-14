# Professional Video to GIF Converter

A sophisticated Python tool that converts MP4 videos to optimized GIFs with custom size and speed constraints.

## Features

- 🎯 **Custom Constraints**: Set maximum file size and speed ratio limits
- 🔍 **Smart Analysis**: Automatically analyzes video properties (duration, FPS, resolution)
- ⚡ **Automatic Optimization**: Calculates optimal FPS and resolution to meet your constraints
- ✅ **Constraint Validation**: Ensures output meets your specified limits
- 📊 **Detailed Reporting**: Shows conversion results and constraint compliance
- 🖥️ **Dual Interface**: Interactive mode and command-line support

## Requirements

- Python 3.6+
- MoviePy
- Pillow (PIL)
- NumPy (automatically installed with MoviePy)

## Installation

1. Install required packages:
```bash
pip install moviepy pillow
```

## Usage

### Interactive Mode (Recommended)

Run the converter and follow the prompts:

```bash
# Windows
advanced_converter.bat

# Or directly
python advanced_gif_converter.py
```

The script will ask for:
- **Video path**: Full path to your MP4 file
- **Size limit**: Maximum file size in MB (e.g., 10)
- **Speed ratio**: Playback speed (1.0 = original, 0.5 = half speed, 2.0 = double speed)

### Command Line Mode

For automation or scripting:

```bash
python advanced_gif_converter.py "path/to/video.mp4" -s 10 -p 1.0 -o "output.gif"
```

Parameters:
- `input`: Path to MP4 file (required)
- `-s, --size`: Size limit in MB (required)
- `-p, --speed`: Speed ratio (required)
- `-o, --output`: Output GIF path (optional)

## Examples

### Basic Conversion (Interactive)
```
Enter MP4 video path: C:\Videos\my_video.mp4
Enter size limit (MB, e.g., 10): 10
Enter speed ratio (0.1-2.0, 1.0 = original speed): 1.0
```

### Command Line
```bash
# Convert with 8MB limit, original speed
python advanced_gif_converter.py "C:\Videos\demo.mp4" -s 8 -p 1.0

# Convert with 5MB limit, half speed
python advanced_gif_converter.py "C:\Videos\demo.mp4" -s 5 -p 0.5 -o "slow_demo.gif"
```

## How It Works

1. **Analysis**: Examines video duration, frame rate, resolution, and file size
2. **Constraint Validation**: Checks if your requirements are realistic
3. **Optimization**: Calculates best FPS and resolution combination
4. **Conversion**: Creates GIF with optimized settings
5. **Verification**: Confirms output meets constraints

## Constraint Guidelines

- **Size Limits**: 1-50 MB recommended (GIFs over 10MB may not play well in browsers)
- **Speed Ratios**: 0.1-2.0 (1.0 = original speed)
- **Resolution**: Automatically scaled down if needed
- **Frame Rate**: Reduced to meet size constraints while maintaining smoothness

## Output Information

After conversion, you'll see:
- ✅ File size and constraint compliance
- ✅ Speed ratio achieved
- ✅ Frame count and FPS
- ✅ Resolution used

## Troubleshooting

### Common Issues

**"Size constraint too restrictive"**
- Try increasing the size limit or reducing speed ratio
- Very short videos may need higher size limits

**"Video analysis failed"**
- Ensure the MP4 file is not corrupted
- Check file path (use quotes for paths with spaces)

**"Conversion failed"**
- Verify MoviePy and dependencies are installed
- Check available disk space
- Try a smaller video first

### Performance Tips

- Larger videos take longer to process
- Higher resolution = larger file sizes
- Higher FPS = smoother animation but larger files
- Speed ratios < 1.0 (slower) often result in smaller files

## Technical Details

- Uses MoviePy for video processing
- PIL/Pillow for GIF optimization
- Automatic frame rate and resolution calculation
- Constraint-based optimization algorithm
- Comprehensive error handling and validation

## License

This tool is provided as-is for personal and educational use.

## Credits

- **MoviePy**: Python library for video editing and processing (https://zulko.github.io/moviepy/)
- **FFmpeg**: Used by MoviePy for video processing (https://ffmpeg.org/)
- **Pillow (PIL)**: Python Imaging Library for image processing (https://python-pillow.org/)