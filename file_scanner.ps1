# ==============================================================================
# File Scanner - Find and Remove Large Files for Storage Optimization
# Copyright (c) 2025 Yxiang-828
# Licensed under the MIT License (see LICENSE file in repository root)
# ==============================================================================

param (
    [int]$TopCount = 100,
    [string]$RootPath = "C:\",
    [string]$FileType = "",
    [string[]]$CustomExtensions = @(),
    [switch]$Help
)

if ($Help) {
    $helpText = @"
╔═══════════════════════════════════════════════════════════════════╗
║          🚀 UNIVERSAL FILE SCANNER v2.0                          ║
║          Powered by .NET EnumerateFiles (10-50x faster!)         ║
╚═══════════════════════════════════════════════════════════════════╝

Usage: .\file_scanner.ps1 [-TopCount INT] [-RootPath PATH] [-FileType TYPE] [-CustomExtensions ARRAY] [-Help]

Parameters:
  -TopCount INT         : Number of largest files to find (default: 100)
  -RootPath PATH        : Root directory to scan (default: C:\)
  -FileType TYPE        : Use a preset group (see below)
  -CustomExtensions     : Custom extensions, e.g. @('.exe', '.dll')
  -Help                 : Show this help message

Preset File Types:
  media      - Videos and images (mp4, avi, mov, jpg, png, gif, etc.) [DEFAULT]
  video      - Video files only (mp4, avi, mov, mkv, wmv, flv, webm)
  image      - Image files only (jpg, png, gif, bmp, tiff, svg, webp)
  audio      - Audio files (mp3, wav, flac, aac, ogg, m4a, wma)
  document   - Documents (pdf, docx, xlsx, pptx, txt, md, odt)
  archive    - Archives (zip, rar, 7z, tar, gz, bz2)
  code       - Source code (py, js, cs, cpp, java, html, css)
  game       - Game-related (unity3d, pak, wad, bsa, esp, esm)
  all        - All files (no filtering)

Examples:
  .\file_scanner.ps1                                     # Scan C:\ for top 100 media files
  .\file_scanner.ps1 -FileType video                     # Videos only
  .\file_scanner.ps1 -FileType audio -TopCount 50        # Top 50 audio files
  .\file_scanner.ps1 -CustomExtensions @('.exe','.msi')  # Custom file types
  .\file_scanner.ps1 -RootPath 'D:\Games' -FileType game # Scan D:\Games for game files

"@
    Write-Host $helpText -ForegroundColor Cyan
    exit
}

# Define preset file type groups
$presets = @{
    media    = @('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg')
    video    = @('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv')
    image    = @('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.heic', '.raw')
    audio    = @('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus', '.alac', '.ape')
    document = @('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.odt', '.ods', '.odp', '.rtf')
    archive  = @('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg')
    code     = @('.py', '.js', '.ts', '.cs', '.cpp', '.c', '.h', '.java', '.html', '.css', '.php', '.rb', '.go', '.rs')
    game     = @('.unity3d', '.pak', '.wad', '.bsa', '.esp', '.esm', '.vpk', '.gcf', '.dat', '.sav')
    all      = @('*')
}

# Determine which extensions to use
if ($CustomExtensions.Count -gt 0) {
    $extensions = $CustomExtensions
    $typeLabel = "Custom Types"
} elseif ($FileType -and $presets.ContainsKey($FileType.ToLower())) {
    $extensions = $presets[$FileType.ToLower()]
    $typeLabel = "$($FileType.ToUpper()) Files"
} else {
    # Default to media files
    $extensions = $presets['media']
    $typeLabel = "MEDIA Files"
}
$excludedPaths = @("C:\Windows\", "C:\Program Files\", "C:\Program Files (x86)\", "C:\ProgramData\", "C:\System Volume Information\", "C:\$Recycle.Bin\")

# Display banner
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    UNIVERSAL FILE SCANNER v2.0" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Scan Root    : " -NoNewline -ForegroundColor Yellow
Write-Host $RootPath -ForegroundColor White
Write-Host "Target Type  : " -NoNewline -ForegroundColor Yellow
Write-Host $typeLabel -ForegroundColor White
Write-Host "Top Count    : " -NoNewline -ForegroundColor Yellow
Write-Host $TopCount -ForegroundColor White
Write-Host "Extensions   : " -NoNewline -ForegroundColor Yellow
Write-Host ($extensions -join ', ') -ForegroundColor Gray
Write-Host "Device Specs : " -NoNewline -ForegroundColor Yellow
Write-Host "16-core CPU, 32GB RAM, 1.82TB disk" -ForegroundColor Gray
Write-Host ""
Write-Host "Starting blazing-fast .NET scan..." -ForegroundColor Green
Write-Host ""

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$fileCount = 0
$lastReport = 0

# Min-heap comparer (ascending order - keeps smallest in collection)
$minHeap = [System.Collections.Generic.SortedSet[object]]::new(
    [System.Collections.Generic.Comparer[object]]::Create({
        param($a, $b)
        $a.Length.CompareTo($b.Length)
    })
)

$queue = [System.Collections.Generic.Queue[string]]::new()
$queue.Enqueue($RootPath)

while ($queue.Count -gt 0) {
    $currentPath = $queue.Dequeue()
    
    # Skip excluded paths
    $skip = $false
    foreach ($excluded in $excludedPaths) {
        if ($currentPath.StartsWith($excluded, [StringComparison]::OrdinalIgnoreCase)) {
            $skip = $true
            break
        }
    }
    if ($skip) { continue }
    
    try {
        # Add subdirectories to queue (BFS approach)
        foreach ($dir in [System.IO.Directory]::EnumerateDirectories($currentPath)) {
            $queue.Enqueue($dir)
        }
        
        # Process files with .NET EnumerateFiles (10x faster than Get-ChildItem)
        foreach ($filePath in [System.IO.Directory]::EnumerateFiles($currentPath)) {
            try {
                $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
                
                # Fast extension check BEFORE creating FileInfo object
                # Special case: 'all' preset matches everything
                if ($extensions -contains '*' -or $extensions -contains $ext) {
                    $file = [System.IO.FileInfo]::new($filePath)
                    $fileCount++
                    
                    # Report progress every 1000 files
                    if ($fileCount - $lastReport -ge 1000) {
                        $elapsed = $stopwatch.Elapsed.TotalSeconds
                        $rate = [math]::Round($fileCount / $elapsed, 0)
                        Write-Host "[$([math]::Round($elapsed, 1))s] Found $fileCount files | Scanning at $rate files/sec..." -ForegroundColor Gray
                        $lastReport = $fileCount
                    }
                    
                    # Maintain min-heap of top N files
                    if ($minHeap.Count -lt $TopCount) {
                        [void]$minHeap.Add([PSCustomObject]@{
                            FullName = $file.FullName
                            Length = $file.Length
                        })
                    }
                    elseif ($file.Length -gt $minHeap.Min.Length) {
                        [void]$minHeap.Remove($minHeap.Min)
                        [void]$minHeap.Add([PSCustomObject]@{
                            FullName = $file.FullName
                            Length = $file.Length
                        })
                    }
                }
            } catch { }
        }
    } catch { }
}

$stopwatch.Stop()
$elapsed = $stopwatch.Elapsed.TotalSeconds
$rate = [math]::Round($fileCount / $elapsed, 0)

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "          SCAN COMPLETE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Time Elapsed   : " -NoNewline -ForegroundColor Yellow
Write-Host "$([math]::Round($elapsed, 2))s" -ForegroundColor White
Write-Host "Files Found    : " -NoNewline -ForegroundColor Yellow
Write-Host "$fileCount $typeLabel" -ForegroundColor White
Write-Host "Scan Rate      : " -NoNewline -ForegroundColor Yellow
Write-Host "$rate files/sec" -ForegroundColor White
Write-Host "Extracting top : " -NoNewline -ForegroundColor Yellow
Write-Host "$TopCount largest files..." -ForegroundColor White
Write-Host ""

# Output largest first (reverse heap order)
$results = @($minHeap | Sort-Object -Property Length -Descending)

# Calculate total size
$totalSize = ($results | Measure-Object -Property Length -Sum).Sum
$totalSizeGB = [math]::Round($totalSize / 1GB, 2)
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

# Write all results to file
$scannerDir = "$pwd\File_Scanner"
if (-not (Test-Path $scannerDir)) {
    New-Item -ItemType Directory -Path $scannerDir -Force | Out-Null
}

$allFilePath = "$scannerDir\all_media_files.txt"
$results | ForEach-Object { "$($_.FullName) - $([math]::Round($_.Length / 1MB, 2)) MB" } | Out-File -FilePath $allFilePath -Encoding UTF8
Write-Host "💾 Saved full list : " -NoNewline -ForegroundColor Yellow; Write-Host $allFilePath -ForegroundColor Gray

# Generate interactive deletion script
$deleteScriptPath = "$scannerDir\delete_top_media.ps1"
$deleteScriptContent = @"
# Interactive Deletion Script for top $typeLabel
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

`$files = @(
"@

foreach ($r in $results) {
    $escapedPath = $r.FullName -replace "'", "''"
    $sizeMB = [math]::Round($r.Length / 1MB, 2)
    $deleteScriptContent += "`n    '$escapedPath', # $sizeMB MB"
}

$deleteScriptContent = $deleteScriptContent -replace ', # [0-9.]+ MB$', ' # Last entry'
$deleteScriptContent += @"

)

Write-Host '================================================' -ForegroundColor Red
Write-Host '     INTERACTIVE FILE DELETION TOOL' -ForegroundColor Red
Write-Host '================================================' -ForegroundColor Red
Write-Host ''
Write-Host 'Total files available: ' -NoNewline -ForegroundColor Yellow
Write-Host `$files.Count -ForegroundColor White
Write-Host ''
`$count = Read-Host 'How many files to delete? (1-'+`$files.Count+', default=14)'
if ([string]::IsNullOrWhiteSpace(`$count)) { `$count = 14 }
`$count = [int]`$count
if (`$count -lt 1 -or `$count -gt `$files.Count) {
    Write-Host 'Invalid count. Exiting.' -ForegroundColor Red
    exit
}

Write-Host ''
Write-Host 'Files to be deleted:' -ForegroundColor Yellow
for (`$i = 0; `$i -lt `$count; `$i++) {
    Write-Host "  [`$(`$i+1)] `$(`$files[`$i])" -ForegroundColor Gray
}
Write-Host ''
`$confirm = Read-Host 'Type YES to confirm deletion'
if (`$confirm -ne 'YES') {
    Write-Host 'Deletion cancelled.' -ForegroundColor Yellow
    exit
}

Write-Host ''
Write-Host 'Deleting files...' -ForegroundColor Red
for (`$i = 0; `$i -lt `$count; `$i++) {
    if (Test-Path `$files[`$i]) {
        Remove-Item `$files[`$i] -Force
        Write-Host "  [OK] Deleted: `$(`$files[`$i])" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] Not found: `$(`$files[`$i])" -ForegroundColor Yellow
    }
}
Write-Host ''
Write-Host 'Deletion complete!' -ForegroundColor Green
"@

$deleteScriptContent | Out-File -FilePath $deleteScriptPath -Encoding UTF8
Write-Host "Saved delete script: " -NoNewline -ForegroundColor Yellow
Write-Host $deleteScriptPath -ForegroundColor Gray

# Display summary and top files
Write-Host ""
Write-Host "================================================" -ForegroundColor Magenta
Write-Host "            RESULTS SUMMARY" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta
Write-Host ""
if ($totalSizeGB -ge 1) {
    Write-Host "Total Size (Top $TopCount): " -NoNewline -ForegroundColor Yellow
    Write-Host "$totalSizeGB GB" -ForegroundColor White
} else {
    Write-Host "Total Size (Top $TopCount): " -NoNewline -ForegroundColor Yellow
    Write-Host "$totalSizeMB MB" -ForegroundColor White
}
Write-Host ""
Write-Host "Top $TopCount largest files:" -ForegroundColor Cyan
Write-Host ""
$rank = 1
foreach ($r in $results) {
    $sizeMB = [math]::Round($r.Length / 1MB, 2)
    $sizeGB = [math]::Round($r.Length / 1GB, 2)
    $fileName = [System.IO.Path]::GetFileName($r.FullName)
    
    if ($sizeGB -ge 1) {
        Write-Host "  $rank. " -NoNewline -ForegroundColor Gray
        Write-Host "($sizeGB GB) " -NoNewline -ForegroundColor Green
    } else {
        Write-Host "  $rank. " -NoNewline -ForegroundColor Gray
        Write-Host "($sizeMB MB) " -NoNewline -ForegroundColor Yellow
    }
    Write-Host $fileName -NoNewline -ForegroundColor White
    Write-Host " -> $($r.FullName)" -ForegroundColor DarkGray
    $rank++
}
Write-Host ""
Write-Host "Tip: Run the delete script to interactively remove files!" -ForegroundColor Cyan
Write-Host "Command: & `"$deleteScriptPath`"" -ForegroundColor Gray
Write-Host ""