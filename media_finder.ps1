param (
    [int]$TopCount = 100,
    [string]$RootPath = "C:\",
    [switch]$Help
)

if ($Help) {
    Write-Host "Media Finder Script Help (Optimized .NET EnumerateFiles)" -ForegroundColor Cyan
    Write-Host "Usage: .\media_finder.ps1 [-TopCount <int>] [-RootPath <string>] [-Help]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -TopCount <int>   : Number of top largest media files to find (default: 100)"
    Write-Host "  -RootPath <string>: Root directory to scan (default: C:\)"
    Write-Host "  -Help             : Show this help message"
    Write-Host ""
    Write-Host "Description: Uses optimized .NET EnumerateFiles to find largest media files 10-50x faster than Get-ChildItem."
    exit
}

$extensions = @('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.bmp', '.tiff', '.svg')
$excludedPaths = @("C:\Windows\", "C:\Program Files\", "C:\Program Files (x86)\", "C:\ProgramData\", "C:\System Volume Information\", "C:\$Recycle.Bin\")

Write-Host "=== OPTIMIZED MEDIA FINDER ===" -ForegroundColor Cyan
Write-Host "Scanning: $RootPath (looking for top $TopCount largest files)" -ForegroundColor Cyan
Write-Host "Device: 16-core CPU, 32GB RAM, 1.82TB disk" -ForegroundColor Gray
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
                if ($extensions -contains $ext) {
                    $file = [System.IO.FileInfo]::new($filePath)
                    $fileCount++
                    
                    # Report progress every 1000 files
                    if ($fileCount - $lastReport -ge 1000) {
                        $elapsed = $stopwatch.Elapsed.TotalSeconds
                        Write-Host "[$([math]::Round($elapsed, 1))s] Found $fileCount media files..." -ForegroundColor Gray
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

Write-Host ""
Write-Host "Scan complete in $([math]::Round($elapsed, 2))s - Found $fileCount media files total" -ForegroundColor Green
Write-Host "Extracting top $TopCount largest files..." -ForegroundColor Cyan
Write-Host ""

# Output largest first (reverse heap order)
$results = @($minHeap | Sort-Object -Property Length -Descending)

# Write all results to file
$allFilePath = "$pwd\Media Scanner\all_media_files.txt"
$results | ForEach-Object { "$($_.FullName) - $([math]::Round($_.Length / 1MB, 2)) MB" } | Out-File -FilePath $allFilePath -Encoding UTF8
Write-Host "Wrote results to $allFilePath" -ForegroundColor Green

# Generate deletion script with exact paths
$deleteScriptPath = "$pwd\Media Scanner\delete_top_media.ps1"
$deleteScript = @()
$deleteScript += "# Delete top $TopCount media files"
$deleteScript += "`$files = @("
foreach ($r in $results) {
    $escapedPath = $r.FullName -replace "'", "''"
    $deleteScript += "    '$escapedPath',"
}
if ($deleteScript.Count -gt 2) {
    $deleteScript[-1] = $deleteScript[-1] -replace ',$'
}
$deleteScript += ")"
$deleteScript += "Remove-Item `$files -Force -ErrorAction SilentlyContinue"
$deleteScript | Out-File -FilePath $deleteScriptPath -Encoding UTF8
Write-Host "Wrote deletion script to $deleteScriptPath" -ForegroundColor Green
Write-Host "Run this to delete all files: & '$deleteScriptPath'" -ForegroundColor Yellow

# Display top files
Write-Host "`nTop $TopCount largest media files:" -ForegroundColor Cyan
$rank = 1
foreach ($r in $results) {
    $sizeMB = [math]::Round($r.Length / 1MB, 2)
    Write-Host "$rank. [$sizeMB MB] $($r.FullName)" -ForegroundColor Yellow
    $rank++
}