import sys
import subprocess
import platform
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QComboBox, QMessageBox, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

DARK_STYLE = """
QWidget {
    background-color: #232629;
    color: #f5f5f5;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 14px;
}
QLabel#TitleLabel {
    color: #e76f00;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 1px;
}
QLabel#DescLabel {
    color: #b0b0b0;
    font-size: 13px;
    margin-bottom: 10px;
}
QPushButton {
    background-color: #3572A5;
    color: #fff;
    border-radius: 7px;
    padding: 7px 18px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    margin: 4px 0;
}
QPushButton:hover {
    background-color: #e76f00;
    color: #fff;
}
QComboBox {
    background-color: #2d3136;
    color: #f5f5f5;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 14px;
}
QFrame#line {
    background: #444;
    max-height: 1px;
    min-height: 1px;
}
"""

class MediaCreator(QWidget):
    def __init__(self):
        super().__init__()
        # Increase window size by 40%: original 420x320 -> 588x448
        self.setWindowTitle('Manhattan Project - Media Creator')
        self.setGeometry(200, 200, 588, 448)
        self.setFixedSize(588, 448)
        self.setWindowIcon(QIcon())  # Placeholder, can set a logo icon here
        self.setStyleSheet(DARK_STYLE)

        self.iso_path = None
        self.usb_devices = []

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(36, 28, 36, 28)
        main_layout.setSpacing(16)

        # Project Title
        title = QLabel('The Manhattan Project')
        title.setObjectName('TitleLabel')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Project Description
        desc = QLabel('A Trust-Anchored Protocol for Provable Data Sanitization')
        desc.setObjectName('DescLabel')
        desc.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName('line')
        main_layout.addWidget(line)

        # ISO selection
        iso_layout = QHBoxLayout()
        # Placeholder: currently selected 'ManhattanSanitizationBootableV1.0.iso'
        self.iso_label = QLabel("ISO: ManhattanSanitizationBootableV1.0.iso")
        self.iso_label.setStyleSheet('color: #b0b0b0;')
        self.iso_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.iso_button = QPushButton('Switch Version')
        self.iso_button.setToolTip('Switch to a different version of the Manhattan Sanitization Engine ISO')
        self.iso_button.clicked.connect(self.select_iso)
        iso_layout.addWidget(self.iso_label)
        iso_layout.addWidget(self.iso_button)
        main_layout.addLayout(iso_layout)

        # USB device selection
        usb_layout = QHBoxLayout()
        self.usb_label = QLabel('USB Device:')
        self.usb_label.setStyleSheet('color: #b0b0b0;')
        self.usb_combo = QComboBox()
        self.usb_combo.setToolTip('Select the USB drive to write the ISO to')
        self.refresh_usb_devices()
        usb_layout.addWidget(self.usb_label)
        usb_layout.addWidget(self.usb_combo)
        main_layout.addLayout(usb_layout)

        # Refresh button
        self.refresh_button = QPushButton('Refresh USB List')
        self.refresh_button.setToolTip('Rescan for connected USB drives')
        self.refresh_button.clicked.connect(self.refresh_usb_devices)
        main_layout.addWidget(self.refresh_button)

        # Info text
        info = QLabel('This tool securely prepares a bootable USB for the Manhattan Project Sanitization Engine.\n\nSelect your ISO, choose a USB drive, and proceed to write. All actions are performed locally and securely.')
        info.setStyleSheet('color: #888; font-size: 12px; margin-top: 8px;')
        info.setWordWrap(True)
        main_layout.addWidget(info)

        # Flash button (placeholder)
        self.flash_button = QPushButton('Flash')
        self.flash_button.setToolTip('Write the selected ISO to the selected USB drive')
        self.flash_button.clicked.connect(self.flash_placeholder)
        main_layout.addWidget(self.flash_button)

        self.setLayout(main_layout)

    def select_iso(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select ISO file', '', 'ISO Files (*.iso)')
        if path:
            self.iso_path = path
            self.iso_label.setText(f'ISO: {path.split("/")[-1]}')
        else:
            # If no ISO selected, keep the placeholder
            self.iso_label.setText('ISO: ManhattanSanitizationBootableV1.0.iso')

    def refresh_usb_devices(self):
        self.usb_combo.clear()
        self.usb_devices = self.detect_usb_devices()
        if not self.usb_devices:
            self.usb_combo.addItem('No USB devices found')
        else:
            for dev in self.usb_devices:
                self.usb_combo.addItem(f"{dev['name']} ({dev['size']}) - {dev['model']}")

    def detect_usb_devices(self):
        """Detect USB devices cross-platform (Windows and Linux)"""
        if platform.system() == 'Windows':
            return self._detect_usb_windows()
        else:
            return self._detect_usb_linux()

    def _detect_usb_windows(self):
        """Detect USB devices on Windows using PowerShell"""
        devices = []
        try:
            # Simpler PowerShell command to get removable drives
            # DriveType 2 = Removable drives
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
            
            # Set up subprocess creation flags for Windows (hide console window)
            creation_flags = 0
            if sys.platform == 'win32':
                try:
                    creation_flags = subprocess.CREATE_NO_WINDOW
                except AttributeError:
                    # CREATE_NO_WINDOW not available in older Python versions
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
            if not output:
                return []
            
            # Parse JSON output
            try:
                data = json.loads(output)
                if isinstance(data, dict):
                    data = [data]
                
                for disk in data:
                    device_id = disk.get('DeviceID', '').strip()
                    if not device_id:
                        continue
                    
                    size_bytes = disk.get('Size')
                    volume_name = disk.get('VolumeName', 'USB Drive')
                    
                    # Format size
                    if size_bytes:
                        try:
                            size_bytes = int(size_bytes)
                            if size_bytes > 0:
                                size_gb = size_bytes / (1024**3)
                                size_str = f"{size_gb:.1f} GB"
                            else:
                                size_str = "Unknown"
                        except:
                            size_str = "Unknown"
                    else:
                        size_str = "Unknown"
                    
                    devices.append({
                        'name': device_id,  # e.g., "E:"
                        'size': size_str,
                        'model': volume_name,
                        'device_path': device_id  # Store for flashing
                    })
                
            except json.JSONDecodeError:
                # If JSON parsing fails, try simple approach
                return []
            
            return devices
            
        except subprocess.CalledProcessError:
            # If PowerShell fails, try alternative method
            return self._detect_usb_windows_alt()
        except Exception:
            # Silent fail - return empty list
            return []

    def _detect_usb_windows_alt(self):
        """Alternative Windows USB detection using diskpart"""
        devices = []
        try:
            # Use diskpart to list removable disks
            diskpart_script = 'list disk\n'
            result = subprocess.run(
                ['diskpart'],
                input=diskpart_script,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            # Parse diskpart output (basic implementation)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Disk' in line and 'Online' in line:
                    # Extract disk number and check if it's removable
                    parts = line.split()
                    if len(parts) > 1:
                        try:
                            disk_num = int(parts[1])
                            # Check if removable (would need additional WMI query)
                            devices.append({
                                'name': f'Disk {disk_num}',
                                'size': 'Unknown',
                                'model': 'USB Drive'
                            })
                        except:
                            pass
        except:
            pass
        
        return devices

    def _detect_usb_linux(self):
        """Detect USB devices on Linux using lsblk"""
        try:
            result = subprocess.run([
                'lsblk', '-o', 'NAME,SIZE,MODEL,TRAN,RM', '-J'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            
            data = json.loads(result.stdout)
            devices = []
            for blk in data.get('blockdevices', []):
                if blk.get('rm') == True or blk.get('tran') == 'usb':
                    devices.append({
                        'name': f"/dev/{blk['name']}",
                        'size': blk.get('size', 'Unknown'),
                        'model': blk.get('model', 'Unknown'),
                        'device_path': f"/dev/{blk['name']}"
                    })
            return devices
        except Exception as e:
            return []

    def flash_placeholder(self):
        QMessageBox.information(self, 'Flash', 'Media creation (flashing) will be implemented here.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaCreator()
    window.show()
    sys.exit(app.exec_())
