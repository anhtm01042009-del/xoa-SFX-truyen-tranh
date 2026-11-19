@echo off
REM Mo giao dien xoa chu. Can da chay cai_dat.bat mot lan.
cd /d "%~dp0"
py -3.12 src\app.py
if errorlevel 1 (
  echo.
  echo CO LOI. Chup man hinh gui cho Claude.
  pause
)
