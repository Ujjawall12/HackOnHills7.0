#!/usr/bin/env python3
"""
Simple test script to verify all applications can be imported and initialized.
This helps catch import errors before running the full GUI.
"""

import sys

def test_media_creator():
    """Test Media Creator imports"""
    try:
        sys.path.insert(0, 'client/media_creator')
        from PyQt5.QtWidgets import QApplication
        import main as mc
        print("[OK] Media Creator: Imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Media Creator: Import failed - {e}")
        return False

def test_wallet_app():
    """Test Wallet App imports"""
    try:
        sys.path.insert(0, 'client/wallet_app')
        from PyQt5.QtWidgets import QApplication
        import main as wa
        print("[OK] Wallet App: Imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Wallet App: Import failed - {e}")
        return False

def test_sanitization_engine():
    """Test Sanitization Engine imports"""
    try:
        sys.path.insert(0, 'sanitization_engine/gui')
        from PyQt5.QtWidgets import QApplication
        import main as se
        print("[OK] Sanitization Engine: Imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Sanitization Engine: Import failed - {e}")
        return False

if __name__ == '__main__':
    print("Testing Manhattan Project Applications...\n")
    
    results = [
        test_media_creator(),
        test_wallet_app(),
        test_sanitization_engine()
    ]
    
    print("\n" + "="*50)
    if all(results):
        print("[SUCCESS] All applications are ready to run!")
        sys.exit(0)
    else:
        print("[FAILED] Some applications have import errors.")
        sys.exit(1)

