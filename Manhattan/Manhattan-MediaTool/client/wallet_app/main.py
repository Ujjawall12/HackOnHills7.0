import sys
import json
import hashlib
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFileDialog, QTextEdit, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Aptos Configuration
APTOS_MODULE_ADDRESS = "0xd2d618ed1248e1ac5f715991af3de929f8f4aa064983956c01ca77521178ed05"
APTOS_NETWORK = "testnet"

DARK_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel#TitleLabel {
    color: #e76f00;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 1px;
}
QLabel#SubtitleLabel {
    color: #b0b0b0;
    font-size: 13px;
    margin-bottom: 10px;
}
QLabel#StatusLabel {
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    border-radius: 8px;
}
QPushButton {
    background-color: #3572A5;
    color: #fff;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    margin: 5px 0;
}
QPushButton:hover {
    background-color: #e76f00;
}
QPushButton:disabled {
    background-color: #555;
    color: #888;
}
QTextEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}
QFrame#line {
    background: #444;
    max-height: 1px;
    min-height: 1px;
}
"""

class WalletApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manhattan Project - Wallet & Verification')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(DARK_STYLE)
        
        self.vc_data = None
        self.vc_file_path = None
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel('🔐 Manhattan Wallet')
        title.setObjectName('TitleLabel')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel('Verify Data Sanitization Certificates on Aptos Blockchain')
        subtitle.setObjectName('SubtitleLabel')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName('line')
        layout.addWidget(line)

        # Load VC Button
        self.load_button = QPushButton('📂 Load Verifiable Credential')
        self.load_button.clicked.connect(self.load_vc_file)
        layout.addWidget(self.load_button)

        # VC Display Area
        vc_label = QLabel('Credential Details:')
        vc_label.setStyleSheet('color: #b0b0b0; font-size: 13px; margin-top: 10px;')
        layout.addWidget(vc_label)
        
        self.vc_display = QTextEdit()
        self.vc_display.setReadOnly(True)
        self.vc_display.setPlaceholderText('No credential loaded...')
        self.vc_display.setMinimumHeight(200)
        layout.addWidget(self.vc_display)

        # Verify Button
        self.verify_button = QPushButton('✅ Verify on Aptos Blockchain')
        self.verify_button.clicked.connect(self.verify_credential)
        self.verify_button.setEnabled(False)
        layout.addWidget(self.verify_button)

        # Status Label
        self.status_label = QLabel('')
        self.status_label.setObjectName('StatusLabel')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

        # Verification Details
        details_label = QLabel('Verification Details:')
        details_label.setStyleSheet('color: #b0b0b0; font-size: 13px; margin-top: 10px;')
        layout.addWidget(details_label)
        
        self.details_display = QTextEdit()
        self.details_display.setReadOnly(True)
        self.details_display.setPlaceholderText('Verification results will appear here...')
        self.details_display.setMinimumHeight(150)
        layout.addWidget(self.details_display)

        self.setLayout(layout)

    def load_vc_file(self):
        """Load a Verifiable Credential JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Verifiable Credential",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                self.vc_data = json.load(f)
            
            self.vc_file_path = file_path
            
            # Display VC contents
            display_text = json.dumps(self.vc_data, indent=2)
            self.vc_display.setPlainText(display_text)
            
            # Enable verify button
            self.verify_button.setEnabled(True)
            
            # Hide previous status
            self.status_label.setVisible(False)
            self.details_display.clear()
            
            # Show file loaded message
            QMessageBox.information(
                self,
                "File Loaded",
                f"✅ Credential loaded successfully!\n\nFile: {Path(file_path).name}"
            )
            
        except json.JSONDecodeError:
            QMessageBox.critical(
                self,
                "Invalid File",
                "❌ The selected file is not a valid JSON file."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"❌ Failed to load file:\n\n{str(e)}"
            )

    def calculate_vc_hash(self, vc_data):
        """Calculate SHA-256 hash of a Verifiable Credential"""
        vc_json = json.dumps(vc_data, sort_keys=True)
        return hashlib.sha256(vc_json.encode()).digest()

    def query_aptos_blockchain(self, serial_number):
        """Query the Aptos blockchain for a proof"""
        try:
            # Check if running in aptos directory
            aptos_dir = Path(__file__).parent.parent.parent / "aptos"
            
            cmd = [
                "aptos", "move", "view",
                "--function-id", f"{APTOS_MODULE_ADDRESS}::manhattan_notary::get_proof",
                "--args", f"address:{APTOS_MODULE_ADDRESS}", f"string:{serial_number}"
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
                # Parse the result
                try:
                    output_json = json.loads(result.stdout)
                    chain_hash_hex = output_json.get('Result', [None])[0]
                    if chain_hash_hex:
                        # Remove 0x prefix and convert to bytes
                        chain_hash = bytes.fromhex(chain_hash_hex[2:] if chain_hash_hex.startswith('0x') else chain_hash_hex)
                        return True, chain_hash
                    else:
                        return False, "No hash returned from blockchain"
                except Exception as e:
                    return False, f"Failed to parse blockchain response: {str(e)}"
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                if "not found" in error_msg.lower():
                    return False, "No proof found for this serial number on the blockchain"
                return False, error_msg
                
        except FileNotFoundError:
            return False, "Aptos CLI not found. Please ensure Aptos CLI is installed."
        except subprocess.TimeoutExpired:
            return False, "Query timeout. Please try again."
        except Exception as e:
            return False, str(e)

    def verify_credential(self):
        """Verify the loaded credential against the Aptos blockchain"""
        if not self.vc_data:
            QMessageBox.warning(self, "No Credential", "Please load a credential first.")
            return
        
        try:
            # Extract serial number
            serial_number = self.vc_data.get('credentialSubject', {}).get('serialNumber')
            if not serial_number:
                QMessageBox.critical(
                    self,
                    "Invalid Credential",
                    "❌ Credential does not contain a serial number."
                )
                return
            
            # Step 1: Calculate local hash
            self.details_display.clear()
            details = f"🔍 Verifying credential for device: {serial_number}\n\n"
            details += "Step 1: Calculating local hash...\n"
            self.details_display.setPlainText(details)
            QApplication.processEvents()
            
            local_hash = self.calculate_vc_hash(self.vc_data)
            local_hash_hex = local_hash.hex()
            details += f"✅ Local hash: {local_hash_hex}\n\n"
            self.details_display.setPlainText(details)
            QApplication.processEvents()
            
            # Step 2: Query blockchain
            details += "Step 2: Querying Aptos blockchain...\n"
            self.details_display.setPlainText(details)
            QApplication.processEvents()
            
            success, chain_result = self.query_aptos_blockchain(serial_number)
            
            if not success:
                details += f"❌ Query failed: {chain_result}\n"
                self.details_display.setPlainText(details)
                self.show_status(False, "Verification Failed", chain_result)
                return
            
            chain_hash = chain_result
            chain_hash_hex = chain_hash.hex()
            details += f"✅ Chain hash: {chain_hash_hex}\n\n"
            self.details_display.setPlainText(details)
            QApplication.processEvents()
            
            # Step 3: Compare hashes
            details += "Step 3: Comparing hashes...\n"
            self.details_display.setPlainText(details)
            QApplication.processEvents()
            
            if local_hash == chain_hash:
                details += "✅ HASHES MATCH!\n\n"
                details += "═" * 50 + "\n"
                details += "🎉 VERIFICATION SUCCESSFUL!\n"
                details += "═" * 50 + "\n\n"
                details += "This certificate is AUTHENTIC and has been\n"
                details += "immutably recorded on the Aptos blockchain.\n\n"
                details += f"Device Serial: {serial_number}\n"
                details += f"Blockchain: Aptos {APTOS_NETWORK.capitalize()}\n"
                details += f"Module: {APTOS_MODULE_ADDRESS[:20]}...\n"
                
                self.details_display.setPlainText(details)
                self.show_status(True, "✅ VERIFIED", "This certificate is authentic!")
            else:
                details += "❌ HASHES DO NOT MATCH!\n\n"
                details += "⚠️  WARNING: This certificate may have been tampered with.\n"
                details += "The data in this file does not match what was recorded\n"
                details += "on the blockchain.\n"
                
                self.details_display.setPlainText(details)
                self.show_status(False, "❌ INVALID", "Certificate has been tampered with!")
                
        except Exception as e:
            self.details_display.setPlainText(f"❌ Verification error:\n\n{str(e)}")
            self.show_status(False, "Error", str(e))

    def show_status(self, success, title, message):
        """Show verification status"""
        if success:
            self.status_label.setStyleSheet(
                'background-color: #2d5016; color: #00ff99; '
                'font-size: 16px; font-weight: bold; padding: 15px; '
                'border-radius: 8px; border: 2px solid #00ff99;'
            )
        else:
            self.status_label.setStyleSheet(
                'background-color: #4d1616; color: #ff5555; '
                'font-size: 16px; font-weight: bold; padding: 15px; '
                'border-radius: 8px; border: 2px solid #ff5555;'
            )
        
        self.status_label.setText(f"{title}\n{message}")
        self.status_label.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WalletApp()
    window.show()
    sys.exit(app.exec_())
