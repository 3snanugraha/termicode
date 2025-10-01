@echo off
echo ============================================
echo  Termicode - Setup PATH
echo ============================================
echo.
echo Adding Python Scripts to PATH...
echo.

powershell -ExecutionPolicy Bypass -Command "$userPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $pythonScripts = 'C:\Users\user\AppData\Local\Programs\Python\Python313\Scripts'; if ($userPath -like \"*$pythonScripts*\") { Write-Host 'Already in PATH!' -ForegroundColor Green } else { $newPath = \"$userPath;$pythonScripts\"; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Write-Host 'Successfully added to PATH!' -ForegroundColor Green }"

echo.
echo ============================================
echo  IMPORTANT: Restart your terminal!
echo ============================================
echo.
echo After restarting, you can use: termicode
echo.
pause
