# Add Python Scripts to PATH
# Run this script with: powershell -ExecutionPolicy Bypass -File add_to_path.ps1

Write-Host "Adding Python Scripts to PATH..." -ForegroundColor Cyan

# Get current user PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Python Scripts directory
$pythonScripts = "C:\Users\user\AppData\Local\Programs\Python\Python313\Scripts"

# Check if already in PATH
if ($userPath -like "*$pythonScripts*") {
    Write-Host "Python Scripts is already in PATH!" -ForegroundColor Green
    Write-Host "Path: $pythonScripts" -ForegroundColor Yellow
} else {
    # Add to PATH
    Write-Host "Adding to PATH: $pythonScripts" -ForegroundColor Yellow
    $newPath = "$userPath;$pythonScripts"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    Write-Host "Successfully added to PATH!" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: You need to restart your terminal for changes to take effect." -ForegroundColor Red
    Write-Host ""
    Write-Host "After restarting, test with: termicode" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
