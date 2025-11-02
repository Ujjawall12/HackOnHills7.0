#!/usr/bin/env python3
import subprocess
import json
import os
from datetime import datetime

def log(msg):
    with open('/var/log/sanitization.log', 'a') as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

def run(cmd):
    log(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log(result.stdout)
        if result.stderr:
            log(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error: {e.stderr}")
        return False

def detect_devices():
    # Use lsblk to get all block devices
    result = subprocess.run(['lsblk', '-o', 'NAME,TYPE,MODEL,TRAN,SERIAL', '-J'], stdout=subprocess.PIPE, text=True, check=True)
    data = json.loads(result.stdout)
    devices = []
    for blk in data.get('blockdevices', []):
        if blk.get('type') == 'disk':
            dev = {
                'name': f"/dev/{blk['name']}",
                'model': blk.get('model', ''),
                'tran': blk.get('tran', ''),
                'serial': blk.get('serial', ''),
                'type': 'unknown'
            }
            # NVMe detection
            if dev['name'].startswith('/dev/nvme'):
                dev['type'] = 'nvme'
            # SED detection (simple heuristic)
            elif 'sed' in (dev['model'] or '').lower() or 'self-encrypt' in (dev['model'] or '').lower():
                dev['type'] = 'sed'
            # ATA detection
            elif dev['tran'] in ('sata', 'ata'):
                dev['type'] = 'ata'
            devices.append(dev)
    return devices

def sanitize_nvme(dev):
    log(f"Sanitizing NVMe device: {dev['name']}")
    return run(['nvme', 'sanitize', dev['name'], '--sanitize', '1', '--no-deallocate'])

def sanitize_ata(dev):
    log(f"Sanitizing ATA device: {dev['name']}")
    # Set password NULL, then erase
    ok1 = run(['hdparm', '--user-master', 'u', '--security-set-pass', 'NULL', dev['name']])
    ok2 = run(['hdparm', '--user-master', 'u', '--security-erase', 'NULL', dev['name']])
    return ok1 and ok2

def sanitize_sed(dev):
    log(f"Sanitizing SED device: {dev['name']}")
    return run(['cryptsetup', 'luksErase', dev['name']])

def main():
    log("==== Manhattan Project Auto-Sanitization Started ====")
    devices = detect_devices()
    if not devices:
        log("No block devices found for sanitization.")
        return
    for dev in devices:
        log(f"Device: {dev['name']} | Model: {dev['model']} | Type: {dev['type']}")
        if dev['type'] == 'nvme':
            sanitize_nvme(dev)
        elif dev['type'] == 'sed':
            sanitize_sed(dev)
        elif dev['type'] == 'ata':
            sanitize_ata(dev)
        else:
            log(f"Unknown device type for {dev['name']}, skipping.")
    log("==== Manhattan Project Auto-Sanitization Complete ====")

if __name__ == '__main__':
    main()



