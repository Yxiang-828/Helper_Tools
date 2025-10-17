# Helper Tools Collection

**Personal CLI tools for advanced developers. Fast, offline media processing. Not for casual users.**

## Why Helper Tools?

I built this for myself and fellow developers who understand code. These are power-user tools that assume programming knowledge and command-line comfort. Not beginner-friendly - designed for those who can read and modify source code.

- Fast: CLI tools that process in seconds
- Offline: No internet required after setup
- No Ads: Pure functionality
- CLI: Command-line interfaces for automation
- Focused: Each tool does one thing well
- Minimal: Few dependencies

**Rule**: If it requires a browser or takes >30 seconds to set up, it's not included.

## Contents

- [Audio to Text Transcriber](#audio-to-text-transcriber)
- [Video to GIF Converter](#video-to-gif-converter)
- [Video Subtitle & MP3 Extractor](#video-subtitle--mp3-extractor)
- [AMD GPU Image Upscaler](#amd-gpu-image-upscaler)
- [AMD GPU Video Upscaler](#amd-gpu-video-upscaler)
- [Git Auto-Push](#git-auto-push)
- [Unity Image Extractor](#unity-image-extractor)

## Available Tools

### Audio to Text Transcriber
Convert audio files to text transcripts using OpenAI Whisper

Turns MP3, WAV, M4A into searchable text. Works offline after model download.

```bash
mp3-to-txt.bat "path\to\audio.mp3"
```

Features:
- Multiple AI models (tiny to large)
- GPU acceleration (3-5x faster)
- 99+ languages
- Batch processing

Setup: `pip install openai-whisper torch`

[Full Documentation](Audio_to_Text_Transcriber/README.md)

---

### Video to GIF Converter
Convert MP4 videos to optimized GIFs with size/speed constraints

Creates GIFs with exact file size and playback speed limits.

```bash
mp4togif.bat
```

Features:
- Size constraint optimization
- Speed ratio control
- Automatic resolution adjustment
- Interactive interface

Setup: `pip install moviepy pillow`

[Full Documentation](Video_to_GIF_Converter/README.md)

---

### Video Subtitle & MP3 Extractor
Extracts subtitles AND MP3 audio from videos.

What it does:
- Extracts embedded subtitle tracks as SRT files
- Always extracts audio as MP3
- Produces both outputs when subtitles exist
- Produces MP3 audio when no subtitles exist

```bash
extract_cc.bat "path\to\video.mp4"
```

Setup: FFmpeg required

[Full Documentation](Video-subtitle&mp3-extractor/README.md)

---

### AMD GPU Image Upscaler
AI-powered image enhancement with AMD GPU acceleration

Upscales and sharpens images using Real-ESRGAN and EDSR models.

```bash
image_upscaler.bat
```

Features:
- Real-ESRGAN and EDSR models
- 2x, 3x, 4x scaling
- AMD GPU optimized
- Vulkan acceleration

Setup: Models download automatically

[Full Documentation](image_upscaler/README.md)

---

### AMD GPU Video Upscaler
AI-powered video enhancement with AMD GPU acceleration

Upscales videos using Real-ESRGAN AI or fast FFmpeg methods, optimized for AMD GPUs.

```bash
video_upscaler.bat
```

Features:
- Real-ESRGAN AI upscaling (frame-by-frame)
- FFmpeg hardware encoding with AMD VCE
- 2x, 3x, 4x scaling
- MP4 and GIF output
- Automatic CPU fallback for high resolution
- Audio preservation

Setup: FFmpeg and Real-ESRGAN Vulkan required

[Full Documentation](video_upscaler/README.md)

---

### Git Auto-Push
Fast git workflow without commit hassle

Auto-commits and pushes all changes with timestamps for tracking. Skip the commit message drama.

```bash
pushgit.bat
# or with custom message:
pushgit.bat "my changes"
```

Features:
- Automatic timestamp tracking
- One-command push workflow
- No staging required
- Maintains change history

Setup: Git repository required

### Unity Image Extractor
Extract images from Unity3D bundle files

Scans Unity game files for embedded textures and sprites, extracts them as PNG images.

```bash
extract_unity.bat "path\to\unity3d_file_or_directory"
```

Features:
- Extracts Texture2D and Sprite assets
- Recursive directory scanning
- PNG output format
- Preserves source organization

Setup: `pip install UnityPy Pillow`

## Where Do My Files Go?

Each tool saves outputs in predictable locations:

- Audio Transcripts → `Audio_to_Text_Transcriber/output_transcripts/`
- GIFs → `Video_to_GIF_Converter/extracted_gifs/`
- Subtitles → `Video-subtitle&mp3-extractor/extracted_captions/`
- MP3 Audio → `Video-subtitle&mp3-extractor/extracted_audio/`
- Upscaled Images → `image_upscaler/output/`
- Unity Images → `Unity_Image_Extractor/extracted_images/`

All outputs include the original filename with descriptive suffixes.

---

## Quick Start

1. Clone or download this repository
2. Pick your tool from the list above
3. Install dependencies (most tools need `pip install`)
4. Run the batch file
5. Specify your input files

## System Requirements

- OS: Windows 10/11
- Python: 3.7+
- Hardware: Modern CPU/GPU recommended
- Storage: 2-5GB for AI models

## Design Philosophy

### Speed First
Every tool is optimized for performance. Results in seconds, not minutes.

### Offline by Default
No internet required for core functionality. AI models download once and work forever.

### CLI Superiority
Command-line interfaces enable automation, scripting, and integration.

### Minimal Dependencies
Each tool uses as few external libraries as possible.

### Cross-Platform Ready
While currently Windows-focused, all tools are designed to work on Linux/Mac with minimal changes.

## Personal Project

This is a personal collection of tools I built for my own development workflow. Not accepting external contributions or feature requests. Use at your own risk - these tools are designed for advanced developers who can troubleshoot and modify code.

## License

All tools are provided as-is for personal use only. No warranties, no support. Each tool may have its own license - check individual READMEs.

---

Built for me. By me. For developers like me.</content>
<parameter name="filePath">c:\Program Files (x86)\helper_tools\README.md