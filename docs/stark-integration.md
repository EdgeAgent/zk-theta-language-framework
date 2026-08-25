# STARK-style IOP/FRI integration in the ZK Theta compiler/runtime

## Status and scope

This is the proposed integration design for ZK Theta. The current repository contains a workflow reference runner with SHA-256-linked audit receipts, but it does not yet contain an AIR compiler, STARK prover, FRI implementation, or zero-knowledge verifier. The pipeline below describes how those components would fit together.

## 1. Compile `.theta` into a typed agent IR

The compiler first resolves agent declarations, pipeline edges, tool schemas, policy clauses, approval requirements, and observation fields. It lowers the source into a typed intermediate representation with explicit events such as `AgentStart`, `ToolCall`, `ToolResult`, `Assert`, `ApprovalRequested`, `ApprovalGranted`, `StateCommit`, and `AgentHandoff`.

Each event has a canonical encoding. Public fields include the workflow ID, transition ID, policy digest, public inputs, and selected public outputs. Private fields can include prompts, hidden memory, private tool arguments, and intermediate model outputs.

## 2. Lower the typed IR into an algebraic transition system

A future `theta prove` backend would map the event machine to an AIR-like representation. The trace is a table whose rows are execution cycles and whose columns hold finite-field encodings of the current state, agent identifier, event tag, tool-result digest, policy status, approval status, and memory commitments.

The compiler emits low-degree transition constraints that express rules such as: the next state must follow the previous state; a tool result must match its committed digest; an assertion can advance only when its predicate is true; a guarded action can advance only after an approval; and a handoff must consume the output schema of the sending agent and satisfy the input schema of the receiving agent.

Boundary constraints bind the first and final rows to the public statement. For example, the first row binds the request digest and policy digest, while the final row binds the claimed outcome and final state commitment.

## 3. Build the private execution trace

The runtime executes the agent workflow and records a witness trace. The model may propose a plan, but deterministic runtime components write the trace: policy evaluation, schema validation, approval state, tool receipts, evidence digests, and state transitions. This is where probabilistic model behavior is converted into a checkable execution record.

Private witness data stays in the prover’s trace. Only commitments and explicitly declared public outputs are exposed to the verifier.

## 4. Interpolate and compose constraints

The prover interpolates trace columns over a finite-field evaluation domain and evaluates the transition and boundary constraints across that domain. A composition polynomial combines the constraint values using random-looking but transcript-bound coefficients. Correct traces make the relevant constraint expressions vanish on the trace domain, so the composition polynomial has the required divisibility and degree properties.

In a concrete implementation, the exact domain, field, constraint degree, blowup factor, composition construction, and soundness parameters must be specified. They are intentionally not fixed in the current proposal.

## 5. Commit to evaluations

The prover evaluates the trace and composition polynomials on an expanded domain and commits to each evaluation vector with Merkle trees. The verifier receives the roots, not the full private trace. Merkle authentication paths later let the verifier check selected values without downloading the entire vector.

## 6. Use Fiat–Shamir to derive challenges

The runtime transcript absorbs the public statement, canonical source/IR digest, policy digest, commitment roots, and prior prover messages into a domain-separated hash/XOF. Fiat–Shamir derives the challenge coefficients and query positions. Canonical serialization is essential: different encodings must never produce different challenge transcripts for the same logical statement.

## 7. Run FRI low-degree testing

FRI recursively tests whether the committed evaluation vector is close to a low-degree polynomial. In each commit round, the prover folds the current codeword using a verifier challenge and commits to the smaller folded vector. In query rounds, the verifier selects positions, checks Merkle paths, and checks the algebraic folding relation across the queried values. The final small-degree layer is checked directly.

FRI does not by itself prove the agent logic. It proves the low-degree property of the polynomials produced by the AIR/constraint system. The connection to agent correctness comes from the composition polynomial and the verifier’s checks that composition values are consistent with the trace and constraints.

## 8. Verify and return a proof receipt

The verifier checks: public-input binding; Merkle paths; boundary constraints; transition/composition consistency; FRI folding and final-layer checks; proof parameter identifiers; and any signatures on tool manifests or approvals. A successful result is a proof receipt containing the statement digest, proof-system version, policy digest, commitment roots, query transcript, verification result, and optional public outputs.

## 9. What zero knowledge requires

A STARK-style IOP/FRI pipeline is not automatically zero knowledge. The implementation must add witness masking or blinding, ensure that openings do not leak private trace values, bind all public data into the transcript, and prove that the masking preserves soundness. The system also needs a formal security definition, parameter selection, constant-time and side-channel review where applicable, and independent cryptographic audits.

Therefore, in the present repository the correct claim is “proposed STARK-style integration,” not “implemented zero-knowledge verification.”

## References

[1] [Anatomy of a STARK, Part 3: FRI](https://aszepieniec.github.io/stark-anatomy/fri.html).

[2] [Anatomy of a STARK, Part 4: The STARK IOP](https://aszepieniec.github.io/stark-anatomy/stark.html).

[3] [RISC Zero, About the FRI Protocol](https://dev.risczero.com/reference-docs/about-fri).

[4] [ethSTARK Documentation, Version 1.2](https://eprint.iacr.org/2021/582.pdf).
