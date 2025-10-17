# Audio to Text Transcriber

**Built specifically for MY AMD RX GPU on Windows** - This tool is designed exclusively for MY AMD Radeon RX 6000/7000/8000 series GPU using DirectML acceleration on MY Windows 10/11 system.

## 🎯 **Narrow Constraints - Built For MY Device**

This setup is **purposefully restrictive** and only works on:
- **MY AMD Radeon RX 6000/7000/8000 series** (MY RX 6800 XT)
- **MY Windows 10/11 native** (no WSL, no Linux, no macOS)
- **MY DirectML execution provider** (Microsoft's Windows-only GPU API)
- **MY Python 3.13** (specifically tested version)

> Similar setups may work if you have the exact same AMD GPU and Windows version, but no guarantees.
>
**Will NOT work on:**
- ❌ NVIDIA GPUs (requires CUDA)
- ❌ Intel GPUs (different DirectML implementation)
- ❌ AMD GPUs on Linux (requires ROCm)
- ❌ Any other OS (DirectML = Windows only)
- ❌ Python versions other than 3.13

You will have to modify the code yourself to run on other hardware or OS.

**Why these constraints?** MY DirectML is Microsoft's proprietary GPU acceleration API that only supports specific AMD GPU series on Windows. This tool embraces these limitations to provide reliable GPU acceleration without CUDA/ROCm complexity.

## 🚀 **Setup (MY AMD RX + Windows Only)**

### **Prerequisites**
- ✅ AMD Radeon RX 6000/7000/8000 series GPU
- ✅ Windows 10/11 (native)
- ✅ Python 3.13.x installed
- ✅ FFmpeg in PATH

### **One-Command Setup**
```cmd
cd "C:\Program Files (x86)\helper_tools\Audio_to_Text_Transcriber"
setup.bat
```

**What setup.bat does:**
1. Verifies Python 3.13.x
2. Installs PyTorch (CPU version)
3. Installs ONNX Runtime DirectML (AMD GPU acceleration)
4. Installs Optimum (ONNX optimization)
5. Installs Librosa (audio processing)
6. Verifies DirectML GPU acceleration
7. Optional: Pre-downloads Whisper models

### **Verify Setup Success**
```cmd
py -c "import onnxruntime as ort; print('DirectML working:', 'DmlExecutionProvider' in ort.get_available_providers())"
```
**Expected:** `DirectML working: True`

## 🔧 **Troubleshooting (MY AMD RX + Windows Only)**

### **"DmlExecutionProvider not available"**
```cmd
# Fix: Reinstall DirectML
py -m pip uninstall onnxruntime-directml -y
py -m pip install onnxruntime-directml --force-reinstall
```

### **"Module not found" errors**
```cmd
# Update pip and reinstall all
py -m pip install --upgrade pip
py -m pip install onnxruntime-directml optimum[onnxruntime] librosa --force-reinstall
```

### **AMD GPU not detected**
- Update AMD drivers via AMD Adrenalin software
- Ensure GPU is not in power-saving mode
- Check Windows Device Manager for GPU status

### **Python version issues**
- Must use MY Python 3.13 (3.13.0+)
- Check with: `py --version`
- If wrong version: reinstall Python 3.13

## 📊 **Performance (MY AMD RX 6800 XT + DirectML)**

| Model      | First Run | Cached Runs | VRAM Usage | Use Case        |
| ---------- | --------- | ----------- | ---------- | --------------- |
| **tiny**   | 5-10 sec  | 2-3 sec     | ~1GB       | Testing/fast    |
| **base**   | 10-20 sec | 3-5 sec     | ~2GB       | **Recommended** |
| **small**  | 30-60 sec | 8-12 sec    | ~4GB       | Better accuracy |
| **medium** | 2-3 min   | 15-25 sec   | ~8GB       | High accuracy   |
| **large**  | 3-5 min   | 30-60 sec   | ~16GB      | Best accuracy   |

**Notes:**
- Times are for 30 seconds of audio
- First run = ONNX conversion (one-time cost)
- DirectML provides 3-5x speedup vs CPU
- Models cache automatically after first use

## � **New Features (v2.0) - Long Audio Support**

### **✅ Full Audio Processing**
- **Before:** Only processed first 30 seconds (Whisper token limit)
- **Now:** Handles complete 20+ minute audio files by chunking
- **Method:** Splits audio into 30-second segments, processes each on GPU, concatenates results

### **📊 Real-Time Progress Tracking**
- **Visual Progress Bar:** `[████████░░░░░░░░░░░░░░░░░░░░░░] 50.0% - Chunk 21/42 (30.0s audio)`
- **Per-Chunk Timing:** Shows processing time for each 30-second segment
- **GPU Confirmation:** Displays "DirectML provider loaded successfully"

### **⚡ GPU Optimization**
- **Input Features to GPU:** Moves audio features to DirectML device before model.generate()
- **Reduced CPU Load:** CPU drops from 70% to 20-30%, GPU increases to 70-80%
- **Faster Processing:** ~15x real-time factor (2 seconds per 30-second chunk)

### **📈 Enhanced Output Metadata**
Transcripts now include:
- **Duration:** Total audio length in seconds and minutes
- **Chunks Processed:** Number of 30-second segments
- **Total Processing Time:** End-to-end transcription time
- **Real-Time Factor:** Processing speed relative to audio duration
- **GPU Acceleration:** Confirms DirectML usage

### **Example Output**
```
======================================================================
✅ TRANSCRIPTION COMPLETE
======================================================================
Total time: 85.42s
Audio duration: 1242.8s (20.7 minutes)
Average per chunk: 2.03s
Real-time factor: 0.07x (lower is faster)
Total characters: 18547
======================================================================
```

## �🎯 **Usage (AMD RX + Windows Only)**

### **Interactive Mode (Recommended)**
```cmd
# From helper_tools root
mp3-to-txt.bat "path/to/audio.mp3"
```
Choose language, model, and output directory interactively.

### **Command Line**
```cmd
py audio_to_text.py "audio.mp3" --model base --language en
```

### **Model Options**
| Model  | Size   | Speed   | Use Case        |
| ------ | ------ | ------- | --------------- |
| tiny   | 39 MB  | Fastest | Quick tests     |
| base   | 74 MB  | Fast    | **Recommended** |
| small  | 244 MB | Medium  | Better accuracy |
| medium | 769 MB | Slow    | High accuracy   |
| large  | 2.9 GB | Slowest | Best accuracy   |

### **Supported Languages**
- `en` - English (recommended)
- `zh` - Chinese
- `ja` - Japanese
- `es` - Spanish
- `fr` - French
- `de` - German
- `ko` - Korean
- `auto` - Auto-detect

### **Output**
- Markdown files in `output_transcripts/`
- Metadata header + formatted transcript
- Filename: `{original}_transcript.md`

## Output Format

- File Type: Transcripts are saved as Markdown files (.md) with proper formatting
- Naming Convention: Output files are named {original_filename}_transcript.md
- Content: Includes metadata header with file info, model used, language, and formatted transcript content

## Supported Formats

## Supported Formats

- **Audio**: mp3, wav, m4a, flac, ogg, aac
- **Video**: mp4, avi, mov, mkv (audio extracted automatically)

## Credits

Built specifically for AMD RX GPU on Windows using:
- **OpenAI Whisper** - Speech recognition engine
- **ONNX Runtime DirectML** - AMD GPU acceleration
- **Optimum** - ONNX model optimization
- **FFmpeg** - Audio/video processing