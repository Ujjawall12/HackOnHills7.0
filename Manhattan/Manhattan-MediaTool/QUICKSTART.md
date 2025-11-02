# Manhattan Project - Quick Start Guide for Hackathon

## 🚀 Quick Setup (Windows)

### Option 1: Automated Setup (Recommended)
```powershell
# Run the setup script
.\setup.ps1
```

### Option 2: Manual Setup
```powershell
# Install dependencies for each component
pip install -r client\media_creator\requirements.txt
pip install -r client\wallet_app\requirements.txt
pip install -r sanitization_engine\gui\requirements.txt
```

---

## 🎯 Running the Applications

### Using the Quick Run Script
```powershell
# Media Creator
.\run.ps1 -Component media

# Wallet App
.\run.ps1 -Component wallet

# Sanitization Engine
.\run.ps1 -Component engine
```

### Direct Launch
```powershell
# Media Creator
python client\media_creator\main.py

# Wallet App
python client\wallet_app\main.py

# Sanitization Engine
python sanitization_engine\gui\main.py
```

---

## 📱 Application Overview

### 1. **Media Creator**
- **Purpose**: Create bootable USB drives with the sanitization ISO
- **Features**: 
  - Select ISO file
  - Detect USB devices (Windows & Linux)
  - Flash ISO to USB drive
- **Status**: UI functional, USB detection works on both Windows and Linux

### 2. **Wallet App**
- **Purpose**: Manage Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs)
- **Features**: 
  - Store and display sanitization certificates
  - Manage DIDs
  - Scan QR codes for credential transfer
- **Status**: Basic skeleton (ready for DID/VC implementation)

### 3. **Sanitization Engine**
- **Purpose**: Securely erase drives using NIST SP 800-88 Purge-level commands
- **Features**:
  - Auto-detect drive type (NVMe, ATA, SED)
  - Secure erase with hardware-level commands
  - Progress tracking
  - Safety checks (prevents erasing boot device)
- **Status**: Drive detection works on Windows and Linux (note: actual sanitization commands require Linux tools)

---

## 🔧 Technical Details

### Supported Drive Types
- **NVMe**: Uses `nvme sanitize` command
- **ATA/SATA**: Uses `hdparm --security-erase`
- **Self-Encrypting Drives (SED)**: Uses `cryptsetup luksErase`

### System Requirements
- Python 3.6+
- PyQt5
- (For Sanitization Engine): Linux/WSL or appropriate tools for Windows

---

## 🏗️ Project Structure
```
Manhattan-MediaTool/
├── client/
│   ├── media_creator/     # USB media creator
│   └── wallet_app/         # DID/VC wallet
├── sanitization_engine/
│   ├── gui/                # Sanitization GUI
│   └── iso_build/          # ISO build scripts
├── setup.ps1               # Setup script
├── run.ps1                 # Quick run script
└── QUICKSTART.md           # This file
```

---

## 🎓 Hackathon Presentation Points

1. **Problem**: Need for provable, verifiable data sanitization for IT asset disposal
2. **Solution**: Manhattan Project provides cryptographically verifiable certificates
3. **Components**: 
   - Bootable sanitization engine (hardware-level secure erase)
   - Wallet for managing certificates
   - Media creator for deployment
4. **Compliance**: NIST SP 800-88 Purge-level sanitization
5. **Trust**: Cryptographic proof and immutable audit trails

---

## ⚠️ Notes

- **Media Creator**: Fully works on Windows and Linux ✅
- **Sanitization Engine**: Drive detection works on Windows and Linux ✅ (actual sanitization requires Linux tools like hdparm/nvme-cli)
- **Wallet App**: Foundation for DID/VC integration

---

## 📞 Next Steps for Full Implementation

1. **Media Creator**: Port USB detection to Windows APIs (WMI or win32api)
2. **Wallet App**: Implement DID creation, VC issuance, and QR code generation
3. **Sanitization Engine**: Add cryptographic receipt generation after sanitization
4. **Integration**: Connect all components with blockchain/verifiable credential protocols

---

**Good luck with your hackathon! 🚀**

