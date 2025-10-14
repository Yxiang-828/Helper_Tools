# Development Guidelines for Helper Tools

## Environment Setup
- **OS**: Windows
- **Terminal**: PowerShell
- **Python**: Version 3.13, command is `py` (not `python`)
- **Dependencies**: Install via pip, document in README
- **External Tools**: Like FFmpeg, extract to `C:\ffmpeg\bin`, use full paths in scripts to avoid PATH issues

## Project Structure
- **Root Directory**: All helper tools in subfolders (e.g., `cc_extractor/`, `mp4 to gif converter/`)
- **Batch Files**: Place in root directory for easy access, not in subfolders
- **Scripts**: Keep in their respective subfolders
- **Output Directories**: ALWAYS create outputs in the specific helper's subfolder (e.g., `cc_extractor/extracted_audio/`, `mp4 to gif converter/extracted_gifs/`)

## Coding Standards
- **Language**: Python 3.13
- **Imports**: Use `from pathlib import Path` for path handling
- **Error Handling**: Graceful failures, informative messages, no infinite loops
- **Timeouts**: Set reasonable timeouts for external commands (e.g., 300s for FFmpeg)
- **Comments**: Well-commented code, especially for complex logic
- **Modularity**: Separate functions for different tasks (e.g., extract_audio, extract_subtitles)

## Output Management
- **Default Output Path**: Use `Path(__file__).parent / "output_folder"` to ensure outputs go to the helper's directory
- **User-Specified Output**: Allow optional command-line argument for custom output directory
- **File Naming**: Descriptive names with timestamps if needed (e.g., `video_name.mp3`)
- **Cleanup**: No automatic cleanup unless specified

## Git and Version Control
- **.gitignore**: Include patterns for all output folders, temp files (*.tmp, *.log, *.bundle, *.png), __pycache__/
- **New Tools**: When developing new tools, immediately add .gitignore patterns for their output folders before generating any outputs
- **Commits**: Commit scripts and configs, not outputs
- **README**: Update with usage, dependencies, examples

## Batch File Best Practices
- **FFmpeg Check**: Use full path `"C:\ffmpeg\bin\ffmpeg.exe"` instead of relying on PATH
- **Error Checking**: Check %errorlevel% after commands
- **User Interaction**: Pause only on errors, exit immediately on success
- **Arguments**: Pass %* to Python scripts for flexible arguments

## Testing Protocol
- **Manual Testing**: Always test with sample inputs after changes
- **Edge Cases**: Test with missing files, invalid paths, no subtitles/audio
- **Output Verification**: Confirm files are created in correct locations
- **Performance**: Ensure no hanging, reasonable execution times

## Maintenance
- **Updates**: When modifying, update paths, outputs, and test thoroughly
- **Documentation**: Keep guidelines updated with new learnings
- **Consistency**: Follow these rules to avoid reminders and ensure reliability