# Audio to Text Transcriber

Converts audio/video files to text transcripts using OpenAI Whisper.

## Setup (Required - Do This First)

1. **Run setup.bat** (from Audio_to_Text_Transcriber folder):
   ```
   cd Audio_to_Text_Transcriber
   setup.bat
   ```

2. **What setup.bat does**:
   - Installs PyTorch (CPU version)
   - Installs OpenAI Whisper
   - Asks if you want to download all models now (recommended)

3. **Download models?**
   - **Yes (recommended)**: Downloads all 5 models (~4GB total, takes 10-15 minutes)
   - **No**: Models download automatically when first used (slower first run)

## Usage

### Quick Start (Interactive)

```bash
# From helper_tools root directory
mp3-to-txt.bat "path/to/your/audio.mp3"
```

This will:
1. Ask you to choose language (English, Chinese, Japanese, Spanish, etc.)
2. Ask you to choose model (tiny/base/small/medium/large)
3. Ask for output directory (optional, defaults to Audio_to_Text_Transcriber/output_transcripts/)
4. Transcribe the audio and save as .md file

### Command Line (Advanced)

```bash
py audio_to_text.py "audio.mp3" --model large --language zh --output-dir "output/"
```

## Model Options

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| tiny | 39 MB | Fastest | Quick tests, low quality |
| base | 74 MB | Fast | Good balance (recommended) |
| small | 244 MB | Medium | Better accuracy |
| medium | 769 MB | Slow | High accuracy |
| large | 2.9 GB | Slowest | Best accuracy |

## Supported Languages

- English (en) - Recommended
- Chinese (zh)
- Japanese (ja)
- Spanish (es)
- French (fr)
- German (de)
- Korean (ko)
- Auto-detect

## Output

- **Format**: Markdown (.md) files
- **Location**: Audio_to_Text_Transcriber/output_transcripts/
- **Content**: Header with metadata + formatted transcript

## Requirements

- Python 3.7+
- FFmpeg (auto-detected)
- Internet for model downloads

### Manual Installation

If you prefer manual installation:

```bash
pip install openai-whisper torch
```

## Model Options

Choose a model based on your needs for speed, accuracy, and available hardware resources.

| Model | Disk Space | Relative Speed | Use Case |
|-------|------------|----------------|----------|
| tiny | 39 MB | Fastest | Minimal resource usage, suitable for quick tests or drafts |
| base | 74 MB | Fast | Balanced speed and accuracy for general-purpose transcription |
| small | 244 MB | Medium | Improved accuracy for clear audio like podcasts or lectures |
| medium | 769 MB | Slow | High accuracy for transcribing important content |
| large | 2.9 GB | Slowest | Highest accuracy for critical applications where precision is paramount |

**Note:** Models are downloaded automatically on first use. For faster startup, run `setup.bat` and choose to pre-download all models.

## Performance

Processing speed is dependent on the selected model and available hardware.

- GPU (CUDA): Approximately 3-8 seconds per 30 seconds of audio
- CPU: Approximately 10-30 seconds per 30 seconds of audio
- First Run: The script will download and cache the specified model. This is a one-time operation per model
- Memory Usage: Requires 2 GB to 8 GB of RAM, depending on the model size

## Output Format

- File Type: Transcripts are saved as Markdown files (.md) with proper formatting
- Naming Convention: Output files are named {original_filename}_transcript.md
- Content: Includes metadata header with file info, model used, language, and formatted transcript content

## Supported Formats

- Audio: mp3, wav, m4a, flac, ogg, aac
- Video: mp4, avi, mov, mkv (audio is extracted automatically)

## Troubleshooting

- CPU Mode: The tool works perfectly on CPU without CUDA. GPU acceleration is optional and only provides faster processing - CPU mode is normal and fully functional
- CUDA Acceleration: If you have an NVIDIA GPU and want faster processing, install the CUDA toolkit. Otherwise, CPU mode works fine (just slower)
- File not found: Use quotes around file paths, especially those containing spaces or special characters like &, (, ), etc.
- Special Characters: Paths with characters like & will be truncated if not properly quoted. Always use "path\to\file.mp3"
- Slow performance: Use a smaller model (e.g., --model small) for faster processing. Close other resource-intensive applications

## Credits

This tool is a wrapper for the powerful open-source technologies listed below.

- Engine: OpenAI Whisper
- Framework: PyTorch
- Audio Handling: FFmpeg