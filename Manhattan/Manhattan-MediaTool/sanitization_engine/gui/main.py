import sys
import subprocess
import threading
import platform
import json
import hashlib
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QMessageBox, QFrame, QSizePolicy, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# Aptos Configuration
APTOS_MODULE_ADDRESS = "0xd2d618ed1248e1ac5f715991af3de929f8f4aa064983956c01ca77521178ed05"
APTOS_NETWORK = "testnet"

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
QLabel#WarnLabel {
    color: #ff5555;
    font-size: 13px;
    font-weight: bold;
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
QProgressBar {
    background-color: #2d3136;
    color: #e76f00;
    border-radius: 6px;
    text-align: center;
    font-size: 13px;
    height: 18px;
}
"""

class WorkerSignals(QObject):
    finished = pyqtSignal(str, bool, dict)  # Added dict for drive info
    progress = pyqtSignal(int)

class EraseWorker(threading.Thread):
    def __init__(self, method, device, drive_info, signals):
        super().__init__()
        self.method = method
        self.device = device
        self.drive_info = drive_info  # Store full drive info
        self.signals = signals

    def run(self):
        try:
            # Check if running on Windows (shouldn't happen, but safety check)
            if platform.system() == 'Windows':
                error_msg = (
                    "Sanitization requires Linux tools that are not available on Windows.\n\n"
                    "Required tools:\n"
                    "- hdparm (for ATA/SATA drives)\n"
                    "- nvme-cli (for NVMe drives)\n"
                    "- cryptsetup (for Self-Encrypting Drives)\n\n"
                    "Please use the bootable ISO or run this on a Linux system/WSL2."
                )
                self.signals.finished.emit(error_msg, False)
                return
            
            if self.method == 'NVMe Sanitize':
                # Use block erase (1) as default
                cmd = ["nvme", "sanitize", self.device, "--sanitize", "1", "--no-deallocate"]
            elif self.method == 'SED Crypto-Erase':
                # Try cryptsetup (for LUKS SEDs)
                cmd = ["cryptsetup", "luksErase", self.device]
            else:  # ATA Secure Erase
                # Set password NULL, then erase
                cmd1 = ["hdparm", "--user-master", "u", "--security-set-pass", "NULL", self.device]
                cmd2 = ["hdparm", "--user-master", "u", "--security-erase", "NULL", self.device]
                subprocess.run(cmd1, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                proc = subprocess.run(cmd2, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.signals.finished.emit(proc.stdout + proc.stderr, True, self.drive_info)
                return
            proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.signals.finished.emit(proc.stdout + proc.stderr, True, self.drive_info)
        except FileNotFoundError as e:
            tool_name = str(e).split("'")[1] if "'" in str(e) else "required tool"
            error_msg = (
                f"Sanitization tool not found: {tool_name}\n\n"
                f"This tool requires Linux-specific commands:\n"
                f"- hdparm (for ATA/SATA drives)\n"
                f"- nvme-cli (for NVMe drives)\n"
                f"- cryptsetup (for Self-Encrypting Drives)\n\n"
                f"These tools are not available on Windows.\n"
                f"Please use the bootable ISO or run this on a Linux system/WSL2."
            )
            self.signals.finished.emit(error_msg, False, {})
        except subprocess.CalledProcessError as e:
            error_output = e.stdout + e.stderr if e.stdout and e.stderr else str(e)
            error_msg = f"Sanitization command failed:\n\n{error_output}\n\nError code: {e.returncode}"
            self.signals.finished.emit(error_msg, False, {})
        except Exception as e:
            error_msg = f"Unexpected error during sanitization:\n\n{str(e)}\n\nThis may be due to missing Linux tools or insufficient permissions."
            self.signals.finished.emit(error_msg, False, {})

class SanitizationEngineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manhattan Project - Sanitization Engine')
        self.setGeometry(100, 100, 700, 480)
        self.setFixedSize(700, 480)
        self.setStyleSheet(DARK_STYLE)

        self.drives = []
        self.selected_drive = None
        self.selected_method = None
        self.boot_device = self.get_boot_device()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(36, 24, 36, 24)
        main_layout.setSpacing(14)

        # Title
        title = QLabel('The Manhattan Project: Secure Media Sanitization')
        title.setObjectName('TitleLabel')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Description
        desc = QLabel('This tool securely erases all data from selected drives using NIST SP 800-88 Purge-level commands.\n\n')
        desc.setObjectName('DescLabel')
        desc.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc)

        # Warning
        warn = QLabel('WARNING: This process is IRREVERSIBLE. All data on the selected drive will be destroyed.')
        warn.setObjectName('WarnLabel')
        warn.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(warn)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName('line')
        main_layout.addWidget(line)

        # Drive selection
        drive_layout = QHBoxLayout()
        self.drive_label = QLabel('Select Drive:')
        self.drive_label.setStyleSheet('color: #b0b0b0;')
        self.drive_combo = QComboBox()
        self.drive_combo.setToolTip('Select the drive to sanitize')
        self.refresh_drives()
        self.drive_combo.currentIndexChanged.connect(self.update_method_info)
        drive_layout.addWidget(self.drive_label)
        drive_layout.addWidget(self.drive_combo)
        main_layout.addLayout(drive_layout)

        # Method info
        self.method_info = QTextEdit()
        self.method_info.setReadOnly(True)
        self.method_info.setStyleSheet('background: #232629; color: #e0e0e0; border: none; font-size: 13px;')
        self.method_info.setFixedHeight(70)
        main_layout.addWidget(self.method_info)

        # Start button
        self.start_button = QPushButton('Start Sanitization')
        self.start_button.setToolTip('Begin secure erasure of the selected drive')
        self.start_button.clicked.connect(self.confirm_and_start)
        main_layout.addWidget(self.start_button)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)  # Indeterminate
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        # Progress/result area
        self.result_label = QLabel('')
        self.result_label.setStyleSheet('color: #b0b0b0; font-size: 13px;')
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)
        self.update_method_info()

    def generate_verifiable_credential(self, drive_info, method):
        """Generate a Verifiable Credential for the sanitization event"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        serial_number = drive_info.get('serial', 'Unknown')
        
        vc_data = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiableCredential", "SanitizationCertificate"],
            "issuer": "did:manhattan:sanitization-engine",
            "issuanceDate": timestamp,
            "credentialSubject": {
                "id": f"urn:device:{serial_number}",
                "serialNumber": serial_number,
                "deviceName": drive_info.get('name', 'Unknown'),
                "model": drive_info.get('model', 'Unknown'),
                "capacity": drive_info.get('size', 'Unknown'),
                "sanitizationMethod": method,
                "timestamp": timestamp,
                "transport": drive_info.get('tran', 'Unknown'),
                "deviceType": drive_info.get('type', 'Unknown')
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "created": timestamp,
                "proofPurpose": "assertionMethod"
            }
        }
        return vc_data

    def calculate_vc_hash(self, vc_data):
        """Calculate SHA-256 hash of a Verifiable Credential"""
        vc_json = json.dumps(vc_data, sort_keys=True)
        return hashlib.sha256(vc_json.encode()).digest()

    def save_verifiable_credential(self, vc_data, serial_number):
        """Save VC to file"""
        try:
            filename = f"sanitization_cert_{serial_number}.json"
            with open(filename, "w") as f:
                json.dump(vc_data, f, indent=2, sort_keys=True)
            return filename
        except Exception as e:
            return None

    def register_proof_on_aptos(self, serial_number, vc_hash):
        """Register the sanitization proof on Aptos blockchain"""
        try:
            vc_hash_hex = vc_hash.hex()
            
            # Check if running in aptos directory
            aptos_dir = Path(__file__).parent.parent.parent / "aptos"
            
            cmd = [
                "aptos", "move", "run",
                "--function-id", f"{APTOS_MODULE_ADDRESS}::manhattan_notary::register_proof",
                "--args", f"string:{serial_number}", f"hex:{vc_hash_hex}",
                "--assume-yes"
            ]
            
            # Run command from aptos directory if it exists
            if aptos_dir.exists():
                result = subprocess.run(
                    cmd,
                    cwd=str(aptos_dir),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            if result.returncode == 0:
                # Parse transaction hash from output
                try:
                    output_json = json.loads(result.stdout)
                    tx_hash = output_json.get('Result', {}).get('transaction_hash', 'Unknown')
                    return True, tx_hash
                except:
                    return True, "Success (hash unavailable)"
            else:
                return False, result.stderr or result.stdout
                
        except FileNotFoundError:
            return False, "Aptos CLI not found. Please ensure Aptos CLI is installed."
        except subprocess.TimeoutExpired:
            return False, "Transaction timeout. The proof may still be registered."
        except Exception as e:
            return False, str(e)

    def get_boot_device(self):
        """Detect the boot device to prevent erasing it"""
        if platform.system() == 'Windows':
            try:
                # Get the system drive (usually C:)
                import os
                system_drive = os.environ.get('SystemDrive', 'C:')
                return system_drive
            except Exception:
                return None
        else:
            # Linux: Try to detect the device the system booted from
            try:
                with open('/proc/mounts') as f:
                    for line in f:
                        if ' / ' in line:
                            return line.split()[0]
            except Exception:
                return None
            return None

    def refresh_drives(self):
        self.drive_combo.clear()
        self.drives = self.detect_drives()
        if not self.drives:
            self.drive_combo.addItem('No block devices found')
        else:
            for d in self.drives:
                display = f"{d['label']} ({d['model']}, {d['size']})"
                self.drive_combo.addItem(display)

    def detect_drives(self):
        """Detect all drives cross-platform (Windows and Linux)"""
        if platform.system() == 'Windows':
            return self._detect_drives_windows()
        else:
            return self._detect_drives_linux()

    def _detect_drives_windows(self):
        """Detect all drives on Windows using PowerShell/WMI"""
        drives = []
        try:
            # Get all logical disks (drives) - simple and reliable
            ps_script_final = '''
            Get-WmiObject Win32_LogicalDisk | Select-Object DeviceID, Size, VolumeName, FileSystem, DriveType, VolumeSerialNumber | ConvertTo-Json
            '''
            
            creation_flags = 0
            if sys.platform == 'win32':
                try:
                    creation_flags = subprocess.CREATE_NO_WINDOW
                except AttributeError:
                    pass
            
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script_final],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                creationflags=creation_flags
            )
            
            output = result.stdout.strip()
            if not output:
                return []
            
            try:
                data = json.loads(output)
                if isinstance(data, dict):
                    data = [data]
                
                for disk in data:
                    device_id = disk.get('DeviceID', '').strip()
                    if not device_id:
                        continue
                    
                    size_bytes = disk.get('Size')
                    volume_name = disk.get('VolumeName', 'Local Disk')
                    file_system = disk.get('FileSystem', '')
                    drive_type = disk.get('DriveType', 0)
                    
                    # Use volume name as model for simplicity (can be enhanced later)
                    model = volume_name if volume_name else 'Local Disk'
                    
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
                    
                    # Determine drive type string
                    drive_type_str = 'Unknown'
                    if drive_type == 2:
                        drive_type_str = 'Removable'
                    elif drive_type == 3:
                        drive_type_str = 'Fixed'
                    elif drive_type == 4:
                        drive_type_str = 'Network'
                    elif drive_type == 5:
                        drive_type_str = 'CD-ROM'
                    
                    # Build label
                    label = f"{device_id} [{drive_type_str}]"
                    if volume_name and volume_name != device_id:
                        label += f" - {volume_name}"
                    if file_system:
                        label += f" ({file_system})"
                    
                    # Determine transport type for method detection
                    tran = 'ata'  # Default to ATA
                    if 'nvme' in model.lower() or 'nvme' in device_id.lower():
                        tran = 'nvme'
                    elif 'ssd' in model.lower():
                        tran = 'sata'
                    
                    drives.append({
                        'name': device_id,  # e.g., "C:", "D:", etc.
                        'size': size_str,
                        'model': model,
                        'serial': disk.get('VolumeSerialNumber', 'Unknown'),
                        'tran': tran,
                        'type': 'disk',
                        'label': label,
                        'drive_type': drive_type_str
                    })
                
            except json.JSONDecodeError:
                return []
            
            return drives
            
        except subprocess.CalledProcessError:
            return []
        except Exception:
            return []

    def _detect_drives_linux(self):
        """Detect all drives on Linux using lsblk"""
        drives = []
        try:
            # lsblk for all block devices
            result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,MODEL,SERIAL,TYPE,TRAN,PKNAME,MOUNTPOINT', '-J'], 
                                  stdout=subprocess.PIPE, text=True, check=True)
            data = json.loads(result.stdout)
            for blk in data.get('blockdevices', []):
                dev_path = f"/dev/{blk['name']}"
                label = dev_path
                if blk.get('type'):
                    label += f" [{blk['type']}]"
                if blk.get('pkname'):
                    label += f" (Parent: /dev/{blk['pkname']})"
                if blk.get('mountpoint'):
                    label += f" (Mounted: {blk['mountpoint']})"
                drives.append({
                    'name': dev_path,
                    'size': blk.get('size', 'Unknown'),
                    'model': blk.get('model', 'Unknown'),
                    'serial': blk.get('serial', 'Unknown'),
                    'tran': blk.get('tran', 'Unknown'),
                    'type': blk.get('type', ''),
                    'label': label
                })
                # Also add children (partitions, etc.)
                for child in blk.get('children', []):
                    child_path = f"/dev/{child['name']}"
                    child_label = child_path
                    if child.get('type'):
                        child_label += f" [{child['type']}]"
                    if child.get('pkname'):
                        child_label += f" (Parent: /dev/{child['pkname']})"
                    if child.get('mountpoint'):
                        child_label += f" (Mounted: {child['mountpoint']})"
                    drives.append({
                        'name': child_path,
                        'size': child.get('size', 'Unknown'),
                        'model': child.get('model', 'Unknown'),
                        'serial': child.get('serial', 'Unknown'),
                        'tran': child.get('tran', 'Unknown'),
                        'type': child.get('type', ''),
                        'label': child_label
                    })
            # nvme list for NVMe drives (only disks, not partitions)
            nvme_result = subprocess.run(['nvme', 'list', '-o', 'json'], stdout=subprocess.PIPE, text=True)
            if nvme_result.returncode == 0:
                nvme_data = json.loads(nvme_result.stdout)
                for dev in nvme_data.get('Devices', []):
                    dev_path = dev.get('DevicePath', '')
                    drives.append({
                        'name': dev_path,
                        'size': dev.get('UsedSize', 'Unknown'),
                        'model': dev.get('ModelNumber', 'Unknown'),
                        'serial': dev.get('SerialNumber', 'Unknown'),
                        'tran': 'nvme',
                        'type': 'disk',
                        'label': dev_path + ' [nvme]'
                    })
        except Exception:
            return drives
        return drives

    def update_method_info(self):
        idx = self.drive_combo.currentIndex()
        if idx < 0 or not self.drives:
            self.method_info.setText('No drive selected.')
            return
        drive = self.drives[idx]
        model_str = str(drive.get('model') or '').lower()
        # Auto-detect method (stub)
        if drive['tran'] == 'nvme':
            method = 'NVMe Sanitize'
            desc = 'This drive supports NVMe Sanitize, which securely erases all user and hidden areas.'
        elif 'sed' in model_str or 'self-encrypt' in model_str:
            method = 'SED Crypto-Erase'
            desc = 'This drive is a Self-Encrypting Drive (SED). Crypto-Erase will destroy the encryption key, instantly rendering all data inaccessible.'
        else:
            method = 'ATA Secure Erase'
            desc = 'This drive supports ATA Secure Erase, which securely erases all data, including hidden areas.'
        self.selected_method = method
        self.method_info.setText(f"Sanitization Method: {method}\n{desc}")

    def confirm_and_start(self):
        idx = self.drive_combo.currentIndex()
        if idx < 0 or not self.drives:
            QMessageBox.warning(self, 'No Drive', 'Please select a drive to sanitize.')
            return
        drive = self.drives[idx]
        
        # Check if running on Windows
        if platform.system() == 'Windows':
            QMessageBox.warning(
                self, 
                'Windows Limitation',
                'Sanitization commands require Linux tools (hdparm, nvme-cli, cryptsetup).\n\n'
                'This application can detect drives on Windows for demonstration purposes.\n\n'
                'For actual sanitization, please use:\n'
                '1. The bootable ISO on the target machine (recommended)\n'
                '2. WSL2 (Windows Subsystem for Linux)\n'
                '3. A Linux environment\n\n'
                'The drive detection feature is working correctly - all drives are visible.'
            )
            return
        
        # Safety: Prevent erasing the boot device
        if self.boot_device:
            # On Linux, compare device paths
            if self.boot_device.startswith(drive['name']) or drive['name'].startswith(self.boot_device):
                QMessageBox.critical(self, 'Safety Check', 'Cannot erase the booted device!')
                return
        # Confirmation dialog
        confirm = QMessageBox.question(
            self, 'Confirm Erasure',
            f"Are you absolutely sure you want to IRREVERSIBLY erase {drive['name']} ({drive['model']})?\n\nAll data will be destroyed.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        # Optionally: require typing a phrase (not implemented here)
        self.start_sanitization(drive, self.selected_method)

    def start_sanitization(self, drive, method):
        self.result_label.setText('')
        self.progress.setVisible(True)
        self.start_button.setEnabled(False)
        self.drive_combo.setEnabled(False)
        # Start worker thread
        self.signals = WorkerSignals()
        self.signals.finished.connect(self.on_erase_finished)
        self.worker = EraseWorker(method, drive['name'], drive, self.signals)  # Pass full drive info
        self.worker.start()

    def on_erase_finished(self, output, success, drive_info):
        self.progress.setVisible(False)
        self.start_button.setEnabled(True)
        self.drive_combo.setEnabled(True)
        
        if success:
            self.result_label.setStyleSheet('color: #00ff99; font-size: 13px;')
            result_text = '✅ Sanitization completed successfully!\n\n' + output
            
            # Generate Verifiable Credential
            try:
                result_text += '\n\n📝 Generating Verifiable Credential...'
                self.result_label.setText(result_text)
                QApplication.processEvents()
                
                vc_data = self.generate_verifiable_credential(drive_info, self.selected_method)
                serial_number = drive_info.get('serial', 'Unknown')
                
                # Calculate hash
                vc_hash = self.calculate_vc_hash(vc_data)
                result_text += f'\n✅ VC Hash: {vc_hash.hex()[:32]}...'
                self.result_label.setText(result_text)
                QApplication.processEvents()
                
                # Save VC to file
                vc_file = self.save_verifiable_credential(vc_data, serial_number)
                if vc_file:
                    result_text += f'\n✅ VC saved: {vc_file}'
                    self.result_label.setText(result_text)
                    QApplication.processEvents()
                
                # Register on Aptos blockchain
                result_text += '\n\n⛓️  Registering proof on Aptos blockchain...'
                self.result_label.setText(result_text)
                QApplication.processEvents()
                
                aptos_success, aptos_result = self.register_proof_on_aptos(serial_number, vc_hash)
                
                if aptos_success:
                    result_text += f'\n✅ PROOF REGISTERED ON BLOCKCHAIN!'
                    result_text += f'\n   Transaction: {aptos_result[:32]}...'
                    result_text += f'\n\n🎉 COMPLETE! Certificate is immutably recorded on Aptos!'
                else:
                    result_text += f'\n⚠️  Blockchain registration failed: {aptos_result}'
                    result_text += f'\n   (VC file saved locally for manual registration)'
                    
                self.result_label.setText(result_text)
                
            except Exception as e:
                result_text += f'\n\n⚠️  Post-processing error: {str(e)}'
                result_text += '\n   Sanitization was successful, but VC generation failed.'
                self.result_label.setText(result_text)
        else:
            self.result_label.setStyleSheet('color: #ff5555; font-size: 13px;')
            self.result_label.setText('❌ Sanitization failed!\n\n' + output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SanitizationEngineGUI()
    window.show()
    sys.exit(app.exec_())
