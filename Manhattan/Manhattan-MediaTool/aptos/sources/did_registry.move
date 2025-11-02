module manhattan_registry::manhattan_notary {
    use std::signer;
    use std::string::String;
    use aptos_std::table::{Self, Table};Ye

    /// Error codes
    const E_NOT_AUTHORIZED: u64 = 1;
    const E_PROOF_NOT_FOUND: u64 = 2;
    const E_REGISTRY_NOT_FOUND: u64 = 3;

    /// Resource struct to store immutable sanitization proofs
    /// Maps device serial numbers to sha256 hashes of their Verifiable Credentials
    struct ProofRegistry has key {
        proofs: Table<String, vector<u8>>
    }

    /// Initialize the module - creates an empty ProofRegistry for the publisher
    /// This runs automatically when the module is published
    fun init_module(publisher: &signer) {
        let registry = ProofRegistry {
            proofs: table::new()
        };
        move_to(publisher, registry);
    }

    /// Register a sanitization proof on-chain
    /// Only the owner of the ProofRegistry (module publisher) can call this function
    /// This creates an immutable, auditable record of the drive wipe
    public entry fun register_proof(
        owner: &signer,
        serial_number: String,
        vc_hash: vector<u8>
    ) acquires ProofRegistry {
        let owner_addr = signer::address_of(owner);
        
        // Security check: only the registry owner can register proofs
        assert!(exists<ProofRegistry>(owner_addr), E_REGISTRY_NOT_FOUND);
        
        let registry = borrow_global_mut<ProofRegistry>(owner_addr);
        
        // Add or update the proof in the table
        // Note: Updating allows for re-certification if needed
        if (table::contains(&registry.proofs, serial_number)) {
            *table::borrow_mut(&mut registry.proofs, serial_number) = vc_hash;
        } else {
            table::add(&mut registry.proofs, serial_number, vc_hash);
        }
    }

    /// Retrieve a sanitization proof for a given device serial number
    /// This is a public view function - anyone can verify proofs
    /// Returns the sha256 hash of the Verifiable Credential
    #[view]
    public fun get_proof(
        registry_owner: address,
        serial_number: String
    ): vector<u8> acquires ProofRegistry {
        // Ensure the registry exists
        assert!(exists<ProofRegistry>(registry_owner), E_REGISTRY_NOT_FOUND);
        
        let registry = borrow_global<ProofRegistry>(registry_owner);
        
        // Ensure the proof exists
        assert!(table::contains(&registry.proofs, serial_number), E_PROOF_NOT_FOUND);
        
        // Return the VC hash - this is the immutable proof
        *table::borrow(&registry.proofs, serial_number)
    }
}
