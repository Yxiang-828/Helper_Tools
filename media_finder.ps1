param (
    [int]$TopCount = 100,
    [string]$RootPath = "$env:USERPROFILE",
    [string[]]$Exclude = @("C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\ProgramData"),
    [string]$OutMarkdown = "$pwd\Media Finder\open_top_media.md",
    [switch]$Help
)

if ($Help) {
    Write-Host "Media Finder Script Help" -ForegroundColor Cyan
    Write-Host "Usage: .\media_finder.ps1 [-TopCount <int>] [-RootPath <string>] [-Exclude <string[]>] [-OutMarkdown <string>] [-Help]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -TopCount <int>      : Number of top largest media files to find (default: 100)"
    Write-Host "  -RootPath <string>   : Root directory to scan (default: %USERPROFILE%)"
    Write-Host "  -Exclude <string[]>  : Array of paths to exclude (default: Windows/Program Files dirs)"
    Write-Host "  -OutMarkdown <string>: Output file for open script (default: open_top_media.md -> .ps1)"
    Write-Host "  -Help                : Show this help message"
    Write-Host ""
    Write-Host "Description: Scans for largest media files (.mp4, .mov, etc.), displays top N, generates open script, and auto-opens them."
    exit
}

# Define media file extensions
$extensions = @('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.bmp', '.tiff', '.svg')

Write-Host "Searching under: $RootPath (top $TopCount files)" -ForegroundColor Cyan

# Collect all media files using recursive search
Write-Host "Searching for media files recursively under: $RootPath" -ForegroundColor Cyan

$allFiles = Get-ChildItem -Path $RootPath -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.FullName -and $extensions -contains $_.Extension.ToLower() } | Sort-Object Length -Descending | Select-Object -First $TopCount

# Since we take top N directly, results are already sorted
$results = $allFiles

# Write all found media files to a file (but since we only have top N, write those)
$allFilePath = "$pwd\Media Finder\all_media_files.txt"
$results | ForEach-Object { "$($_.FullName) - $([math]::Round($_.Length / 1MB, 2)) MB" } | Out-File -FilePath $allFilePath -Encoding UTF8
Write-Host "Wrote top media files to $allFilePath" -ForegroundColor Green
$psScript = @()
$psScript += "# Open top $TopCount media files in default applications"
$psScript += ""
$rank = 1
foreach ($r in $results) {
    $psScript += "# Rank $rank - Size: $([math]::Round($r.Length / 1MB, 2)) MB"
    $psScript += "if (Test-Path '$($r.FullName)') { Start-Process '$($r.FullName)'; Start-Sleep 3 } else { Write-Host 'File not found: $($r.FullName)' }"
    $psScript += ""
    $rank++
}

# Change output file to .ps1
$OutScript = $OutMarkdown -replace '\.md$', '.ps1'
$psScript | Out-File -FilePath $OutScript -Encoding UTF8
Write-Host "Wrote open script to $OutScript (run it to open files in default apps)" -ForegroundColor Green

# Auto display top media files
Write-Host "`nTop $TopCount media files found:" -ForegroundColor Cyan
$rank = 1
foreach ($r in $results) {
    Write-Host "$rank. $($r.FullName) - $([math]::Round($r.Length / 1MB, 2)) MB" -ForegroundColor Yellow
    $rank++
}

# Auto-open the top files by running the generated script
# Write-Host "`nAuto-opening top $TopCount media files one by one with 3-second delays..." -ForegroundColor Green
# & $OutScript