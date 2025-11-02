"""
Manhattan Notary - Simple Demo
Demonstrates registration and verification workflow
"""

import hashlib
import json

# Constants
MODULE_ADDRESS = "0xd2d618ed1248e1ac5f715991af3de929f8f4aa064983956c01ca77521178ed05"

print("=" * 70)
print("🎉 Manhattan Notary - Full-Stack Aptos dApp")
print("=" * 70)

# ========== STEP 1: Sanitization Engine (Backend) ==========
print("\n📦 STEP 1: Sanitization Engine (After Drive Wipe)")
print("-" * 70)

serial_number = "WD-PROD-789ABC"
timestamp = "2025-11-02T12:00:00Z"

# Create Verifiable Credential
vc_data = {
    "@context": ["https://www.w3.org/2018/credentials/v1"],
    "type": ["VerifiableCredential", "SanitizationCertificate"],
    "issuer": "did:manhattan:sanitization-engine",
    "issuanceDate": timestamp,
    "credentialSubject": {
        "id": f"urn:device:{serial_number}",
        "serialNumber": serial_number,
        "sanitizationMethod": "ATA Secure Erase",
        "passes": 1,
        "timestamp": timestamp,
        "capacity": "1TB",
        "model": "Samsung EVO SSD"
    },
    "proof": {
        "type": "Ed25519Signature2020",
        "created": timestamp,
        "proofPurpose": "assertionMethod"
    }
}

print(f"✅ Drive wiped: {serial_number}")
print(f"✅ VC generated")

# Calculate hash
vc_json = json.dumps(vc_data, sort_keys=True)
vc_hash = hashlib.sha256(vc_json.encode()).digest()

print(f"✅ SHA-256 hash calculated: {vc_hash.hex()}")

# Save VC to file
vc_filename = f"sanitization_cert_{serial_number}.json"
with open(vc_filename, "w") as f:
    json.dump(vc_data, f, indent=2, sort_keys=True)
print(f"✅ VC saved to: {vc_filename}")

# ========== STEP 2: Register on Aptos Blockchain ==========
print("\n⛓️  STEP 2: Register Proof on Aptos Blockchain")
print("-" * 70)

register_cmd = f"""aptos move run \\
  --function-id {MODULE_ADDRESS}::manhattan_notary::register_proof \\
  --args string:"{serial_number}" hex:"{vc_hash.hex()}" \\
  --assume-yes"""

print("Run this command to register the proof:")
print()
print(register_cmd)
print()
print("This creates an IMMUTABLE record on the blockchain! ⛓️")

# ========== STEP 3: Verify from Wallet App ==========
print("\n💼 STEP 3: Verify Proof from Wallet App (Frontend)")
print("-" * 70)

verify_cmd = f"""aptos move view \\
  --function-id {MODULE_ADDRESS}::manhattan_notary::get_proof \\
  --args address:{MODULE_ADDRESS} string:"{serial_number}\""""

print("Your wallet app would:")
print(f"1. Load the VC file: {vc_filename}")
print(f"2. Calculate local hash: {vc_hash.hex()}")
print("3. Query Aptos blockchain:")
print()
print(verify_cmd)
print()
print("4. Compare hashes:")
print("   - If match: ✅ VERIFIED (authentic)")
print("   - If different: ❌ INVALID (tampered)")

# ========== Summary ==========
print("\n" + "=" * 70)
print("📊 SUMMARY: Full-Stack Aptos dApp Workflow")
print("=" * 70)
print()
print("Backend (Sanitization Engine):")
print("  → Wipes drive")
print("  → Generates VC")
print("  → Calculates hash")
print("  → Registers on Aptos ⛓️")
print()
print("Blockchain (Manhattan Notary):")
print(f"  → Stores: {serial_number} → {vc_hash.hex()[:16]}...")
print("  → Immutable")
print("  → Public verification")
print()
print("Frontend (Wallet App):")
print("  → Loads VC file")
print("  → Queries blockchain")
print("  → Verifies authenticity ✅")
print()
print("=" * 70)
print("🎯 This is a TRUE full-stack Aptos dApp!")
print("   • Decentralized storage")
print("   • Cryptographic verification")
print("   • Immutable audit trail")
print("   • No trusted third party needed")
print("=" * 70)
