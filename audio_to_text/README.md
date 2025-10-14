# Audio to Text Converter

Converts audio files (MP3, WAV, etc.) to text transcripts using Google Speech Recognition API.

## Installation

1. Install Python dependencies:
   ```
   pip install speechrecognition pydub
   ```

## Usage

### Command Line
```bash
# Basic usage
py audio_to_text/audio_to_text.py path/to/audio.mp3

# Custom output directory
py audio_to_text/audio_to_text.py path/to/audio.mp3 --output-dir /path/to/output
```

### Batch File (Windows)
```cmd
audio_to_text.bat "path\to\audio.mp3"
```

## Output

Transcripts are saved as `.txt` files in `output_transcripts/` directory with the format:
`{audio_filename}_transcript.txt`

## Dependencies

- Python 3.13
- speechrecognition
- pydub
- pathlib (built-in)

## Notes

- Uses Google Speech Recognition API (free, but has daily limits)
- Converts audio to WAV temporarily for better processing
- Internet connection required
- Best results with clear speech and minimal background noise