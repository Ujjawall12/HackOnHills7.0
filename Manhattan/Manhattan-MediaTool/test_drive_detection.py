#!/usr/bin/env python3
"""
Test script to verify drive detection works on Windows for the sanitization engine
"""
import sys
import subprocess
import platform
import json

def test_windows_drive_detection():
    """Test Windows drive detection"""
    if platform.system() != 'Windows':
        print("This test is for Windows only. Current OS:", platform.system())
        return False
    
    try:
        ps_script = '''
        Get-WmiObject Win32_LogicalDisk | Select-Object DeviceID, Size, VolumeName, FileSystem, DriveType, VolumeSerialNumber | ConvertTo-Json
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
            print("[INFO] No drives found")
            return False
        
        try:
            data = json.loads(output)
            if isinstance(data, dict):
                data = [data]
            
            print(f"[SUCCESS] Found {len(data)} drive(s):")
            for disk in data:
                device_id = disk.get('DeviceID', 'N/A')
                size_bytes = disk.get('Size')
                volume_name = disk.get('VolumeName', 'N/A')
                file_system = disk.get('FileSystem', 'N/A')
                drive_type = disk.get('DriveType', 0)
                
                # Drive type mapping
                drive_type_str = 'Unknown'
                if drive_type == 2:
                    drive_type_str = 'Removable'
                elif drive_type == 3:
                    drive_type_str = 'Fixed'
                elif drive_type == 4:
                    drive_type_str = 'Network'
                elif drive_type == 5:
                    drive_type_str = 'CD-ROM'
                
                if size_bytes:
                    try:
                        size_gb = int(size_bytes) / (1024**3)
                        size_str = f"{size_gb:.1f} GB"
                    except:
                        size_str = "Unknown"
                else:
                    size_str = "Unknown"
                
                print(f"  - {device_id}: {volume_name} ({size_str}) [{drive_type_str}] - {file_system}")
            
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
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Testing Windows Drive Detection for Sanitization Engine...\n")
    success = test_windows_drive_detection()
    print("\n" + "="*50)
    if success:
        print("[RESULT] Drive detection test completed successfully!")
        print("[NOTE] Your drives (C:, D:, E:, etc.) should now be visible in the Sanitization Engine!")
        sys.exit(0)
    else:
        print("[RESULT] Drive detection test failed!")
        sys.exit(1)

