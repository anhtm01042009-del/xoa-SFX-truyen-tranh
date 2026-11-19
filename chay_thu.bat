@echo off
REM Xoa chu tren 1 anh. Dung: chay_thu.bat samples\ten-anh.png
REM (hoac keo tha file anh len file chay_thu.bat). Ket qua nam trong outputs\may-em
cd /d "%~dp0"
if "%~1"=="" (
  echo Thieu ten anh. Vi du: chay_thu.bat samples\ten-anh.png
  pause
  exit /b 1
)
py -3.12 src\m0_clean.py --input "%~1" --out outputs\may-em --detector models\ctd_seg.onnx --lama models\big-lama.pt --dilate 11 --save-mask
echo.
echo Xong. Chup man hinh dong chu {"file": ...} o tren gui cho Claude.
pause
