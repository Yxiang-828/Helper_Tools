# Audio to Text Transcriber

**Convert audio files to accurate text transcripts using OpenAI Whisper - completely offline after initial setup**

Transform MP3, WAV, M4A, and other audio formats into searchable, editable text. Perfect for content creators, researchers, students, and anyone who needs to transcribe audio content quickly and accurately.

## ⚡ Key Features

- 🎯 **Multiple AI Models**: Choose from tiny (fast) to large (most accurate)
- 🚀 **GPU Acceleration**: CUDA support for 3-5x faster processing
- 📁 **Batch Processing**: Convert multiple files automatically
- 🔍 **Smart Detection**: Handles various audio formats and qualities
- 💾 **Offline Operation**: Works without internet after model download
- 📝 **Clean Output**: Well-formatted transcripts with timestamps

## Quick Start

```bash
# Install dependencies (one-time)
pip install openai-whisper torch

# Basic transcription (downloads base model ~150MB)
py audio_to_text.py "path\to\your\audio.mp3"

# High accuracy mode (downloads large model ~3GB)
py audio_to_text.py "path\to\your\audio.mp3" --model large
```

## Installation

### Option 1: Basic Setup (Recommended)
```bash
pip install openai-whisper torch
```

### Option 2: GPU Acceleration (Faster)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install openai-whisper
```

**First run will download the AI model (150MB-3GB depending on model size)**

## Usage Examples

### Interactive Mode (Windows)
```cmd
REM Basic transcription
audio_to_text.bat "C:\Audio\lecture.mp3"

REM High accuracy for important content
audio_to_text.bat "C:\Audio\interview.mp3" --model large

REM Custom output directory
audio_to_text.bat "C:\Audio\podcast.mp3" --output-dir "C:\Transcripts"
```

### Command Line Mode
```bash
# Basic usage
python audio_to_text.py "audio.mp3"

# Specify model size
python audio_to_text.py "audio.mp3" --model small

# Custom output location
python audio_to_text.py "audio.mp3" --output-dir "/path/to/transcripts"
```

### Batch Processing
```bash
# Process all MP3 files in a directory
for %f in (*.mp3) do audio_to_text.bat "%f"
```

## Model Options

| Model | Size | Accuracy | Speed | Use Case |
|-------|------|----------|-------|----------|
| `tiny` | 39MB | Basic | ⚡⚡⚡ | Quick drafts, noisy audio |
| `base` | 74MB | Good | ⚡⚡ | General use, meetings |
| `small` | 244MB | Better | ⚡ | Podcasts, lectures |
| `medium` | 769MB | High | 🐌 | Important content |
| `large` | 2.9GB | Best | 🐌🐌 | Critical accuracy needed |

## Output Format

Transcripts are saved as UTF-8 text files:
```
{filename}_transcript.txt
```

**Example output:**
```
audio_transcript.txt
├── Contains full transcription
├── Automatic punctuation
├── Speaker identification (when available)
└── Timestamp information
```

## Performance Guide

- **CPU Processing**: 30 seconds of audio ≈ 10-30 seconds processing time
- **GPU Processing**: 30 seconds of audio ≈ 3-8 seconds processing time
- **Model Download**: First run downloads model (one-time, 150MB-3GB)
- **Memory Usage**: 2-8GB RAM depending on model size

## Supported Formats

- **Audio**: MP3, WAV, M4A, FLAC, OGG, AAC
- **Video**: MP4, AVI, MOV, MKV (audio extracted automatically)
- **Sample Rates**: Any (automatically resampled if needed)

## Troubleshooting

### "Model download failed"
- Check internet connection
- Use a smaller model (`--model tiny`) for testing
- Models are cached locally after first download

### "CUDA not available"
- Install CUDA toolkit: https://developer.nvidia.com/cuda-downloads
- Or use CPU mode (slower but works)

### "Audio file not found"
- Use quotes around paths with spaces
- Check file extension is supported
- Verify file is not corrupted

### Performance Issues
- Use smaller models for faster processing
- Close other applications to free RAM
- GPU mode requires NVIDIA GPU with CUDA

## Technical Details

- **Engine**: OpenAI Whisper (state-of-the-art speech recognition)
- **Architecture**: Transformer-based neural network
- **Languages**: 99+ languages supported
- **Accuracy**: Up to 95% on clear audio
- **Dependencies**: PyTorch, NumPy, FFmpeg (auto-handled)

## Use Cases

- 📚 **Education**: Lecture transcriptions, study materials
- 🎙️ **Podcasting**: Episode transcripts, SEO optimization
- 💼 **Business**: Meeting notes, interview records
- 🎵 **Music**: Lyrics transcription, audio analysis
- 🎬 **Media**: Video captioning, content creation
- 🔬 **Research**: Audio data analysis, documentation

## Credits

- **OpenAI Whisper**: https://github.com/openai/whisper
- **PyTorch**: https://pytorch.org/
- **FFmpeg**: Audio processing backend

---

**Ready to transcribe? Run `audio_to_text.bat` and start converting audio to text instantly!** 🎵➡️📝