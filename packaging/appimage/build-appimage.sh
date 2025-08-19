#!/usr/bin/env bash
set -euo pipefail

APP=Kydras-eBook-Studio
ARCH=x86_64
APPDIR="$(pwd)/packaging/appimage/AppDir"

# Clean AppDir payload each time
rm -rf "$APPDIR/usr/src" || true
mkdir -p "$APPDIR/usr/src" "$APPDIR/usr/share/applications"

# Copy project sources into the AppDir
rsync -a --exclude '.git' \
  kydras_ebook_studio/ webui/ requirements.txt \
  "$APPDIR/usr/src/"

# Desktop file into AppDir
install -m644 packaging/appimage/kydras-ebook-studio.desktop \
  "$APPDIR/usr/share/applications/kydras-ebook-studio.desktop"

# Fetch builders (local, no install)
cd packaging/appimage
LD="linuxdeploy-${ARCH}.AppImage"
PYPLUG="linuxdeploy-plugin-python-${ARCH}.AppImage"
[ -x "$LD" ] || curl -L -o "$LD" "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-${ARCH}.AppImage"
[ -x "$PYPLUG" ] || curl -L -o "$PYPLUG" "https://github.com/linuxdeploy/linuxdeploy-plugin-python/releases/download/continuous/linuxdeploy-plugin-python-${ARCH}.AppImage"
chmod +x "$LD" "$PYPLUG"

# Build. The python plugin reads requirements.txt from the AppDir.
APPIMAGE_EXTRACT_AND_RUN=1 \
"./$LD" --appdir "$APPDIR" \
  -d "$APPDIR/usr/share/applications/kydras-ebook-studio.desktop" \
  -i "$APPDIR/usr/share/icons/hicolor/256x256/apps/kydras.png" \
  --output appimage \
  --plugin python

# Rename & move to dist/
mkdir -p ../../dist
mv ./*.AppImage "../../dist/${APP}-${ARCH}.AppImage"
echo "[ok] Built dist/${APP}-${ARCH}.AppImage"
