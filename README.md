# Helper Tools Collection

**Personal CLI tools for advanced developers. Fast, offline media processing. Not for casual users.**

## Why Helper Tools?

I built this for myself and fellow developers who understand code. These are power-user tools that assume programming knowledge and command-line comfort. Not beginner-friendly - designed for those who can read and modify source code.

- 🚀 **Fast**: CLI tools that process in seconds
- 🔒 **Offline**: No internet required after setup
- 🛡️ **No Ads**: Pure functionality
- 💻 **CLI**: Command-line interfaces for automation
- 🎯 **Focused**: Each tool does one thing well
- 📦 **Minimal**: Few dependencies

**Rule**: If it requires a browser or takes >30 seconds to set up, it's not included.

## Available Tools

### 🎵 Audio to Text Transcriber
**Convert audio files to text transcripts using OpenAI Whisper**

Turns MP3, WAV, M4A into searchable text. Works offline after model download.

```bash
mp3-to-txt.bat "path\to\audio.mp3"
```

**Features:**
- Multiple AI models (tiny to large)
- GPU acceleration (3-5x faster)
- 99+ languages
- Batch processing

**Setup:** `pip install openai-whisper torch`

📖 **[Full Documentation](Audio_to_Text_Transcriber/README.md)**

---

### 🎬 Video to GIF Converter
**Convert MP4 videos to optimized GIFs with size/speed constraints**

Creates GIFs with exact file size and playback speed limits.

```bash
mp4togif.bat
```

**Features:**
- Size constraint optimization
- Speed ratio control
- Automatic resolution adjustment
- Interactive interface

**Setup:** `pip install moviepy pillow`

📖 **[Full Documentation](Video_to_GIF_Converter/README.md)**

---

### 📝 Video Subtitle Extractor
**Extract subtitles and audio from videos**

Pulls embedded captions and audio tracks from video files.

```bash
extract_cc.bat
```

**Features:**
- Multiple subtitle format support
- Audio track extraction
- Batch processing
- FFmpeg integration

**Setup:** FFmpeg executable required

📖 **[Full Documentation](Video-subtitle&mp3-extractor/README.md)**

---

### 🖼️ AMD GPU Image Upscaler
**AI-powered image enhancement with AMD GPU acceleration**

Upscales and sharpens images using Real-ESRGAN and EDSR models.

```bash
image_upscaler.bat
```

**Features:**
- Real-ESRGAN and EDSR models
- 2x, 3x, 4x scaling
- AMD GPU optimized
- Vulkan acceleration

**Setup:** Models download automatically

**Setup:** Python + AI models (automatic download)

📖 **[Full Documentation](image_upscaler/README.md)**

---

## 📂 Where Do My Files Go?

Don't worry about hunting for your processed files - each tool saves outputs in predictable locations:

- **🎵 Audio Transcripts** → `Audio_to_Text_Transcriber/output_transcripts/`
- **🎬 GIFs** → `Video_to_GIF_Converter/extracted_gifs/`
- **📝 Subtitles** → `Video-subtitle&mp3-extractor/extracted_captions/`
- **🖼️ Upscaled Images** → `image_upscaler/output/`

**Pro Tip**: All outputs include the original filename with descriptive suffixes (like `_realesrgan_x4.png` or `_transcript.txt`)

---

## Quick Start Guide

Getting started is dead simple:

1. **Grab the repo** - clone or download this repository
2. **Pick your tool** - see which one matches what you need above
3. **Install stuff** - most tools just need `pip install` commands
4. **Run the batch file** - double-click the `.bat` file or run it from command line
5. **Drop your files** - drag & drop or specify paths, and you're done!

Seriously, that's it. No complicated setup, no endless configuration. Just works.

## System Requirements

Don't worry, we kept the requirements minimal so you can actually use these tools:

- **OS:** Windows 10/11 (Linux/Mac versions coming soon)
- **Python:** 3.7+ (most tools - already installed on many systems)
- **Hardware:** Modern CPU/GPU recommended but not required
- **Storage:** 2-5GB for AI models (downloaded automatically on first use)

**Bottom line:** If you have a computer from the last 5 years, you're probably good to go.

## Our Design Philosophy

We built these tools with a clear vision - cut through the noise and deliver results. Here's what drives every decision:

### ⚡ Speed First
Every tool is optimized for performance. If it takes more than a few seconds, we broke something. No loading screens, no progress bars that lie, just fast results.

### 🔒 Offline by Default
No internet required for core functionality. AI models download once and work forever. Your data stays on your machine where it belongs.

### 💻 CLI Superiority
Command-line interfaces aren't old-school - they're power-user tools that enable automation, scripting, and integration. Drag & drop works too, but the CLI is where the real magic happens.

### 🎯 Minimal Dependencies
Each tool uses as few external libraries as possible. No bloated frameworks, no dependency hell, no "install 47 packages to run hello world."

### 🌍 Cross-Platform Ready
While currently Windows-focused, all tools are designed to work on Linux/Mac with minimal changes. One codebase, multiple platforms.

## Personal Project

This is a personal collection of tools I built for my own development workflow. Not accepting external contributions or feature requests. Use at your own risk - these tools are designed for advanced developers who can troubleshoot and modify code.

## License

All tools are provided as-is for personal use only. No warranties, no support. Each tool may have its own license - check individual READMEs.

---

**Built for me. By me. For developers like me.** ⚡</content>
<parameter name="filePath">c:\Program Files (x86)\helper_tools\README.md