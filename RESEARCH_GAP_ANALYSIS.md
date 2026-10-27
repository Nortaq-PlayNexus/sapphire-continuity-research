# RESEARCH GAP ANALYSIS — Sapphire Continuity Research Program

**Date:** 2026-10-27  
**Status:** Phase 2 Complete

## 1. What IS Demonstrated

| Finding | Evidence Grade | Notes |
|---------|---------------|-------|
| **Content-specific episodic sensitivity (H8)** | REPRODUCED + INDEPENDENTLY REPLICATED | gemma3:4b: diff=0.819 (p<1e-4), dolphin-llama3: diff=1.875 (p<1e-4). Correctly retrieved episodes change model output in direction of retrieved content. Rubric-independent discrimination confirmed. |
| **Episodic memory store works** | VERIFIED | Episodic-memory project: stores experiences, semantic retrieval works. Retrieval quality measured (top-3 acc 0.98-1.00). Critical bugs fixed (sentence-transformers hang, ChromaDB telemetry). |
| **Adversarial verification discipline** | VERIFIED | CE-1 has excellent track record of finding and fixing instrument defects. Multiple experiments had defects caught by adversarial review. |
| **Preregistered methodology** | VERIFIED | Proper preregistration, frozen protocols, separation of exploratory/confirmatory, statistical rigor. |

## 2. What IS Only Asserted (Not Demonstrated)

| Claim | Status | Gap |
|-------|--------|-----|
| **"Continuous existence"** | NOT TESTED / OVERSTATED | H8 measures prompt-based content delivery, not interruption/resumption. The name "H8" and some framing overreach. CE-1 docs correctly caution against this, but it's easy to conflate. |
| **Interruption/resumption (H3)** | UNTESTED | No experiments test process restart, session recovery, or computational state restoration. This is explicitly called out as untested. |
| **Persistent conversation state benefits** | NOT TESTED | Condition D in the prompt (OpenAI Conversations API) not tested. |
| **Agent session recovery** | NOT TESTED | Condition E not tested. |
| **Local runtime state recovery** | NOT TESTED | Condition F (KV cache, inference state) not tested. This requires local open-weight models with engines that support state serialization. |
| **Cross-process/cross-environment portability** | NOT TESTED | No tests of this. |
| **Parametric persistence** | NOT TESTED | Can't be inferred from recall alone per prompt - correct stance. |
| **Episodic store used as retrieval substrate in continuity tests** | NOT TESTED | H8 uses synthetic episode blocks injected into prompts, not the actual episodic-memory ChromaDB store. |

## 3. What is NOT Testable with Current Architecture

| Capability | Blocker | Notes |
|------------|---------|-------|
| **OpenAI hidden runtime state extraction** | Correctly identified as impossible via documented APIs | Support Case 18384370 analysis matches - no documented API for this. Must not attempt. |
| **True computational state serialization (KV cache)** | Engine support unknown/limited | Ollama may not expose KV cache serialization in a portable form. Need to investigate vLLM, llama.cpp, koboldcpp capabilities. Hardware limited (GTX 1080 8GB). |
| **Cross-environment state transfer** | Requires engine support + format compatibility | Very few engines support this. |
| **Consciousness claims** | Philosophical, not empirically testable with current tools | Correctly separated in CE-1 principles. |

## 4. Mechanism Mapping (per prompt requirements)

| Mechanism | Current Status | Testable? | Priority |
|-----------|---------------|-----------|----------|
| 1. Context continuity | Tested (implicit in all conditions) | Yes | Done |
| 2. Transcript replay | Partially tested | Yes | Medium |
| 3. External episodic memory | Store exists but not tested as substrate | Yes | **HIGH** |
| 4. Persistent conversation state (Conversations API) | Not tested | Yes (if API available) | Medium |
| 5. Persistent agent state (sessions) | Not tested | Yes | Medium |
| 6. Application-level state reconstruction | Not tested | Yes | Medium |
| 7. Inference-runtime recovery | Not tested | Yes (locally) | **HIGH** |
| 8. Cross-process computational continuity | Not tested | Yes (locally) | **HIGH** |
| 9. Cross-environment portability | Not tested | Unlikely with open tools | Low |
| 10. Parametric persistence | Not testable by recall alone | No direct test | Low (separate track) |
| 11. Behavioral continuity | Demonstrated (H8) | Yes | Done |
| 12. Identity/consciousness claims | Philosophical | No | Separate track only |

## 5. Critical Gaps to Address in CE-2

1. **Use the actual episodic-memory store as retrieval substrate** - H8 proved content matters, but used synthetic injection. Need to test with real ChromaDB store, real retrieval, test for leakage, contamination, etc.

2. **Test interruption/resumption (H3)** - This is the key untested hypothesis. Need to define what "resumption" means operationally and test it.

3. **Investigate local runtime state recovery** - Check what Ollama/llama.cpp can actually do. This is technically complex but important for mechanism #7/#8.

4. **Implement proper ablation controls** - CE-1 has some, but need to be systematic across all mechanisms.

5. **Test for leakage and contamination** - Episodic store has no tests for cross-session contamination, stale memory, false recall etc.

6. **Separate mechanisms cleanly** - The prompt emphasizes not collapsing categories. Need explicit mechanism attribution.

## 6. Recommendations

**Immediate (CE-2 Phase):**
- Build CE-2 as new experiment, don't modify CE-1 history
- Use episodic-memory store as Condition C (external episodic memory) properly
- Implement H3 test (interruption/resumption) - define operationally
- Add leakage detection tests
- Create proper mechanism attribution framework

**Medium term:**
- Investigate Ollama KV cache save/restore capabilities
- Test with actual process restarts
- Add OpenAI API adapter (optional, requires approval)

**Long term:**
- Only pursue consciousness claims if strong behavioral evidence exists AND proper framework in place
- Focus on mechanism identification, not metaphysical claims
