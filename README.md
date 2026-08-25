# ZK Theta Language — Developer AI Agent Framework

[![Status](https://img.shields.io/badge/status-proposed%20spec-ff7a00)](docs/zk-theta-framework.pdf)
[![Focus](https://img.shields.io/badge/focus-agent--native-9d72ff)](docs/framework.md)
[![Security](https://img.shields.io/badge/security-policy--first-35d0ba)](docs/framework.md)
[![Observability](https://img.shields.io/badge/observability-by%20design-f5c451)](docs/framework.md)

ZK Theta is a proposed language and runtime framework for building trustworthy, observable AI agents. It gives developers explicit constructs for intent, constraints, typed tools, policy gates, evidence-bound memory, evaluation, and deployment telemetry.

> This repository contains a design proposal and reference materials. ZK Theta is not presented as an existing public standard, and the metrics in the accompanying PDF are illustrative design targets rather than measured production results.

## Contents

The main deliverable is [`docs/zk-theta-framework.pdf`](docs/zk-theta-framework.pdf). The editable narrative is in [`docs/framework.md`](docs/framework.md). Architecture and runtime lifecycle diagrams are maintained as Mermaid sources under [`diagrams/`](diagrams/), with rendered PNG assets under [`assets/`](assets/).

## Design pillars

| Pillar | Purpose |
| --- | --- |
| Intent-first syntax | Make goals, constraints, and success criteria explicit. |
| Typed tool contracts | Make external actions schema-driven, bounded, and auditable. |
| Policy-native execution | Enforce permissions, approvals, privacy, and budget rules at runtime. |
| Evidence-bound memory | Keep observations, inferences, and durable facts separated. |
| Evaluation loops | Regression-test plans, tools, grounding, cost, and latency. |
| Deployment observability | Emit traces, lineage, receipts, and audit events by default. |

## Status

The current repository is a concept specification and visual reference package. A future implementation should begin with a small runtime slice: compile one agent definition, execute mocked typed tools, enforce one approval gate, and emit a replayable trace.

## License

The proposal and source materials are released under the MIT License. See [`LICENSE`](LICENSE).
