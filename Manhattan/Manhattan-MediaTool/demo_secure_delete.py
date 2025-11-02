#!/usr/bin/env python3
"""
Manhattan Project - Secure File Deletion Demo
This script demonstrates secure file deletion by actually overwriting and deleting files.
Creates a demo folder with sample files and then securely deletes them.
"""
import os
import random
import sys
from pathlib import Path

def create_demo_folder(base_path="manhattan_demo_folder"):
    """Create a demo folder with sample files"""
    demo_path = Path(base_path)
    demo_path.mkdir(exist_ok=True)
    
    # Create 5 sample files with different content
    sample_files = [
        ("sensitive_document.txt", "This is a sensitive document with confidential information.\nEmployee SSN: 123-45-6789\nCredit Card: 4532-1234-5678-9010"),
        ("private_data.csv", "Name,Email,Password\nJohn Doe,john@example.com,secret123\nJane Smith,jane@example.com,password456"),
        ("financial_report.xlsx", b"Excel binary data - financial information"),
        ("database_backup.sql", "-- Database backup\nCREATE TABLE users (id INT, name VARCHAR(50));\nINSERT INTO users VALUES (1, 'admin');\nINSERT INTO users VALUES (2, 'user');"),
        ("encryption_keys.key", "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----")
    ]
    
    created_files = []
    for filename, content in sample_files:
        file_path = demo_path / filename
        if isinstance(content, bytes):
            file_path.write_bytes(content)
        else:
            file_path.write_text(content, encoding='utf-8')
        created_files.append(str(file_path))
        print(f"Created: {file_path}")
    
    return demo_path, created_files

def secure_overwrite_file(file_path, passes=3):
    """
    Securely overwrite a file with random data multiple times (NIST SP 800-88 inspired)
    This implements a Purge-level deletion by overwriting file content
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    
    file_size = file_path.stat().st_size
    
    # Multiple overwrite passes with different patterns
    patterns = [
        lambda: bytes([0x00] * file_size),  # All zeros
        lambda: bytes([0xFF] * file_size),  # All ones
        lambda: bytes([random.randint(0, 255) for _ in range(file_size)]),  # Random
        lambda: bytes([random.randint(0, 255) for _ in range(file_size)]),  # Random again
    ]
    
    try:
        with open(file_path, 'r+b') as f:
            for i in range(passes):
                if i < len(patterns):
                    pattern = patterns[i]
                else:
                    pattern = lambda: bytes([random.randint(0, 255) for _ in range(file_size)])
                
                f.seek(0)
                f.write(pattern())
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
                
        return True
    except Exception as e:
        print(f"Error overwriting {file_path}: {e}")
        return False

def secure_delete_file(file_path, passes=3):
    """
    Securely delete a file by overwriting it multiple times, then deleting it
    Implements NIST SP 800-88 Purge-level deletion
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return False
    
    file_size = file_path.stat().st_size
    print(f"\n[Secure Delete] {file_path.name} ({file_size} bytes)")
    print(f"  Step 1: Overwriting file with random data ({passes} passes)...")
    
    # Secure overwrite
    if not secure_overwrite_file(file_path, passes):
        return False
    
    print(f"  Step 2: Deleting file...")
    
    # Delete the file
    try:
        file_path.unlink()
        print(f"  [SUCCESS] File securely deleted: {file_path.name}")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to delete file: {e}")
        return False

def secure_delete_folder(folder_path, passes=3):
    """
    Securely delete all files in a folder, then delete the folder
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return False
    
    if not folder_path.is_dir():
        print(f"Path is not a directory: {folder_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Manhattan Project - Secure File Deletion Demo")
    print(f"{'='*60}")
    print(f"Target: {folder_path}")
    print(f"Overwrite passes: {passes}")
    print(f"{'='*60}\n")
    
    # Get all files
    files = list(folder_path.glob('*'))
    files = [f for f in files if f.is_file()]
    
    if not files:
        print("No files found in the folder.")
        return False
    
    print(f"Found {len(files)} file(s) to securely delete:\n")
    for f in files:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")
    
    # Confirm
    response = input("\n⚠️  WARNING: This will PERMANENTLY delete all files in this folder!\nContinue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return False
    
    print("\nStarting secure deletion process...\n")
    
    # Delete each file
    success_count = 0
    for file_path in files:
        if secure_delete_file(file_path, passes):
            success_count += 1
    
    # Delete the folder if empty
    try:
        remaining = list(folder_path.glob('*'))
        if not remaining:
            folder_path.rmdir()
            print(f"\n[SUCCESS] Folder deleted: {folder_path}")
    except Exception as e:
        print(f"\n[NOTE] Could not delete folder: {e}")
    
    print(f"\n{'='*60}")
    print(f"Deletion Complete: {success_count}/{len(files)} files securely deleted")
    print(f"{'='*60}\n")
    
    return success_count == len(files)

def demo_mode():
    """Create demo folder and then securely delete it"""
    demo_folder, files = create_demo_folder()
    
    print(f"\n{'='*60}")
    print("Demo folder created with sample files:")
    print(f"{'='*60}")
    for f in files:
        print(f"  - {Path(f).name}")
    
    print(f"\n{'='*60}")
    print("Starting secure deletion demo...")
    print(f"{'='*60}\n")
    
    # Securely delete the folder
    return secure_delete_folder(demo_folder, passes=3)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Delete specified folder
        target_folder = sys.argv[1]
        secure_delete_folder(target_folder, passes=3)
    else:
        # Demo mode - create and delete demo folder
        demo_mode()

