# STARK-style IOP/FRI research notes

1. The Anatomy of a STARK tutorial describes AIR as an arithmetic intermediate representation of an execution trace, where rows represent states and low-degree polynomial constraints enforce state transitions and boundary conditions. Source: https://aszepieniec.github.io/stark-anatomy/stark.html
2. The same tutorial describes FRI as a protocol proving that a committed codeword is close to evaluations of a low-degree polynomial. Real deployments use Merkle trees to commit to codeword evaluations and answer selective queries. Source: https://aszepieniec.github.io/stark-anatomy/fri.html
3. RISC Zero describes FRI as recursive low-degree testing with commit rounds and query rounds; Fiat–Shamir selects query locations non-interactively. Source: https://dev.risczero.com/reference-docs/about-fri
4. ethSTARK documentation organizes a concrete STARK pipeline around execution traces, constraints, trace low-degree extension, commitments, composition polynomials, DEEP consistency checks, FRI commit/query phases, and Fiat–Shamir transformation. Source: https://eprint.iacr.org/2021/582.pdf

## Proposed compiler/runtime mapping

Theta source compiles into a typed agent IR, then a deterministic policy/evidence IR, then an AIR-like transition specification. Each agent handoff, tool result, assertion, approval, and state update becomes a trace row or trace-column value. The prover builds the private trace; the verifier receives commitments and public inputs. A future runtime would produce composition polynomials for transition and boundary constraints, commit to their evaluations with Merkle roots, use Fiat–Shamir to derive challenges, and use FRI queries to test low-degree proximity. Zero knowledge requires masking/blinding and a proof construction that formally provides it; the current repository does not implement these pieces.
