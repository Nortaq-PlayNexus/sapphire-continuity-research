# Sapphire Continuity Research Program

**Independent AI Memory, Episodic Continuity, Persistent State, Runtime Recovery and Scientific Evidence Audit**

## Purpose

This research program investigates different mechanisms that may produce continuity in an AI system across interactions, sessions, process restarts, and changes of execution environment. It distinguishes between context continuity, transcript replay, external episodic memory, persistent conversation state, persistent agent state, application-level state reconstruction, inference-runtime recovery, cross-process computational continuity, cross-environment portability, parametric persistence, behavioral continuity, and identity/consciousness claims.

The central question: **Which kinds of continuity can be demonstrated experimentally, which mechanisms explain the observations, and what additional evidence would be needed to establish stronger claims?**

## Status

- **Phase 1 (Discovery & Audit):** COMPLETE
- **Phase 2 (Research Gap Analysis):** COMPLETE
- **Phase 3 (Experimental Design - CE-2):** COMPLETE (proposed, not frozen)
- **Phase 4 (Core Implementation):** COMPLETE
- **Phase 5 (Exploratory Validation):** IN PROGRESS (red-team findings being addressed)
- **Phase 6 (Freeze Protocol):** CANDIDATE created (not frozen)
- **Phase 7 (Confirmatory Experiments):** Pending (blocked on protocol freeze + LLM availability)
- **Phase 8 (Independent Analysis & Red Team):** IN PROGRESS
- **Phase 9 (Final Package):** IN PROGRESS

## Project Location

`C:\Users\natha\projects\sapphire-continuity-research`

## Related Repositories

- `C:\Users\natha\projects\ce-1-continuous-existence` - Primary research program (H1-H8), adversarially verified
- `C:\Users\natha\projects\episodic-memory` - Persistent experience store (ChromaDB + ONNX embeddings)
- `C:\Users\natha\ScientificDiscoveryLab` - Broader research

## Key Findings So Far

### Verified
- **H8 (content-specific episodic continuity):** SUPPORTED and REPLICATED on second model (dolphin-llama3). Correctly retrieved episodic content changes model output. gemma3:4b: diff=0.819 (p<1e-4), dolphin-llama3: diff=1.875 (p<1e-4).
- **Episodic memory store:** Functional, retrieval quality measured (top-3 acc 0.98-1.00). Critical bugs fixed.

### Not Demonstrated
- **Interruption/resumption (H3):** UNTESTED - process restart continuity
- **Runtime state recovery (KV cache):** UNTESTED
- **Real episodic store as retrieval substrate:** H8 used synthetic prompt injection, not the actual ChromaDB store
- **Consciousness/identity claims:** Not supported by evidence, properly separated

## Running

This is primarily a research/audit project. Tests and experiments will be added as development progresses.

```powershell
cd C:\Users\natha\projects\sapphire-continuity-research
# Tests will be run with pytest when available
```

## Principles

- Rigorous, reproducible, independently auditable
- Distinguish mechanisms, don't collapse into single score
- Adversarial testing - attempt to falsify
- Honest reporting of limitations
- Published artifacts remain immutable
- No consciousness claims without proper framework and evidence
- Local-first, no API calls without approval

## Documentation

- `AUDIT_REPORT.md` - Phase 1 findings
- `RESEARCH_GAP_ANALYSIS.md` - Phase 2 analysis
- `PREREGISTRATION_CE2.md` - Proposed CE-2 protocol (not frozen)
- `PREREGISTRATION_CE2_FROZEN.md` - Protocol candidate with hash (NOT frozen)
- `METHODS.md` - Experiment methods
- `DATA_DICTIONARY.md` - Scenario/result/metric schemas
- `EVIDENCE_LEDGER.md` - Claim-to-artifact mapping
- `RED_TEAM_REPORT.md` - Adversarial findings
- `REPRODUCIBILITY.md` - Setup, run, and verification commands
- `CHANGELOG.md` - Modification history
- `LIMITATIONS.md` - Known limitations
- `AUDIT_BASELINE.json` - Repository baseline
