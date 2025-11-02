# The Manhattan Project: A Trust-Anchored Protocol for Provable Data Sanitization

## Overview

The Manhattan Project is a system for provable, cryptographically verifiable data sanitization. It provides a secure, auditable, and user-owned certificate of sanitization for IT asset disposal, combining secure erasure with cryptographic proof and immutable audit trails.

### Components

- **Client**
  - **media_creator**: Cross-platform USB media creator (Python GUI)
  - **wallet_app**: Desktop wallet for managing DIDs and Verifiable Credentials (Python GUI)
- **Sanitization Engine**
  - **gui**: GUI wrapper for hdparm/nvme-cli (Python GUI)
  - **iso_build**: Scripts/configs for building the custom bootable Linux ISO

---

## Directory Structure

```
client/
  media_creator/   # USB media creator app
  wallet_app/      # Wallet app for DIDs & VCs
sanitization_engine/
  gui/             # GUI for sanitization engine
  iso_build/       # ISO build scripts/configs
```

---

## Getting Started

### Quick Setup (Windows)

1. **Install dependencies:**
   ```powershell
   .\setup.ps1
   ```

2. **Run an application:**
   ```powershell
   # Media Creator
   .\run.ps1 -Component media
   
   # Wallet App
   .\run.ps1 -Component wallet
   
   # Sanitization Engine
   .\run.ps1 -Component engine
   ```

3. **Or run directly:**
   ```powershell
   python client\media_creator\main.py
   python client\wallet_app\main.py
   python sanitization_engine\gui\main.py
   ```

### Manual Setup

Install dependencies for each component:
```bash
pip install -r client/media_creator/requirements.txt
pip install -r client/wallet_app/requirements.txt
pip install -r sanitization_engine/gui/requirements.txt
```

### Test Installation

Run the test script to verify everything is set up correctly:
```powershell
python test_apps.py
```

See `QUICKSTART.md` for detailed instructions and hackathon presentation tips.
