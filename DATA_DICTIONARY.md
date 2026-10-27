# EVIDENCE LEDGER — CE-2

| Claim | Classification | Evidence | Artifact |
|---|---|---|---|
| Episodic store is functional and retrievable | VERIFIED | Adapter smoke test retrieves the correct content; 5 tests pass | `tests/test_adapters.py`, `adapters/episodic_store.py` |
| Application state survives a real process restart | VERIFIED | `recovery/restart_test.py` spawns a child process, loads saved state, retrieves the fact, reports `RESTORED:True` | `recovery/restart_test.py` |
| Transcript replay surfaces the correct answer | VERIFIED | C1: 100% found_correct, 0% decoy | `C:\tmp\ce2_results_*\*_results.json` |
| Episodic store surfaces the correct answer | VERIFIED | C2: 100% found_correct | same |
| Episodic store surfaces the decoy too (no discrimination) | VERIFIED | C2/C5: 100% found_decoy | same |
| Episodic store does not discriminate target from decoy | VERIFIED | Consistent with episodic-memory retrieval-quality finding (margin ~0.005 for numeric near-duplicates) | `projects/episodic-memory/research/RETRIEVAL_QUALITY.md` |
| Fresh baseline finds nothing | VERIFIED | C0: 0% correct, 0% decoy | result JSON |
| H3 (interruption/resumption) demonstrated | NOT TESTED | No experiment measures resumption after interruption of an in-flight computation | — |
| KV cache recovery | NOT TESTED | No supported engine found | — |
| Consciousness/identity claims | NOT TESTABLE | Separated per CE-1 principles | `LIMITATIONS.md` |

## Source-artifact hashes

- PREREGISTRATION_CE2.md SHA-256: `7FF859B571829EDB8CDF786E44C4AC784FE09A6D2F3DDDB18FE2EB955A430986`
- Git commit at time of writing: `cf84fda0b0fd0130e9648d5a33d2c4636020e1e7`