# ZK Theta cryptography and state-transition verification

## Current status

ZK Theta is a proposal. The repository does **not** currently implement a zero-knowledge proving system, a verifier circuit, a trusted setup, or a post-quantum signature stack. The Python reference runner demonstrates agent handoffs, policy checks, evidence hashing, and an append-only hash chain; it does not provide a zero-knowledge guarantee.

## Proposed proof model

A ZK Theta state transition would be represented as a relation:

```text
R(previous_state_commitment,
  public_policy_digest,
  public_transition_id,
  next_state_commitment,
  witness) = true
```

The witness can include private prompts, private tool inputs, hidden memory entries, and intermediate model/tool data. The public statement can expose only the transition identifier, policy digest, previous commitment, next commitment, and selected public outputs.

A verifier would accept a proof only if it establishes that a valid witness exists for the relation and that the transition satisfies the compiled policy and tool-result constraints. Privacy is achieved only when the circuit/relation omits private values from the public statement and the proof system is actually zero knowledge.

## Proposed primitive suite

| Component | Proposed primitive | Role | Important limitation |
| --- | --- | --- | --- |
| Domain-separated hashing | SHA-256 or SHAKE256 | Hash state snapshots, transcripts, policy digests, and event payloads. | A hash commitment is not a zero-knowledge proof. |
| State/event commitment | Merkle tree using SHA-256 or SHAKE256 | Commit to ordered evidence and state logs; prove inclusion of selected records. | Merkle inclusion proves membership, not validity of the whole transition. |
| Proof system | Transparent STARK-style polynomial IOP/FRI construction | Prove that the transition circuit satisfies its constraints without a trusted setup. | A concrete protocol, field, soundness error, and implementation are still unspecified. |
| Non-interactive transcript | Fiat–Shamir over a canonical transcript | Derive verifier challenges from commitments and public inputs. | Security depends on correct encoding, domain separation, and the proof model; the IRTF document cited below is an Internet-Draft, not a final standard. |
| Agent/tool identity | ML-DSA for the post-quantum profile; Ed25519 only for a non-PQ prototype | Authenticate tool manifests, approval receipts, and deployment identities. | Signatures provide authenticity, not zero knowledge. |
| Confidential transport | ML-KEM for the post-quantum profile | Establish keys for encrypted evidence or telemetry channels. | Key establishment provides confidentiality in transit, not proof of correct state transition. |

## What can and cannot be claimed

The specific answer to “which primitives guarantee zero-knowledge proof verification?” is: **none are currently implemented in ZK Theta, and no primitive alone guarantees it**. A future implementation would need a formally specified proof system with a zero-knowledge property, a sound transition relation, canonical serialization, secure Fiat–Shamir transcript binding, correct witness isolation, and independent cryptographic review.

The proposed default is a transparent STARK-style proof system because it can avoid a trusted setup. A production team could instead select a SNARK system such as PLONK-family proving with a polynomial commitment scheme, but that would require a separate decision about trusted setup, curve security, commitment assumptions, recursion, proof size, and post-quantum posture. The framework deliberately does not pretend those choices have already been made.

## Verification flow

1. Compile the agent workflow into a transition relation and policy digest.
2. Serialize public inputs and private witness data canonically.
3. Commit to the relevant private state and ordered event log.
4. Produce a non-interactive proof using a specified proof system and Fiat–Shamir transcript.
5. Sign the proof receipt and tool/approval metadata with the configured identity key.
6. Verify the proof, commitments, signatures, policy digest, and chain linkage.
7. Emit a trace and replay record without exposing private witness contents.

## References

1. [NIST, “NIST Releases First 3 Finalized Post-Quantum Encryption Standards”](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) — FIPS 203 ML-KEM, FIPS 204 ML-DSA, and FIPS 205 SLH-DSA overview.
2. [IRTF, “Fiat–Shamir Transformation,” draft-irtf-cfrg-fiat-shamir-03](https://datatracker.ietf.org/doc/draft-irtf-cfrg-fiat-shamir/) — transcript construction, serialization, and security considerations; active Internet-Draft.
3. [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — vendor-neutral traces, metrics, and logs used by the observability model.
