#!/bin/bash
set -e

# Manhattan Project: ISO Build Script
# This script automates building a custom Ubuntu-based ISO for the Sanitization Engine.
# It requires root privileges and a modern Ubuntu/Debian host.

# --- CONFIG ---
ISO_NAME="ManhattanSanitizationBootableV1.0.iso"
BASE_ISO_URL="https://releases.ubuntu.com/22.04/ubuntu-22.04.4-live-server-amd64.iso"
BASE_ISO="ubuntu-base.iso"
WORK_DIR="/tmp/manhattan_iso_build"
EXTRACT_DIR="$WORK_DIR/extract"
CUSTOM_DIR="$WORK_DIR/custom"
FINAL_ISO="$PWD/$ISO_NAME"
GUI_SRC_DIR="$PWD/../gui"

# --- PREPARE ---
echo "[1/7] Cleaning up old build..."
sudo rm -rf "$WORK_DIR"
mkdir -p "$EXTRACT_DIR" "$CUSTOM_DIR"

# --- DOWNLOAD BASE ISO ---
echo "[2/7] Downloading base ISO..."
wget -O "$WORK_DIR/$BASE_ISO" "$BASE_ISO_URL"

# --- EXTRACT ISO ---
echo "[3/7] Extracting ISO..."
sudo 7z x "$WORK_DIR/$BASE_ISO" -o"$EXTRACT_DIR"

# --- CHROOT & CUSTOMIZE ---
echo "[4/7] Preparing chroot for customization..."
sudo cp -r "$EXTRACT_DIR/casper" "$CUSTOM_DIR/"
sudo mount --bind /dev "$CUSTOM_DIR/casper/dev"
# Copy auto_sanitize.py into chroot
sudo cp "$PWD/../files/auto_sanitize.py" "$CUSTOM_DIR/casper/tmp/auto_sanitize.py"
sudo chroot "$CUSTOM_DIR/casper" /bin/bash <<EOF
apt-get update
apt-get install -y python3 python3-pyqt5 hdparm nvme-cli cryptsetup parted lsblk udev
# Copy GUI app (assumes it's in /gui)
mkdir -p /opt/manhattan_gui
cp -r "$GUI_SRC_DIR"/* /opt/manhattan_gui/
# Move auto_sanitize.py to /usr/local/bin and make executable
mv /tmp/auto_sanitize.py /usr/local/bin/auto_sanitize.py
chmod +x /usr/local/bin/auto_sanitize.py
# Set GUI to autostart (for live session)
echo "[Desktop Entry]
Type=Application
Exec=python3 /opt/manhattan_gui/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Manhattan Sanitization Engine" > /etc/xdg/autostart/manhattan-gui.desktop
EOF
sudo umount "$CUSTOM_DIR/casper/dev"

# --- REPACKAGE ISO ---
echo "[5/7] Repackaging ISO..."
cd "$CUSTOM_DIR"
sudo mkisofs -D -r -V "ManhattanSanitization" -cache-inodes -J -l \
  -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot \
  -boot-load-size 4 -boot-info-table -o "$FINAL_ISO" .
cd "$PWD"

# --- DONE ---
echo "[6/7] Custom ISO created: $FINAL_ISO"
