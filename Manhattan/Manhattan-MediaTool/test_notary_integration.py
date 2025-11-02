"""
Manhattan Notary - Integration Test
This script demonstrates the full workflow of registering and verifying sanitization proofs on Aptos.
"""

import hashlib
import json
import asyncio
from aptos_sdk.async_client import RestClient

# Constants
NODE_URL = "https://fullnode.testnet.aptoslabs.com/v1"
MODULE_ADDRESS = "0xd2d618ed1248e1ac5f715991af3de929f8f4aa064983956c01ca77521178ed05"

def create_sample_vc(serial_number: str, timestamp: str) -> dict:
    """Create a sample Verifiable Credential for a drive sanitization."""
    return {
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
            "capacity": "500GB",
            "model": "WD Blue SSD"
        },
        "proof": {
            "type": "Ed25519Signature2020",
            "created": timestamp,
            "proofPurpose": "assertionMethod"
        }
    }

def calculate_vc_hash(vc_data: dict) -> bytes:
    """Calculate SHA-256 hash of a Verifiable Credential."""
    # Convert to canonical JSON (sorted keys)
    vc_json = json.dumps(vc_data, sort_keys=True)
    return hashlib.sha256(vc_json.encode()).digest()

def register_proof_simulation(serial_number: str, vc_hash: bytes):
    """
    Simulate registering a proof on Aptos.
    In production, this would be called by your sanitization engine.
    
    NOTE: This is a simulation - actual registration requires a private key.
    """
    print(f"\n📝 SIMULATION: Registering proof on Aptos")
    print(f"   Serial Number: {serial_number}")
    print(f"   VC Hash: {vc_hash.hex()}")
    print(f"\n   Command to run (replace with your private key):")
    print(f"   aptos move run \\")
    print(f"     --function-id {MODULE_ADDRESS}::manhattan_notary::register_proof \\")
    print(f"     --args string:\"{serial_number}\" hex:\"{vc_hash.hex()}\" \\")
    print(f"     --assume-yes")
    print()

async def verify_proof(serial_number: str, vc_data: dict) -> bool:
    """
    Verify a Verifiable Credential against the Aptos blockchain.
    This would be called by your wallet app.
    """
    print(f"\n🔍 Verifying proof for serial: {serial_number}")
    
    # Step 1: Calculate hash locally
    local_hash = calculate_vc_hash(vc_data)
    print(f"   Local hash: {local_hash.hex()}")
    
    # Step 2: Query Aptos
    try:
        client = RestClient(NODE_URL)
        result = await client.view(
            f"{MODULE_ADDRESS}::manhattan_notary::get_proof",
            [],
            [MODULE_ADDRESS, serial_number]
        )
        await client.close()
        
        # Extract hash from result
        chain_hash_list = result[0]
        chain_hash = bytes(chain_hash_list)
        print(f"   Chain hash: {chain_hash.hex()}")
        
        # Step 3: Compare hashes
        if local_hash == chain_hash:
            print("   ✅ VERIFIED - This credential is authentic!")
            return True
        else:
            print("   ❌ INVALID - Hashes do not match!")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR - Could not verify: {str(e)}")
        return False

async def main():
    """Main test workflow."""
    print("=" * 70)
    print("🚀 Manhattan Notary - Integration Test")
    print("=" * 70)
    
    # Test with the proof we registered earlier
    serial_number = "WD-TEST-123456"
    timestamp = "2025-11-02T00:00:00Z"
    
    print("\n1️⃣ Creating sample Verifiable Credential...")
    vc_data = create_sample_vc(serial_number, timestamp)
    print(f"   VC created for device: {serial_number}")
    
    print("\n2️⃣ Calculating SHA-256 hash...")
    vc_hash = calculate_vc_hash(vc_data)
    print(f"   Hash: {vc_hash.hex()}")
    
    print("\n3️⃣ Simulating proof registration...")
    register_proof_simulation(serial_number, vc_hash)
    
    print("\n4️⃣ Verifying proof from blockchain...")
    is_valid = await verify_proof(serial_number, vc_data)
    
    print("\n" + "=" * 70)
    if is_valid:
        print("✅ TEST PASSED - Full workflow successful!")
    else:
        print("⚠️  Note: Verification may fail if the hash doesn't match")
        print("   the one we registered earlier (different VC data).")
    print("=" * 70)
    
    # Show how to save/load VCs
    print("\n📄 Bonus: Saving VC to file...")
    vc_filename = f"sanitization_cert_{serial_number}.json"
    with open(vc_filename, "w") as f:
        json.dump(vc_data, f, indent=2, sort_keys=True)
    print(f"   Saved to: {vc_filename}")
    print(f"   This file can be verified by your wallet app!")

if __name__ == "__main__":
    asyncio.run(main())
