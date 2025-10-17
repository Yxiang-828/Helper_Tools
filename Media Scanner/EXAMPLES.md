# 🎯 Universal File Scanner v2.0 - Usage Examples

## Basic Commands

### Default Scan (Media Files)
```powershell
.\media_finder.ps1
```
Scans `C:\` for top 100 largest media files (images + videos)

### Show Help
```powershell
.\media_finder.ps1 -Help
```

## 📁 Preset File Types

### 🎬 Video Files Only
```powershell
.\media_finder.ps1 -FileType video
```
Find: mp4, avi, mov, mkv, wmv, flv, webm, m4v, mpg, mpeg, 3gp, ogv

### 🖼️ Image Files Only
```powershell
.\media_finder.ps1 -FileType image
```
Find: png, jpg, jpeg, gif, bmp, tiff, svg, webp, ico, heic, raw

### 🎵 Audio Files
```powershell
.\media_finder.ps1 -FileType audio -TopCount 50
```
Find: mp3, wav, flac, aac, ogg, m4a, wma, opus, alac, ape

### 📄 Documents
```powershell
.\media_finder.ps1 -FileType document -RootPath "$env:USERPROFILE\Documents"
```
Find: pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, odt, ods, odp, rtf

### 📦 Archives
```powershell
.\media_finder.ps1 -FileType archive
```
Find: zip, rar, 7z, tar, gz, bz2, xz, iso, dmg

### 💻 Source Code
```powershell
.\media_finder.ps1 -FileType code -RootPath "D:\Projects"
```
Find: py, js, ts, cs, cpp, c, h, java, html, css, php, rb, go, rs

### 🎮 Game Files
```powershell
.\media_finder.ps1 -FileType game -RootPath "D:\Games"
```
Find: unity3d, pak, wad, bsa, esp, esm, vpk, gcf, dat, sav

### 🌐 All Files
```powershell
.\media_finder.ps1 -FileType all -TopCount 200
```
Scans **ALL** files regardless of extension

## 🔧 Custom Extensions

### Find Executables
```powershell
.\media_finder.ps1 -CustomExtensions @('.exe', '.msi', '.dll')
```

### Find Log Files
```powershell
.\media_finder.ps1 -CustomExtensions @('.log', '.txt') -RootPath "C:\Logs"
```

### Find Database Files
```powershell
.\media_finder.ps1 -CustomExtensions @('.db', '.sqlite', '.mdf', '.ldf')
```

### Find Virtual Machine Files
```powershell
.\media_finder.ps1 -CustomExtensions @('.vmdk', '.vdi', '.vhd', '.qcow2') -TopCount 20
```

## 🎯 Advanced Use Cases

### Clean Up Downloads Folder
```powershell
# Find large videos in Downloads
.\media_finder.ps1 -FileType video -RootPath "$env:USERPROFILE\Downloads" -TopCount 25
```

### Find Space Hogs in User Profile
```powershell
# Find all large files in your profile
.\media_finder.ps1 -FileType all -RootPath "$env:USERPROFILE" -TopCount 100
```

### Clean Game Installations
```powershell
# Find largest game assets
.\media_finder.ps1 -FileType game -RootPath "C:\Program Files (x86)\Steam" -TopCount 50
```

### Audit External Drive
```powershell
# Scan entire external drive for videos
.\media_finder.ps1 -FileType video -RootPath "E:\" -TopCount 100
```

### Find Large Archives for Cleanup
```powershell
# Find archives over a certain size
.\media_finder.ps1 -FileType archive -TopCount 30
```

### Development Cleanup
```powershell
# Find large source files
.\media_finder.ps1 -FileType code -RootPath "C:\Dev" -TopCount 50
```

## 🗑️ Interactive Deletion

After scanning, the script generates `delete_top_media.ps1`:

```powershell
# Run the deletion script
& "C:\Program Files (x86)\helper_tools\Media Scanner\delete_top_media.ps1"
```

Features:
- ✅ **Ask how many files to delete** (default: 14)
- ✅ **Preview files before deletion**
- ✅ **Confirmation prompt** (must type "YES")
- ✅ **Safe deletion with error handling**

## 💡 Pro Tips

### Combine with Task Scheduler
Create a scheduled task to scan weekly:
```powershell
# Weekly video cleanup scan
.\media_finder.ps1 -FileType video -TopCount 100
```

### Scan Multiple Drives
```powershell
# C: drive
.\media_finder.ps1 -FileType all -RootPath "C:\" -TopCount 100

# D: drive
.\media_finder.ps1 -FileType all -RootPath "D:\" -TopCount 100
```

### Quick Scans for Specific Areas
```powershell
# Only scan Downloads
.\media_finder.ps1 -RootPath "$env:USERPROFILE\Downloads"

# Only scan Desktop
.\media_finder.ps1 -RootPath "$env:USERPROFILE\Desktop"

# Only scan Documents
.\media_finder.ps1 -RootPath "$env:USERPROFILE\Documents"
```

## ⚡ Performance Notes

- **Speed**: Scans ~3,000 files/second on typical hardware
- **Memory**: Uses O(N) memory where N = TopCount (not total files!)
- **Algorithm**: Min-heap + BFS for optimal performance
- **Interruption**: Press `Ctrl+C` to safely stop scan

## 📊 Output Files

Generated in `Media Scanner/` directory:
- `all_media_files.txt` - Complete list of all found files
- `delete_top_media.ps1` - Interactive deletion script (gitignored)

Both files use UTF-8 encoding to handle special characters (™, 桌面, etc.)
