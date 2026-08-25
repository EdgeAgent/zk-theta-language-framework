# Cryptography research notes

ZK Theta is currently a proposal and does not yet implement zero-knowledge proofs or claim a cryptographic guarantee. The updated specification therefore distinguishes a proposed proof suite from the runnable reference workflow.

## Sources and findings

1. NIST’s finalized post-quantum standards include FIPS 203 ML-KEM for key encapsulation, FIPS 204 ML-DSA for digital signatures, and FIPS 205 SLH-DSA for hash-based digital signatures. Source: https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
2. The IRTF Fiat–Shamir Internet-Draft describes making a public-coin protocol non-interactive with a cryptographic hash function and emphasizes transcript encoding, serialization, soundness, zero knowledge, and quantum-adversary considerations. It is an active Internet-Draft and not an endorsed final standard. Source: https://datatracker.ietf.org/doc/draft-irtf-cfrg-fiat-shamir/
3. OpenTelemetry describes itself as a vendor-neutral observability framework for generating, collecting, and exporting traces, metrics, and logs. Source: https://opentelemetry.io/docs/

## Proposed ZK Theta proof suite

The proposal uses a modular suite rather than claiming that one primitive alone guarantees zero knowledge:

- SHA-256 or SHAKE256 for domain-separated hashes, transcript binding, event commitments, and Merkle-tree hashing.
- A transparent polynomial IOP / STARK-style proof system as the default proof family for state-transition validity, avoiding a trusted setup. A concrete implementation would need to select a specific protocol and field.
- Fiat–Shamir with explicit domain separation and canonical serialization to convert interactive challenge rounds into a non-interactive proof transcript.
- Merkle commitments for ordered event logs and state snapshots, allowing inclusion proofs for selected transition inputs and outputs.
- A signature layer for agent/tool identity and approval receipts. ML-DSA is the proposed post-quantum option; Ed25519 may be used for a non-PQ prototype, but the suite must state that this is not post-quantum.
- ML-KEM for protecting encrypted transport or sealed evidence channels when post-quantum key establishment is required. It is not itself a zero-knowledge proof primitive.

## Important security qualification

No named primitive by itself guarantees that an agent state transition is valid or private. The guarantee depends on a formally specified relation, a sound and zero-knowledge proof system, secure transcript binding, correct witness handling, sound serialization, key management, implementation correctness, and independent cryptographic review. The reference runner shipped with this update demonstrates workflow execution and hash-linked audit records only; it does not implement a ZK proof system.
