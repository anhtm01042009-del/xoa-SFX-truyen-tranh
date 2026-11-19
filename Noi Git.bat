@echo off
rem Noi thu muc nay voi repo GitHub (chay 1 lan). Khong xoa file nao.
title Noi Git - Xoa chu truyen tranh
cd /d "%~dp0"
where git >nul 2>nul
if errorlevel 1 (
  echo Chua cai Git. Tai o https://git-scm.com/download/win roi chay lai file nay.
  pause
  exit /b 1
)
if exist ".git" (
  echo Thu muc nay da co git roi.
  git status
  pause
  exit /b 0
)
git init -b main
git remote add origin https://github.com/anhtm01042009-del/xoa-SFX-truyen-tranh.git
git fetch origin main
git reset --mixed origin/main
git branch -u origin/main
echo.
echo Xong. Trang thai thu muc so voi GitHub:
git status
pause
