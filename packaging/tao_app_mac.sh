#!/bin/bash
# Dung XoaChuTruyenTranh.app tu thu muc onedir cua PyInstaller (dist/XoaChuTruyenTranh), roi ky ad-hoc.
# Chay tu thu muc goc du an, tren Mac, sau khi da chay pyinstaller.
set -euo pipefail
SRC=dist/XoaChuTruyenTranh
APP=dist/XoaChuTruyenTranh.app
VER=$(python -c "import sys; sys.path.insert(0,'src'); from phien_ban import __version__; print(__version__)")

rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
# File chay o Contents/MacOS; thu vien (_internal, nguyen khoi, khong tach) o Contents/Resources,
# MacOS/_internal la lien ket sang do. codesign khong chap nhan thu muc *.dist-info nam trong MacOS.
cp "$SRC/XoaChuTruyenTranh" "$APP/Contents/MacOS/"
cp -R "$SRC/_internal" "$APP/Contents/Resources/_internal"
ln -s ../Resources/_internal "$APP/Contents/MacOS/_internal"
python - <<PY
from PIL import Image
Image.open("assets/icon.ico").save("$APP/Contents/Resources/icon.icns")
PY
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key><string>XoaChuTruyenTranh</string>
  <key>CFBundleIdentifier</key><string>io.github.anhtm01042009-del.xoachutruyentranh</string>
  <key>CFBundleName</key><string>XoaChuTruyenTranh</string>
  <key>CFBundleDisplayName</key><string>Xóa chữ truyện tranh</string>
  <key>CFBundleIconFile</key><string>icon.icns</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>$VER</string>
  <key>CFBundleVersion</key><string>$VER</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST
codesign --force --sign - "$APP"
codesign --verify --verbose=2 "$APP" && echo "Da dung va ky ad-hoc: $APP ($VER)"
