# Audio to Text Converter

Converts audio files (MP3, WAV, etc.) to text transcripts using OpenAI Whisper.

## Installation

1. Install Python dependencies:
   ```
   pip install openai-whisper torch
   ```

2. For GPU acceleration (optional, requires CUDA):
   ```
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## Usage

### Command Line
```bash
# Basic usage
py audio_to_text/audio_to_text.py path/to/audio.mp3

# Specify model size (larger = more accurate but slower)
py audio_to_text/audio_to_text.py path/to/audio.mp3 --model small

# Custom output directory
py audio_to_text/audio_to_text.py path/to/audio.mp3 --output-dir /path/to/output
```

### Batch File (Windows)
```cmd
audio_to_text.bat "path\to\audio.mp3"
audio_to_text.bat "path\to\audio.mp3" --model small
```

## Model Options

- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: Better accuracy
- `medium`: High accuracy
- `large`: Best accuracy, slowest

## Output

Transcripts are saved as `.txt` files in `output_transcripts/` directory with the format:
`{audio_filename}_transcript.txt`

## Dependencies

- Python 3.13
- openai-whisper
- torch
- pathlib (built-in)

## Notes

- First run may download the Whisper model (several hundred MB)
- GPU recommended for faster processing
- Supports various audio formats (MP3, WAV, M4A, etc.)
- Works offline once model is downloaded
- Processing time depends on audio length and model size (e.g., 30 seconds ~10-30 seconds on CPU)