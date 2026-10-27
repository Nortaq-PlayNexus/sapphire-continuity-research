# AUDIT REPORT — Sapphire Continuity Research Program

**Date:** 2026-10-27  
**Auditor:** OpenCode (autonomous)  
**Scope:** Existing research artifacts for AI memory, episodic continuity, persistent state, runtime recovery  
**Status:** Phase 1 Complete

## 1. Executive Summary

This audit examined three primary repositories containing continuity/memory research:
- `C:\Users\natha\projects\ce-1-continuous-existence` (clean, branch master, commit fd14fac)
- `C:\Users\natha\projects\episodic-memory` (clean, branch master, commit ddf1f1d)  
- `C:\Users\natha\ScientificDiscoveryLab` (dirty, branch master, commit 022fb28)

**Key findings:**
- **CE-1/H8 is the most mature experimental work.** Strong adversarial verification has been performed. H8 (content-specific episodic continuity) is **SUPPORTED** and **REPLICATED** on a second model (dolphin-llama3). The effect is real but narrower than claimed.
- **Episodic-memory is the persistent experience store.** Recently fixed critical bugs (sentence-transformers hang, ChromaDB telemetry blocking). Has retrieval quality measurements. Not yet integrated into CE-1 continuity experiments as the retrieval substrate.
- **ScientificDiscoveryLab** contains broader research but less directly focused on the continuity mechanisms specified in the prompt.

## 2. Repository Audits

### 2.1 CE-1 Continuous Existence (`projects/ce-1-continuous-existence`)

**Purpose:** Rigorous scientific investigation of AI continuity/consciousness questions  
**Status:** Active, well-documented, adversarially verified  
**Git:** Clean, own repo, no remote

**Strengths:**
- Excellent adversarial verification practices (Experiments 1.1-1.3 had instrument defects found)
- H8 fully preregistered, analyzed with proper statistics (permutation test, bootstrap CI), replicated on second model
- Comprehensive documentation (preregistrations, adversarial reports, limitations)
- Proper separation of pilot vs confirmatory, exploratory vs confirmatory
- Evidence grading system in place
- Tests exist (pytest)

**Key Results (H8):**
- **gemma3:4b (confirmatory):** primary diff = 0.819 (as-run) / 1.833 (corrected), p < 1e-4, CI [0.667, 0.972]
- **dolphin-llama3 (replication):** primary diff = 1.875, p < 1e-4, CI [1.722, 2.028] - **REPLICATED**
- Effect is rubric-independent (content discrimination +0.152 correct vs -0.215 decoy)
- 216 trials, 0 truncations, 0 invalid

**Critical Issues Found & Fixed (per adversarial report):**
- D1: No committed live runner - **FIXED** (now committed)
- D2: Preregistered statistics never performed - **FIXED**
- D3: 2 of 5 rubric components unreachable (decision, rationale_codes) - **DOCUMENTED**
- D4: Scoring defects (raw ID comparison, point 5 subset of point 4) - **FIXED with corrected scorer**
- D5: Invalid trials scored as zero - **FIXED**
- D6: False claim about fuzzy matching - **CORRECTED**
- D7: H1-H7 hypothesis register deleted - **RESTORED**
- D9-D10: Design issues documented (no_memory not memory-free, decoy contradicts)

**What H8 Actually Demonstrates:**
> "Correctly retrieved episodic content changes what the model says, and it changes it in the direction of the retrieved episode" - this is content-specific sensitivity under prompt delivery. NOT proof of "continuous existence" or interruption/resumption.

**Untested:** H3 (interruption/resumption) remains untested. H1-H2 INCONCLUSIVE, H3-H6 UNTESTED, H7 OUT OF REACH.

### 2.2 Episodic Memory (`projects/episodic-memory`)

**Purpose:** Persistent episodic memory store for AI agents (experiences not facts)  
**Status:** Recently stabilized, own git repo since 2026-10-21  
**Git:** Clean, branch master, commit ddf1f1d

**Architecture:**
- ChromaDB (persistent, cosine) + ONNXMiniLM_L6_V2 embeddings (384-dim)
- Append-only JSONL log
- MCP server interface
- `remember()`, `recall()`, `relive()`, `get_timeline()`, `stats()`

**Critical Fixes Applied:**
- Swapped from sentence-transformers to ONNXMiniLM_L6_V2 (sentence-transformers hung indefinitely)
- Disabled ChromaDB anonymized telemetry (blocked on network call for >25min)
- Both fixes are load-bearing and documented

**Retrieval Quality (measured):**
- 60 scenarios / 270 episodes, seed 20261021
- Top-3 accuracy 0.98-1.00, MRR 0.75-0.93, chance 0.0037 (p = 1.2e-56)
- Embedding separates by wording well, poorly by numbers alone (margin ~0.004/-0.005)
- Near-duplicate decoys harder to distinguish

**Known Issues:**
- `recall()` re-reads entire JSONL every call (O(n))
- `remember()` writes to ChromaDB before JSONL (failure leaves orphan in vector store)
- No validation of enum fields in Episode dataclass
- `relive()` truncates related episodes unconditionally

**Outstanding:**
- Not yet used as retrieval substrate in CE-1 continuity experiments (H8 uses synthetic episode blocks in prompt)
- Value-level retrieval needs attention
- Need to design v2 benchmark where query carries distinguishing info

### 2.3 ScientificDiscoveryLab

**Purpose:** Broad research lab  
**Status:** Dirty working tree, large codebase  
**Git:** Clean commit but uncommitted changes

Less directly relevant to the specific continuity mechanisms in the prompt. Contains various experiments and tools.

## 3. Zenodo Records (as specified)

The prompt lists:
- Episodic Memory for AI Agents: A Persistent Experience Store (https://zenodo.org/records/23489660)
- CE-1 Confirmatory Result: Content-Specific Episodic Continuity (H8) (https://zenodo.org/records/23489491)  
- Associated software record (https://zenodo.org/records/23471293)

These need to be retrieved if possible. I'll attempt to fetch them.
