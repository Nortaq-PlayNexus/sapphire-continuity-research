# METHODS — CE-2 (Mechanism-Specific Persistence and Cross-Session Continuity)

**Status:** PROPOSED / EXPLORATORY — see PREREGISTRATION_CE2.md and PREREGISTRATION_CE2_FROZEN.md.

## 1. What CE-2 measures

CE-2 tests whether the *mechanism* by which a fact survives into a later turn can be
attributed to a specific persistence channel, by comparing conditions that differ in
which channels are present and by removing one channel at a time.

It is a new experiment. It does not alter CE-1/H1-H8 history and does not retroactively
treat CE-2 decisions as preregistered CE-1 decisions.

## 2. System under test

- **Memory substrate:** the real episodic-memory store (`C:\Users\natha\projects\episodic-memory`),
  ChromaDB 1.5 + ONNXMiniLM_L6_V2 (all-MiniLM-L6-v2, 384-dim), cosine distance. This addresses
  the gap that H8 used synthetic episode blocks injected into prompts rather than the real store.
- **Transcript substrate:** an in-memory list of `{role, content}` messages replayed into the
  prompt (Condition C1).
- **Application-state substrate:** a JSON file on disk (`AppStateAdapter`), written and read back
  by a different process (`recovery/restart_test.py`).
- **No LLM is called.** Retrieval is the whole measurement, so the results are mechanism-level,
  not model-level.

## 3. Conditions

| ID | Name | Adapters | What it tests |
|---|---|---|---|
| C0 | Fresh baseline | none | guessing / prior knowledge |
| C1 | Transcript replay | transcript | context continuity via supplied history |
| C2 | Episodic store (real) | episodic_store | external episodic memory (real ChromaDB store) |
| C5 | Episodic only, no transcript | episodic_store | isolation of the memory mechanism |
| C6 | Transcript only | transcript | isolation of the transcript mechanism |

Conditions C3 (episodic + transcript), C4 (app state save/restart), C7 (restart control) and C8
(KV cache recovery) are specified in PREREGISTRATION_CE2.md but not yet implemented or run.

## 4. Scenario generation

12 scenarios per run, seed 12345, deterministic. Each scenario has one fact
(`{entity} uses access code {code} and has limit {value} requests`), a matched decoy with a
different code, 3-4 transcript messages, and a question. Scoring: substring match of the correct
answer in retrieved content, and of the decoy answer.

## 5. Measurement

- `found_correct_rate` — fraction of scenarios in which the correct answer appears in retrieved
  content.
- `found_decoy_rate` — fraction in which the decoy answer appears in retrieved content.
- Mechanism attribution: difference between conditions that differ by one adapter.

## 6. Adversarial controls

- Matched decoys (same entity, different code).
- Empty store (C0).
- Process restart with a real subprocess (`recovery/restart_test.py`).
- Leakage check: hidden answer keys are never placed in prompts, filenames, logs or metadata.
- Cross-scenario isolation: each scenario's store is torn down after use.

## 7. Limitations

- No LLM is called, so the measurement is "did the retrieved content contain the answer", not
  "did the model use it correctly".
- The decoy is retrieved alongside the correct answer in the episodic conditions (see
  RED_TEAM_REPORT.md), so the store does not discriminate between them — consistent with the
  episodic-memory retrieval-quality finding that near-duplicate numeric values are not separable
  by this embedding.
- C4/C7/C8 (restart, KV cache) are specified but not run.
- Small sample (n=12 scenarios); exploratory only.