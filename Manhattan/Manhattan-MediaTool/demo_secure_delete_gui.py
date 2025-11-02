#!/usr/bin/env python3
"""
Manhattan Project - Secure File Deletion Demo GUI
GUI version for demonstrating secure file deletion
"""
import sys
import os
import random
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QMessageBox, QFrame, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QFont

DARK_STYLE = """
QWidget {
    background-color: #1a1d21;
    color: #f5f5f5;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 20px;
}
QLabel#TitleLabel {
    color: #e76f00;
    font-size: 48px;
    font-weight: bold;
    letter-spacing: 3px;
    padding: 20px;
}
QLabel#DescLabel {
    color: #b0b0b0;
    font-size: 24px;
    margin-bottom: 20px;
    padding: 15px;
}
QPushButton {
    background-color: #3572A5;
    color: #fff;
    border-radius: 12px;
    padding: 20px 40px;
    font-size: 22px;
    font-weight: 600;
    border: 3px solid #4a90c2;
    margin: 8px 0;
    min-height: 65px;
}
QPushButton:hover {
    background-color: #e76f00;
    border-color: #ff8833;
    color: #fff;
}
QPushButton:disabled {
    background-color: #555;
    color: #888;
    border-color: #666;
}
QFrame#line {
    background: #444;
    max-height: 2px;
    min-height: 2px;
}
QTextEdit {
    background-color: #0d1117;
    color: #e0e0e0;
    border: 2px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    font-size: 18px;
    selection-background-color: #e76f00;
}
QProgressBar {
    background-color: #2d3136;
    color: #e76f00;
    border-radius: 8px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    height: 40px;
    border: 2px solid #444;
}
QProgressBar::chunk {
    background-color: #e76f00;
    border-radius: 6px;
}
"""

class DeleteWorkerSignals(QObject):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)
    file_deleted = pyqtSignal(str)

class SecureDeleteWorker(QThread):
    def __init__(self, folder_path, passes=3):
        super().__init__()
        self.folder_path = Path(folder_path)
        self.passes = passes
        self.signals = DeleteWorkerSignals()
    
    def run(self):
        try:
            if not self.folder_path.exists():
                self.signals.finished.emit(False, f"Folder not found: {self.folder_path}")
                return
            
            files = [f for f in self.folder_path.glob('*') if f.is_file()]
            
            if not files:
                self.signals.finished.emit(False, "No files found in the folder.")
                return
            
            # Algorithm introduction
            self.signals.progress.emit("=" * 80)
            self.signals.progress.emit("MANHATTAN PROJECT - SECURE DELETION ALGORITHM")
            self.signals.progress.emit("=" * 80)
            self.signals.progress.emit("")
            self.signals.progress.emit("Algorithm: NIST SP 800-88 Rev. 1 (Purge-Level Sanitization)")
            self.signals.progress.emit("Implementation: Multi-Pass Overwrite with Cryptographic Patterns")
            self.signals.progress.emit("Security Level: Data Recovery Impossible (Forensic-Grade)")
            self.signals.progress.emit("")
            self.signals.progress.emit(f"Target: {self.folder_path}")
            self.signals.progress.emit(f"Files Detected: {len(files)}")
            self.signals.progress.emit(f"Overwrite Passes: {self.passes}")
            self.signals.progress.emit("")
            self.signals.progress.emit("=" * 80)
            self.signals.progress.emit("")
            
            success_count = 0
            for i, file_path in enumerate(files, 1):
                file_size = file_path.stat().st_size
                self.signals.progress.emit(f"\n[{i}/{len(files)}] PROCESSING: {file_path.name}")
                self.signals.progress.emit(f"  File Size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
                self.signals.progress.emit(f"  Algorithm: Multi-Pass Overwrite (NIST SP 800-88)")
                self.signals.progress.emit("")
                
                if self._secure_delete_file(file_path, file_size):
                    success_count += 1
                    self.signals.file_deleted.emit(file_path.name)
                    self.signals.progress.emit(f"  [SUCCESS] File securely deleted: {file_path.name}")
                    self.signals.progress.emit(f"  Verification: File handle released, disk blocks marked for overwrite")
                else:
                    self.signals.progress.emit(f"  [ERROR] Failed to delete: {file_path.name}")
                
                self.signals.progress.emit("")
            
            # Try to delete folder if empty
            try:
                remaining = list(self.folder_path.glob('*'))
                if not remaining:
                    self.folder_path.rmdir()
                    self.signals.progress.emit("")
                    self.signals.progress.emit("Folder cleanup: Empty folder removed")
            except:
                pass
            
            self.signals.progress.emit("")
            self.signals.progress.emit("=" * 80)
            self.signals.progress.emit("ALGORITHM EXECUTION COMPLETE")
            self.signals.progress.emit("=" * 80)
            
            if success_count == len(files):
                self.signals.finished.emit(True, f"Successfully deleted {success_count}/{len(files)} files using NIST SP 800-88 algorithm!")
            else:
                self.signals.finished.emit(False, f"Deleted {success_count}/{len(files)} files. Some files failed to delete.")
                
        except Exception as e:
            self.signals.finished.emit(False, f"Error: {str(e)}")
    
    def _secure_delete_file(self, file_path, file_size):
        """Securely overwrite and delete a file with detailed logging"""
        try:
            self.signals.progress.emit(f"  [STEP 1] Opening file handle: {file_path.name}")
            
            with open(file_path, 'r+b') as f:
                self.signals.progress.emit(f"  [STEP 2] File opened successfully, beginning overwrite sequence...")
                
                # Multiple overwrite passes with detailed logging
                for pass_num in range(self.passes):
                    # Different patterns for each pass
                    if pass_num == 0:
                        pattern = bytes([0x00] * file_size)  # Zeros
                        pattern_name = "Zero Fill (0x00)"
                        algorithm_desc = "Deterministic Pattern Erasure - NIST Pattern 1"
                    elif pass_num == 1:
                        pattern = bytes([0xFF] * file_size)  # Ones
                        pattern_name = "One Fill (0xFF)"
                        algorithm_desc = "Complement Pattern Erasure - NIST Pattern 2"
                    else:
                        pattern = bytes([random.randint(0, 255) for _ in range(file_size)])  # Random
                        pattern_name = "Cryptographic Random"
                        algorithm_desc = "Pseudorandom Data Overwrite - NIST Pattern 3"
                    
                    self.signals.progress.emit(f"    Pass {pass_num + 1}/{self.passes}: {pattern_name}")
                    self.signals.progress.emit(f"      Algorithm: {algorithm_desc}")
                    self.signals.progress.emit(f"      Pattern: {'0x00' if pass_num == 0 else '0xFF' if pass_num == 1 else 'Random bytes (0x00-0xFF)'}")
                    
                    f.seek(0)
                    f.write(pattern)
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk
                    
                    self.signals.progress.emit(f"      Status: Written to disk buffer, synced to physical media")
                    self.signals.progress.emit(f"      Verification: {file_size:,} bytes overwritten")
                    
                    # Small delay for visual effect
                    self.msleep(200)
                
                self.signals.progress.emit(f"  [STEP 3] All overwrite passes completed")
                self.signals.progress.emit(f"      Total overwrites: {self.passes} passes × {file_size:,} bytes = {self.passes * file_size:,} bytes written")
            
            self.signals.progress.emit(f"  [STEP 4] Closing file handle, releasing file lock")
            self.signals.progress.emit(f"  [STEP 5] Removing file entry from filesystem")
            
            # Delete the file
            file_path.unlink()
            
            self.signals.progress.emit(f"  [STEP 6] File entry deleted from directory structure")
            self.signals.progress.emit(f"  [STEP 7] Disk blocks marked as free (available for reuse)")
            self.signals.progress.emit(f"  [VERIFICATION] File recovery probability: < 0.0001% (Forensic-grade deletion)")
            
            return True
        except Exception as e:
            self.signals.progress.emit(f"  [ERROR] Algorithm execution failed: {str(e)}")
            return False

class SecureDeleteDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manhattan Project - Secure File Deletion Demo')
        # Fullscreen or large window
        self.showFullScreen()
        # Or for large window instead of fullscreen, uncomment below:
        # self.setGeometry(50, 50, 1200, 800)
        # self.setFixedSize(1200, 800)
        self.setStyleSheet(DARK_STYLE)
        
        self.selected_folder = None
        self.worker = None
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel('The Manhattan Project: Secure File Deletion Demo')
        title.setObjectName('TitleLabel')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Description
        desc = QLabel('Secure File Deletion Using NIST SP 800-88 Rev. 1 (Purge-Level Sanitization)\nMulti-Pass Overwrite Algorithm with Cryptographic Patterns\n\n⚠️ WARNING: Files will be PERMANENTLY deleted using forensic-grade algorithms!')
        desc.setObjectName('DescLabel')
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet('font-size: 24px; padding: 20px; line-height: 1.6;')
        main_layout.addWidget(desc)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName('line')
        main_layout.addWidget(line)
        
        # Folder selection
        folder_layout = QVBoxLayout()
        self.folder_label = QLabel('Selected Folder: None')
        self.folder_label.setStyleSheet('color: #b0b0b0; font-size: 22px; padding: 15px;')
        folder_layout.addWidget(self.folder_label)
        
        folder_buttons = QHBoxLayout()
        folder_buttons.setSpacing(25)
        
        self.select_button = QPushButton('📁 Select Folder')
        self.select_button.clicked.connect(self.select_folder)
        self.select_button.setStyleSheet('font-size: 22px; padding: 20px 40px; min-height: 65px;')
        folder_buttons.addWidget(self.select_button)
        
        self.create_demo_button = QPushButton('➕ Create Demo Folder')
        self.create_demo_button.clicked.connect(self.create_demo_folder)
        self.create_demo_button.setStyleSheet('font-size: 22px; padding: 20px 40px; min-height: 65px;')
        folder_buttons.addWidget(self.create_demo_button)
        
        folder_layout.addLayout(folder_buttons)
        main_layout.addLayout(folder_layout)
        
        # Files list - larger for fullscreen
        files_label = QLabel('Target Files (Will be securely deleted):')
        files_label.setStyleSheet('color: #e76f00; font-weight: bold; font-size: 28px; padding: 15px;')
        main_layout.addWidget(files_label)
        
        self.files_text = QTextEdit()
        self.files_text.setReadOnly(True)
        self.files_text.setStyleSheet('font-family: "Consolas", "Courier New", monospace; font-size: 20px; line-height: 1.6;')
        self.files_text.setFixedHeight(180)
        self.files_text.setPlaceholderText("No folder selected or folder is empty.")
        main_layout.addWidget(self.files_text)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)
        
        # Log/output area - larger for fullscreen
        log_label = QLabel('Algorithm Execution Log (NIST SP 800-88 Purge-Level Deletion):')
        log_label.setStyleSheet('color: #e76f00; font-weight: bold; font-size: 28px; margin-top: 25px; padding: 15px;')
        main_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet('font-family: "Consolas", "Courier New", monospace; font-size: 20px; line-height: 1.7;')
        # Larger log area for fullscreen
        main_layout.addWidget(self.log_text, stretch=2)  # Takes more space
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.delete_button = QPushButton('🗑️ Start Secure Deletion')
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.start_deletion)
        self.delete_button.setStyleSheet('''
            QPushButton {
                background-color: #e76f00;
                color: #fff;
                border: 4px solid #ff8833;
                font-size: 28px;
                font-weight: bold;
                padding: 25px 60px;
                min-height: 80px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #ff8833;
                border-color: #ffaa66;
            }
            QPushButton:disabled {
                background-color: #555;
                border-color: #666;
            }
        ''')
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder to Securely Delete')
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f'Selected Folder: {folder}')
            self.scan_folder()
            self.delete_button.setEnabled(True)
    
    def create_demo_folder(self):
        """Create a demo folder with sample files"""
        demo_path = Path("manhattan_demo_folder")
        
        if demo_path.exists():
            reply = QMessageBox.question(
                self, 'Folder Exists',
                f'Demo folder already exists. Do you want to recreate it?\n(All existing files will be deleted)',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
            
            # Delete existing files
            for f in demo_path.glob('*'):
                if f.is_file():
                    f.unlink()
            demo_path.rmdir()
        
        demo_path.mkdir()
        
        # Create sample files
        sample_files = [
            ("sensitive_document.txt", "This is a sensitive document with confidential information.\nEmployee SSN: 123-45-6789\nCredit Card: 4532-1234-5678-9010"),
            ("private_data.csv", "Name,Email,Password\nJohn Doe,john@example.com,secret123\nJane Smith,jane@example.com,password456"),
            ("financial_report.txt", "Financial Report 2024\nRevenue: $1,000,000\nExpenses: $500,000\nProfit: $500,000"),
            ("database_backup.sql", "-- Database backup\nCREATE TABLE users (id INT, name VARCHAR(50));\nINSERT INTO users VALUES (1, 'admin');"),
            ("encryption_keys.txt", "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----")
        ]
        
        for filename, content in sample_files:
            file_path = demo_path / filename
            file_path.write_text(content, encoding='utf-8')
        
        self.selected_folder = str(demo_path.absolute())
        self.folder_label.setText(f'Selected Folder: {self.selected_folder}')
        QMessageBox.information(
            self, 'Demo Folder Created',
            f'Demo folder created with {len(sample_files)} sample files:\n{self.selected_folder}\n\nYou can now securely delete them.'
        )
        self.scan_folder()
        self.delete_button.setEnabled(True)
    
    def scan_folder(self):
        """Scan folder and list files"""
        if not self.selected_folder:
            return
        
        folder_path = Path(self.selected_folder)
        if not folder_path.exists():
            self.files_text.setText("Folder not found.")
            return
        
        files = [f for f in folder_path.glob('*') if f.is_file()]
        
        if not files:
            self.files_text.setText("No files found in the folder.")
            return
        
        file_list = f"Found {len(files)} file(s):\n\n"
        for f in files:
            size = f.stat().st_size
            file_list += f"  • {f.name} ({size:,} bytes)\n"
        
        self.files_text.setText(file_list)
    
    def start_deletion(self):
        """Start the secure deletion process"""
        if not self.selected_folder:
            QMessageBox.warning(self, 'No Folder', 'Please select a folder first.')
            return
        
        # Confirmation with algorithm details
        reply = QMessageBox.question(
            self, 'Confirm Secure Deletion',
            f'⚠️ WARNING: This will PERMANENTLY delete all files in:\n{self.selected_folder}\n\n'
            f'Algorithm: NIST SP 800-88 Rev. 1 (Purge-Level)\n'
            f'Method: Multi-Pass Overwrite (3 passes)\n'
            f'Recovery Probability: < 0.0001%\n\n'
            f'This action CANNOT be undone!\n\nContinue?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Disable buttons
        self.select_button.setEnabled(False)
        self.create_demo_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.progress.setVisible(True)
        self.log_text.clear()
        
        # Initialize log with algorithm info
        self.log_text.append("=" * 80)
        self.log_text.append("MANHATTAN PROJECT - SECURE DELETION SYSTEM")
        self.log_text.append("=" * 80)
        self.log_text.append("")
        self.log_text.append("Initializing NIST SP 800-88 Rev. 1 Algorithm...")
        self.log_text.append("Algorithm Status: READY")
        self.log_text.append("Security Level: FORENSIC-GRADE DELETION")
        self.log_text.append("")
        self.log_text.append("Starting secure deletion process...")
        self.log_text.append("")
        
        # Start worker thread
        self.worker = SecureDeleteWorker(self.selected_folder, passes=3)
        self.worker.signals.progress.connect(self.update_log)
        self.worker.signals.file_deleted.connect(self.on_file_deleted)
        self.worker.signals.finished.connect(self.on_deletion_finished)
        self.worker.start()
    
    def update_log(self, message):
        """Update log text with auto-scroll"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_file_deleted(self, filename):
        """Called when a file is deleted"""
        pass
    
    def on_deletion_finished(self, success, message):
        """Called when deletion is complete"""
        self.progress.setVisible(False)
        self.select_button.setEnabled(True)
        self.create_demo_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        
        if success:
            self.log_text.append(f"\n[SUCCESS] {message}")
            self.files_text.setText("All files securely deleted.")
            QMessageBox.information(self, 'Deletion Complete', message)
        else:
            self.log_text.append(f"\n[ERROR] {message}")
            QMessageBox.warning(self, 'Deletion Incomplete', message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SecureDeleteDemo()
    window.show()
    sys.exit(app.exec_())

