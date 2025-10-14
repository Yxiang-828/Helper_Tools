# Professional Audio to Text Transcriber

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

### Simple Batch File (Recommended)
```cmd
mp3-to-txt.bat "path\to\audio_file.mp3"
```

### Command Line
```bash
py audio_to_text.py "path/to/audio.mp3"
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

## Credits

- **OpenAI Whisper**: Advanced speech recognition model (https://github.com/openai/whisper)
- **PyTorch**: Deep learning framework used by Whisper (https://pytorch.org/)