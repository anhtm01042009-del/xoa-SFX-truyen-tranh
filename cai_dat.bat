@echo off
REM Cai thu vien va tai mo hinh (chay mot lan). Can Python 3.12 (lenh: py -3.12).
cd /d "%~dp0"
py -3.12 -m pip install -r src\requirements.txt
if errorlevel 1 goto loi
py -3.12 src\tai_mo_hinh.py
if errorlevel 1 goto loi
echo.
echo XONG. Co the chay chay_thu.bat
goto het
:loi
echo.
echo CO LOI. Chup man hinh gui cho Claude.
:het
pause
