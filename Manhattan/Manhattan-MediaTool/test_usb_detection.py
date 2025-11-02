#!/usr/bin/env python3
"""
Test script to verify USB detection works on Windows
"""
import sys
import subprocess
import platform
import json

def test_windows_usb_detection():
    """Test Windows USB detection"""
    if platform.system() != 'Windows':
        print("This test is for Windows only. Current OS:", platform.system())
        return False
    
    try:
        ps_script = '''
        Get-WmiObject Win32_LogicalDisk | Where-Object {$_.DriveType -eq 2} | ForEach-Object {
            $vol = $_.VolumeName
            if (-not $vol) { $vol = "USB Drive" }
            [PSCustomObject]@{
                DeviceID = $_.DeviceID
                Size = $_.Size
                VolumeName = $vol
                FreeSpace = $_.FreeSpace
            }
        } | ConvertTo-Json
        '''
        
        creation_flags = 0
        if sys.platform == 'win32':
            try:
                creation_flags = subprocess.CREATE_NO_WINDOW
            except AttributeError:
                pass
        
        result = subprocess.run(
            ['powershell', '-NoProfile', '-Command', ps_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            creationflags=creation_flags
        )
        
        output = result.stdout.strip()
        print("PowerShell output:")
        print(output)
        print("\n" + "="*50)
        
        if not output:
            print("[INFO] No USB devices found (this is normal if no USB drives are connected)")
            return True
        
        try:
            data = json.loads(output)
            if isinstance(data, dict):
                data = [data]
            
            print(f"[SUCCESS] Found {len(data)} USB device(s):")
            for disk in data:
                device_id = disk.get('DeviceID', 'N/A')
                size_bytes = disk.get('Size')
                volume_name = disk.get('VolumeName', 'N/A')
                
                if size_bytes:
                    try:
                        size_gb = int(size_bytes) / (1024**3)
                        size_str = f"{size_gb:.1f} GB"
                    except:
                        size_str = "Unknown"
                else:
                    size_str = "Unknown"
                
                print(f"  - {device_id}: {volume_name} ({size_str})")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            print("Raw output:", output)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] PowerShell command failed:")
        print(f"  Return code: {e.returncode}")
        print(f"  Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == '__main__':
    print("Testing Windows USB Detection...\n")
    success = test_windows_usb_detection()
    print("\n" + "="*50)
    if success:
        print("[RESULT] USB detection test completed successfully!")
        sys.exit(0)
    else:
        print("[RESULT] USB detection test failed!")
        sys.exit(1)

