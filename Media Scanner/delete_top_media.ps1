# Delete top N media files (user specified)
Write-Host "=== DELETE TOP LARGEST MEDIA FILES ===" -ForegroundColor Cyan
Write-Host "This script contains 73 largest media files found on your system." -ForegroundColor Yellow
Write-Host ""

# Ask user how many to delete
$deleteCount = Read-Host "How many of the top largest files do you want to delete? (1-73, default: 14)"
if ([string]::IsNullOrWhiteSpace($deleteCount)) {
    $deleteCount = 14
}
$deleteCount = [int]$deleteCount

if ($deleteCount -lt 1 -or $deleteCount -gt 73) {
    Write-Host "Invalid number. Must be between 1 and 73." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "You chose to delete the top $deleteCount largest files." -ForegroundColor Yellow
Write-Host ""

$allFiles = @(
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 06-23-38.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 04-22-48.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 08-24-07.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-08 20-42-19.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 03-34-58.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 03-23-27.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R5RUOJ6.gif',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RPWIVLM.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-07 19-36-39.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-07 19-33-14.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-07 19-30-23.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R09S62P.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R1CFL44.png',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R4K5TID.mp4',
    'C:\Users\xiang\Downloads\Telegram Desktop\endgame.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-07 19-28-41.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 03-22-07.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\prophecy 140m.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-04 03-20-44.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\b1   2024-09-07 09-25-13.mp4',
    'C:\Users\xiang\Videos\New folder\ai final (2).mp4',
    'C:\Users\xiang\Videos\New folder\AI FINAL.mp4',
    'C:\Users\xiang\Videos\New folder\REM.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\Event_20001_01.mp4',
    'C:\Users\xiang\Videos\Overwolf\Insights Capture\Wuthering Waves 05-28-2025_2-41-24-917.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\b1   2024-09-07 09-41-39.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R4Z3GXU.gif',
    'C:\Users\xiang\Anchor\Anchor\AnchorPanic_Data\GameRes\extra\video\ui\update_res_cg.mp4',
    'C:\Users\xiang\OneDrive\done donedone - Made with Clipchamp_1719166011335.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_02_01_EP01.mp4',
    'C:\Users\xiang\OneDrive\chef''s kiss - Made with Clipchamp_1719157027000.mp4',
    'C:\Users\xiang\OneDrive\桌面\ai hoshino good raw - Made with Clipchamp_1719143483309.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\b1   2024-09-07 09-30-33.mp4',
    'C:\Users\xiang\Documents\saber power.mp4',
    'C:\Users\xiang\Music\Captures\Baldur''s Gate 3 (2560x1440) - (DX11) - (6 + 6 WT) 2024-01-13 14-56-15.mp4',
    'C:\Users\xiang\Downloads\20610_Aorin_UR_MaxSkill_CutIn.gif',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_03_12_EP01.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_01_01_EP01.mp4',
    'C:\Users\xiang\Downloads\graded fail 3x3.MOV',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$R02GH5S.gif',
    'C:\Users\xiang\Pictures\Screenshots\Captures\ELDEN RING™ 2024-12-08 22-16-00.mp4',
    'C:\Users\xiang\Videos\New folder\TensorPix - mp4-1280.mp4',
    'C:\Users\xiang\Downloads\9.5wheel slow!.MOV',
    'C:\Users\xiang\Music\Captures\Wuthering Waves   2024-05-25 01-24-07.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RSL1KMY.png',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\Event_30001_12.mp4',
    'C:\Users\xiang\Pictures\Screenshots\Captures\b1   2024-09-07 09-32-16.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\videos\jp\toupiao.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_01_01_EP04.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\Windows\videos\en\1_0_pv.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\videos\jp\1_0_pv.mp4',
    'C:\Users\xiang\Downloads\final run completed with ta block.MOV',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_07_16_EP01.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_02_09_EP05.mp4',
    'C:\Users\xiang\AppData\Roaming\Opera Software\Opera GX Stable\Default\Extensions\mnkkglfmiilbekidalchanbiebnpffci\1.0_0\wallpaper\video.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\Video\Event_50001_01.mp4',
    'C:\Users\xiang\AppData\Roaming\Opera Software\Opera GX Stable\Default\Extensions\nffcalnpgakjpnpgdjjbgiokimffjpin\1.1_0\wallpaper\video.mp4',
    'C:\Users\xiang\AppData\Local\Temp\tmpgj13dflg\upscaled\frame_000031.png',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RJR73C3.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\Video\Event_20001_01.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\videos\jp\s01_pv.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\videos\en\s01_pv.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RL9NG3M.gif',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RY8APP0.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\videos\2_4_activity_04.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\Event_30001_02.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RZFRWJJ.mp4',
    'C:\Reverse1999en\reverse1999_Data\StreamingAssets\Windows\videos\1_9_pv.mp4',
    'C:\Users\xiang\Music\Captures\Speed Dial - Opera 2024-05-04 15-43-38.mp4',
    'C:\Users\xiang\Documents\trysnb\ExportedProject\Assets\StreamingAssets\HQ\Video\MainLevel_04_15_EP01.mp4',
    'C:\$Recycle.Bin\S-1-5-21-3262764739-2563264561-764020362-1001\$RE2JC1H.png',
    'C:\Users\xiang\Videos\Overwolf\Insights Capture\Highlight - Valorant - Match 1 - 1207am.mp4',
    'C:\Users\xiang\Downloads\GoSleep.gif'
)

# Select only the top N files to delete
$files = $allFiles | Select-Object -First $deleteCount

Write-Host "Files to be deleted:" -ForegroundColor Red
for ($i = 0; $i -lt $files.Count; $i++) {
    Write-Host "$($i+1). $($files[$i])" -ForegroundColor Yellow
}

Write-Host ""
$confirm = Read-Host "Are you sure you want to delete these $deleteCount files? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Deletion cancelled." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Deleting $deleteCount files..." -ForegroundColor Red
Remove-Item $files -Force -ErrorAction SilentlyContinue
Write-Host "Done! Deleted $deleteCount files." -ForegroundColor Green
