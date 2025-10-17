# Media Finder Script

This PowerShell script scans a specified directory (default: your user profile) for the largest media files (images and videos) and provides tools to manage them.

## What It Does

- Recursively scans the root directory for media files with extensions: .png, .jpg, .jpeg, .gif, .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .bmp, .tiff, .svg
- Sorts files by size (largest first) and selects the top N files
- Displays the top files in the terminal with ranks and sizes
- Generates two output files:
  - `all_media_files.txt`: Full list of found media files with sizes
  - `open_top_media.ps1`: Script to open the top files in their default applications with 3-second delays
- Automatically runs the open script to open the top files one by one

## How It's Done

1. Uses `Get-ChildItem -Recurse` to find all files in the root directory
2. Filters for media extensions and sorts by file length (size)
3. Takes the top N files
4. Outputs to files and terminal
5. Executes the generated open script

## Usage

Run the script from PowerShell:

```powershell
.\media_finder.ps1 -TopCount 10
```

### Parameters

- `-TopCount <int>`: Number of top files to find (default: 100)
- `-RootPath <string>`: Directory to scan (default: $env:USERPROFILE)
- `-Exclude <string[]>`: Paths to exclude (default: system dirs)
- `-OutMarkdown <string>`: Base name for output script (default: open_top_media.md -> .ps1)
- `-Help`: Show help message

### Examples

- Find top 10 largest media files in user profile:
  ```powershell
  .\media_finder.ps1 -TopCount 10
  ```

- Scan entire C: drive (warning: slow):
  ```powershell
  .\media_finder.ps1 -RootPath "C:\" -TopCount 50
  ```

- Get help:
  ```powershell
  .\media_finder.ps1 -Help
  ```

## Requirements

- PowerShell 5.1+
- Access to the directories being scanned

## Notes

- Scanning large directories can take time
- The open script checks if files exist before opening
- Files are opened with `Start-Process` in default apps</content>
<parameter name="filePath">c:\Users\xiang\Desktop\y2\media_tools\README.md