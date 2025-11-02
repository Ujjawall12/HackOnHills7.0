# ISO Build Instructions

This directory contains scripts and configuration for building the custom bootable Linux ISO used by the Manhattan Project Sanitization Engine.

## Requirements
- Ubuntu or Debian-based host (for best compatibility)
- Root privileges (for chroot and ISO creation)
- Tools: wget, 7z, mkisofs, sudo

## What the Build Script Does
- Downloads a minimal Ubuntu ISO
- Extracts and customizes it in a chroot environment
- Installs required packages: Python 3, PyQt5, hdparm, nvme-cli, cryptsetup, parted, lsblk, udev
- Copies the custom GUI app into the ISO
- Sets the GUI to autostart on boot
- Repackages the ISO as `ManhattanSanitizationBootableV1.0.iso`

## Usage

```bash
cd scripts
sudo bash build_iso.sh
```

The resulting ISO will be created in the current directory. You can then use the Media Creator app to write it to a USB drive.

---

**Note:** This script is a starting point and may require tweaks for your environment or for additional customizations (branding, drivers, etc.).
