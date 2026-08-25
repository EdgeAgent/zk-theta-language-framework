#!/usr/bin/env python3
"""Runnable reference for examples/multi_agent_workflow.theta.

This is an executable workflow simulator, not a Theta compiler and not a ZK
proof implementation. It demonstrates agent handoffs, policy gating, evidence
collection, and hash-linked audit records using only the Python standard
library.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ReleaseRequest:
    service: str
    repository: str
    commit: str
    environment: str


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def event(agent: str, action: str, payload: object, previous: str) -> tuple[dict, str]:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "action": action,
        "payload": payload,
        "previous_event": previous,
    }
    record["event_hash"] = digest(record)
    return record, record["event_hash"]


def main() -> None:
    request = ReleaseRequest(
        service="checkout-api",
        repository="edge/checkout-api",
        commit="a1b2c3d4",
        environment="staging",
    )
    events: list[dict] = []
    previous = "GENESIS"

    record, previous = event("Planner", "plan.created", {
        "checks": ["ci", "security", "change-window"],
        "evidence_required": 3,
        "request": asdict(request),
    }, previous)
    events.append(record)

    evidence = {
        "ci": {"status": "green", "commit": request.commit},
        "security": {"status": "pass", "commit": request.commit},
        "change_window": {"open": True, "service": request.service},
    }
    assert evidence["ci"]["status"] == "green"
    assert evidence["security"]["status"] == "pass"
    assert evidence["change_window"]["open"] is True
    record, previous = event("Researcher", "evidence.collected", evidence, previous)
    events.append(record)

    evidence_digest = digest(evidence)
    verification = {"decision": "eligible", "evidence_digest": evidence_digest}
    record, previous = event("Verifier", "verification.completed", verification, previous)
    events.append(record)

    # Reference runner uses an explicit local approval. A production runtime
    # should obtain this from a policy service or human approval channel.
    approval = {"approver": "release-manager", "approved": True}
    assert verification["decision"] == "eligible"
    assert approval["approved"] is True
    promotion = {"service": request.service, "commit": request.commit, "environment": request.environment, "status": "promoted"}
    record, previous = event("Promoter", "promotion.completed", {"approval": approval, "promotion": promotion}, previous)
    events.append(record)

    receipt = {
        "workflow": "SafeRelease",
        "status": "success",
        "event_count": len(events),
        "final_event_hash": previous,
        "evidence_digest": evidence_digest,
        "events": events,
    }
    output = Path(__file__).with_name("run_receipt.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ("workflow", "status", "event_count", "final_event_hash", "evidence_digest")}, indent=2))
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
