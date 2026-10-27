# PREREGISTRATION — CE-2: Mechanism-Specific Persistence and Cross-Session Continuity

**Status:** PROPOSED (not yet frozen)  
**Date:** 2026-10-27  
**Authors:** CE-1 Research Programme  
**Version:** 0.1.0-draft

> This is a NEW experiment. It does not alter CE-1/H1-H8 historical data or retroactively treat CE-2 decisions as preregistered CE-1 decisions.

## 1. Research Questions

1. **RQ1:** When using the actual episodic-memory store (ChromaDB + ONNX embeddings) as retrieval substrate, does content-specific retrieval improve performance compared to synthetic prompt injection?
2. **RQ2:** Can we demonstrate interruption/resumption (H3) - continuity across process restart - and what mechanism enables it?
3. **RQ3:** Which of the 12 continuity mechanisms can be cleanly distinguished by ablation, and which are confounded?
4. **RQ4:** Does the episodic store introduce leakage, contamination, or false recall not present in simple prompt replay?
5. **RQ5:** Can local inference runtime state (KV cache) be serialized and restored to resume generation?

## 2. Primary Hypotheses

**H3 (primary, previously untested):** *Interruption/resumption* - After process termination and restart, a system using application-level state reconstruction (Condition F) can correctly use previously established facts, performing better than fresh session baseline but the mechanism differs from transcript replay.

**H3a:** External episodic memory (real store) provides measurable benefit over transcript replay when tested with proper controls.
**H3b:** Application-level state reconstruction (saving/loading app state) can restore continuity across process restart.
**H3c:** The benefit of external memory persists after transcript is removed, but transcript replay benefit disappears only if transcript is truly removed.

## 3. Operational Definitions

| Mechanism | Operational Definition | Measurement |
|-----------|------------------------|-------------|
| **Transcript replay** | Full conversation history provided in prompt | Model sees all prior messages |
| **External episodic memory** | Facts stored in episodic-memory ChromaDB, retrieved via `recall()` | Retrieved episodes injected into prompt; transcript/history may or may not be present |
| **Application-level state reconstruction** | App saves state to disk (JSON/DB), reloads on restart | New process reads saved state and reconstructs context |
| **Inference-runtime recovery** | KV cache or execution state saved/restored | Requires engine support; measure bitwise or behavioral equivalence |
| **Cross-process continuity** | Terminate process, start new process, test | Must use different PID/process instance |

## 4. Experimental Conditions

| Condition | Name | Description | Tests |
|-----------|------|-------------|-------|
| **C0** | Fresh baseline | No history, no memory | Guessing/prior knowledge |
| **C1** | Transcript replay | Full transcript in prompt | Context continuity |
| **C2** | Episodic store (real) | Store facts in episodic-memory, retrieve via real `recall()` | External episodic memory (real) |
| **C3** | Episodic store + transcript | Both mechanisms | Confounding |
| **C4** | App state save/restart | Save app state, kill process, restart, load state | Application-level reconstruction |
| **C5** | Episodic store only (no transcript) | Memory but no history | Isolation of mechanism |
| **C6** | Transcript only (no memory) | History but nothing in memory store | Isolation of mechanism |
| **C7** | Empty store + fresh start (restart) | True fresh start after restart | Restart control |
| **C8** | Local KV cache recovery (if supported) | Save/restore inference state | Runtime recovery (experimental) |

## 5. Primary Outcome Measures

Same as H8 for comparability:
- **Primary:** mean(score_correct_retrieval - score_matched_decoy) paired by scenario
- **Rubric:** Use CE-1's 0-5 rubric but also report rubric-independent metrics
- **Rubric-independent:** token discrimination, episode citation accuracy, target/decoy preference

Additional CE-2 measures:
- **Mechanism attribution:** delta when removing each component
- **Leakage rate:** false recall of facts not in any allowed source
- **Contamination rate:** cross-session/cross-scenario leakage
- **Recovery success:** % of state correctly restored after restart
- **Ablation clarity:** can we attribute effect to single mechanism?

## 6. Controls & Red Team

- **Matched decoys** (same as H8)
- **Unrelated semantically similar memories** in store
- **Contradictory memories**
- **Wrong session ID**
- **Stale memories**
- **Empty store**
- **Process restart controls**
- **Evaluator blind to condition where possible**
- **Separate roles** (generator, SUT, adapter, evaluator)
- **Leakage detection** on all retrieved items
- **Corrupted state files**

## 7. Statistical Plan

- Paired comparisons by scenario
- Permutation tests (seeded)
- Bootstrap CIs
- Account for repeated measures
- Correct for multiple comparisons
- Report effect sizes
- If underpowered, say so

## 8. Sample Size

Start with **exploratory** (smaller n), freeze protocol before confirmatory. Target similar scale to H8 (72 scenarios) if feasible.

## 9. Falsification Criteria

- **H3 falsified:** No difference between fresh start and app-state-restored start, or difference is explained by transcript leakage
- **H3a falsified:** Real episodic store performs no better than matched decoys / no better than empty
- **Mechanism conflation:** Cannot distinguish mechanisms despite ablations (confounded) - report as INCONCLUSIVE

## 10. Limitations Acknowledged

- Local models only (Ollama) - may not generalize
- KV cache recovery may not be possible with available engines
- Process restart testing is complex on Windows
- Some mechanisms may be confounded in practice
- Consciousness claims remain out of scope

## 11. Protocol Freezing

**NOT FROZEN.** This is a proposal. Will freeze only after:
1. Test harness passes validation
2. Exploratory runs complete
3. Protocol reviewed and hash recorded
4. Explicit approval if external APIs needed

---

*This preregistration follows CE-1's principles of rigor, adversarial testing, and honest reporting.*
