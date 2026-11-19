@echo off
rem Dua thay doi tren may em len GitHub. Anh truyen (samples, outputs, anh trong validation) va mo hinh
rem da bi chan trong .gitignore nen khong bi dua len. Khong xoa file nao.
title Day len GitHub - Xoa chu truyen tranh
cd /d "%~dp0"
where git >nul 2>nul
if errorlevel 1 (
  echo Chua cai Git. Tai o https://git-scm.com/download/win roi chay lai file nay.
  pause
  exit /b 1
)
if not exist ".git" (
  echo Thu muc chua noi voi GitHub. Chay "Noi Git.bat" truoc.
  pause
  exit /b 1
)
git add -A
git diff --cached --quiet
if not errorlevel 1 goto khong_moi
echo Cac file se duoc dua len:
git diff --cached --name-status
echo.
set "MSG="
set /p MSG="Ghi ngan gon da sua gi (Enter de dung loi mac dinh): "
if not defined MSG set "MSG=Cap nhat tu may em Minh Anh"
git commit -m "%MSG%"
goto keo_ve
:khong_moi
echo Khong co gi moi de commit.
:keo_ve
git pull --rebase origin main
if errorlevel 1 (
  echo.
  echo Co xung dot khi keo ban moi ve. Dang huy rebase, khong mat gi ca.
  git rebase --abort
  echo Chup man hinh cua so nay gui chi.
  pause
  exit /b 1
)
git push origin main
echo.
echo ==== Ket qua (dong dau phai la "## main...origin/main") ====
git status -sb
git log --oneline -3
pause
