@echo off
chcp 65001 >nul
rem Tao bieu tuong "Xoa chu truyen tranh" ngoai man hinh chinh (Desktop). Chay 1 lan la du.
set "APP=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$d=[Environment]::GetFolderPath('Desktop'); $s=(New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $d 'Xoa chu truyen tranh.lnk')); $s.TargetPath='pyw.exe'; $s.Arguments='-3.12 src\app.py'; $s.WorkingDirectory='%APP%'; $s.IconLocation='%APP%assets\icon.ico'; $s.Description='Xoa chu truyen tranh'; $s.Save(); Write-Host ('Da tao: ' + $d + '\Xoa chu truyen tranh.lnk')"
echo.
echo Xong. Ra man hinh chinh bam doi "Xoa chu truyen tranh" de mo app.
pause
