# Manhattan Notary - Aptos Smart Contract

## Overview

The **Manhattan Notary** is an Aptos Move module that serves as an immutable, on-chain registry for data sanitization proofs. It creates a permanent, verifiable record of every drive wipe performed by The Manhattan Project sanitization engine.

## Architecture

This smart contract is the backbone of a full-stack Aptos dApp:

```
Sanitization Engine → Aptos Blockchain → Wallet Verification
     (Backend)           (Notary)            (Frontend)
```

### How It Works

1. **Sanitization Engine (Backend)**
   - Wipes a drive using secure erasure methods
   - Generates a JSON Verifiable Credential (VC)
   - Calculates SHA-256 hash of the VC
   - Calls `register_proof(serial_number, vc_hash)` on Aptos
   - Transaction is immutably recorded on-chain

2. **Aptos Blockchain (Notary)**
   - Stores mapping: `Serial Number → VC Hash`
   - Provides cryptographic proof of sanitization
   - Acts as high-speed, immutable public notary

3. **Wallet App (Frontend)**
   - User loads VC file
   - Calculates SHA-256 hash locally
   - Calls `get_proof(serial_number)` view function
   - Compares hashes: Match = ✅ Verified

## Module Details

### Resource: `ProofRegistry`

```move
struct ProofRegistry has key {
    proofs: Table<String, vector<u8>>
}
```

Stores the immutable mapping of device serial numbers to VC hashes.

### Functions

#### `init_module(publisher: &signer)`
- Automatically runs when module is published
- Creates empty `ProofRegistry` and moves it to publisher's account

#### `register_proof(owner: &signer, serial_number: String, vc_hash: vector<u8>)`
- **Entry function** - called by sanitization engine
- **Owner-only** - only module publisher can register proofs
- Records the SHA-256 hash of a Verifiable Credential on-chain
- Creates immutable audit trail

#### `get_proof(registry_owner: address, serial_number: String): vector<u8>`
- **View function** - anyone can verify proofs
- Returns the VC hash for a given serial number
- Used by wallet app to verify credentials

### Error Codes

- `E_NOT_AUTHORIZED (1)` - Caller is not authorized
- `E_PROOF_NOT_FOUND (2)` - No proof exists for this serial number
- `E_REGISTRY_NOT_FOUND (3)` - Registry doesn't exist

## Deployment

### 1. Initialize Aptos CLI

```bash
aptos init
```

### 2. Compile the Module

```bash
cd aptos
aptos move compile
```

### 3. Publish the Module

```bash
aptos move publish
```

### 4. Get Your Module Address

After publishing, note your account address. This will be used in your Python apps.

## Integration with Python Apps

### Sanitization Engine Integration

After wiping a drive, your sanitization engine should:

```python
import hashlib
import json
from aptos_sdk.client import RestClient
from aptos_sdk.account import Account

# 1. Generate VC
vc_data = {
    "type": "SanitizationCertificate",
    "serial": device_serial,
    "timestamp": timestamp,
    # ... other VC fields
}

# 2. Calculate hash
vc_json = json.dumps(vc_data, sort_keys=True)
vc_hash = hashlib.sha256(vc_json.encode()).digest()

# 3. Register on Aptos
client = RestClient("https://fullnode.mainnet.aptoslabs.com/v1")
account = Account.load_key("your_private_key")

payload = {
    "type": "entry_function_payload",
    "function": f"{your_address}::manhattan_notary::register_proof",
    "type_arguments": [],
    "arguments": [device_serial, list(vc_hash)]
}

txn = client.submit_transaction(account, payload)
client.wait_for_transaction(txn)
```

### Wallet App Integration

To verify a VC:

```python
import hashlib
import json
from aptos_sdk.client import RestClient

# 1. Load VC file
with open("sanitization_cert.json", "r") as f:
    vc_data = json.load(f)

# 2. Calculate hash locally
vc_json = json.dumps(vc_data, sort_keys=True)
local_hash = hashlib.sha256(vc_json.encode()).digest()

# 3. Query Aptos
client = RestClient("https://fullnode.mainnet.aptoslabs.com/v1")
registry_owner = "0x..."  # Your published module address

result = client.view_function(
    f"{registry_owner}::manhattan_notary::get_proof",
    [],
    [registry_owner, vc_data["serial"]]
)

chain_hash = bytes(result[0])

# 4. Verify
if local_hash == chain_hash:
    print("✅ VERIFIED - This credential is authentic!")
else:
    print("❌ INVALID - Hashes do not match!")
```

## Security Features

1. **Immutability**: Once recorded, proofs cannot be deleted
2. **Owner-Only Registration**: Only the module publisher can register proofs
3. **Public Verification**: Anyone can verify proofs (transparency)
4. **Cryptographic Proof**: SHA-256 ensures data integrity
5. **Blockchain Audit Trail**: All registrations are permanently logged

## Why This is "Judge-Proof"

- ✅ **Immutable**: Blockchain records cannot be altered
- ✅ **Timestamped**: Every transaction has a block timestamp
- ✅ **Transparent**: Anyone can verify the proof
- ✅ **Decentralized**: No single point of failure
- ✅ **Cryptographically Secure**: SHA-256 + blockchain signatures

## Next Steps

1. Publish the module to Aptos
2. Update your sanitization engine to call `register_proof()`
3. Update your wallet app to call `get_proof()`
4. Test the full workflow end-to-end

---

**This makes The Manhattan Project a true full-stack Aptos dApp!** 🚀
