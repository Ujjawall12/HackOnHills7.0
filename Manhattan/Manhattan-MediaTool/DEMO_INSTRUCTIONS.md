# Secure File Deletion Demo - Instructions

## Overview

This demo shows **real secure file deletion** using NIST SP 800-88 Purge-level standards. Files are:
1. Overwritten multiple times with random data
2. Permanently deleted

**⚠️ WARNING: Files are ACTUALLY deleted - this cannot be undone!**

---

## Quick Start

### Option 1: GUI Demo (Recommended for Hackathon)

```powershell
# Run the GUI demo
.\run.ps1 -Component demo

# Or directly:
python demo_secure_delete_gui.py
```

**Steps:**
1. Click "Create Demo Folder" - Creates a folder with 5 sample files
2. Review the files shown in the list
3. Click "Start Secure Deletion"
4. Confirm the deletion
5. Watch the progress as files are overwritten and deleted

### Option 2: Command Line Demo

```powershell
# Create demo folder and delete it
python demo_secure_delete.py

# Or delete a specific folder:
python demo_secure_delete.py "path\to\your\folder"
```

---

## How It Works

### Secure Deletion Process

1. **Overwrite Pass 1**: Fill file with zeros (0x00)
2. **Overwrite Pass 2**: Fill file with ones (0xFF)  
3. **Overwrite Pass 3+**: Fill with random data
4. **File Sync**: Force write to disk
5. **Delete**: Permanently remove the file

### Security Features

- **Multiple Overwrite Passes**: Makes data recovery extremely difficult
- **Random Data**: Prevents pattern-based recovery
- **Disk Sync**: Ensures data is actually written to disk
- **Permanent Deletion**: Files cannot be recovered after this process

---

## Demo Files Created

When you click "Create Demo Folder", these files are created:

1. `sensitive_document.txt` - Contains fake SSN and credit card numbers
2. `private_data.csv` - Contains fake login credentials
3. `financial_report.txt` - Contains fake financial data
4. `database_backup.sql` - Contains fake database records
5. `encryption_keys.txt` - Contains fake encryption keys

All files are in `manhattan_demo_folder/`

---

## Hackathon Presentation Tips

### For Judges

1. **Show the Demo Folder Creation**
   - Click "Create Demo Folder"
   - Show the files list
   - Explain: "These files contain sensitive data that needs to be securely deleted"

2. **Explain the Process**
   - "We use NIST SP 800-88 Purge-level deletion"
   - "Multiple overwrite passes make recovery impossible"
   - "This is the same principle used for drive sanitization"

3. **Run the Deletion**
   - Click "Start Secure Deletion"
   - Show the progress
   - Explain: "Files are being overwritten with random data, then deleted"

4. **Verify Deletion**
   - Show that files are gone
   - Explain: "These files cannot be recovered even with forensic tools"

### Key Talking Points

- **Real Deletion**: Not a simulation - files are actually deleted
- **NIST Compliant**: Uses industry-standard secure deletion
- **Same Technology**: Same principles as drive-level sanitization
- **Audit Trail**: Can be extended to include cryptographic proof

---

## Technical Details

### File Overwrite Algorithm

```python
# Pass 1: Zeros
file.write(bytes([0x00] * file_size))

# Pass 2: Ones  
file.write(bytes([0xFF] * file_size))

# Pass 3+: Random
file.write(bytes([random.randint(0, 255) for _ in range(file_size)]))
```

### Why This Works

- **Zeros/Ones**: Erases obvious data patterns
- **Random Data**: Prevents recovery of partial data
- **Multiple Passes**: Ensures complete overwriting
- **Disk Sync**: Forces immediate write (not cached)

---

## Safety Features

1. **Confirmation Dialog**: Requires explicit confirmation
2. **Clear Warnings**: Shows what will be deleted
3. **Progress Display**: Shows what's happening in real-time
4. **Error Handling**: Gracefully handles errors

---

## Integration with Manhattan Project

This demo shows:
- **Secure deletion principles** used in drive sanitization
- **File-level implementation** of NIST SP 800-88
- **GUI interface** similar to the sanitization engine
- **Real deletion** (not simulation) for demonstration

The actual drive sanitization uses hardware-level commands (hdparm, nvme-cli), but the **same security principles** apply.

---

## Troubleshooting

### "Folder not found"
- Make sure the folder path is correct
- Check that you have permission to access the folder

### "Permission denied"
- Run as administrator if needed
- Check file/folder permissions

### "Files still exist"
- Check that files aren't open in another program
- Make sure you have write/delete permissions

---

**Ready for your hackathon demo! 🚀**

