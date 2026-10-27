# RED TEAM REPORT — CE-2

## Adversarial findings (ordered by severity)

### 1. The decoy was never tested (FIXED this session)
The runner only included decoy episodes when `"decoy" in condition_name`. None of the
condition names contained "decoy", so decoys were silently dropped from every run. Fixed:
decoys are now included whenever the episodic store is in use. Before the fix, `found_decoy`
was 0% in all conditions and the experiment could not measure content-specificity at all.

### 2. The store does not discriminate target from decoy
After the fix, C2 and C5 both show `found_decoy_rate = 1.00`. The episodic store retrieves
both the correct fact and its near-duplicate decoy. This is consistent with the episodic-memory
retrieval-quality measurement (margin ~0.005 for numeric near-duplicates) and is a real
property of the embedding, not a bug. Any continuity claim that rests on "the store picked the
right one" is unsupported.

### 3. `found_correct` is too lenient a metric
`found_correct` is `correct_answer in retrieved_content`. With the correct answer in the store,
it is 100% in every non-fresh condition regardless of mechanism. It cannot distinguish
transcript replay from episodic retrieval from application state. A proper metric would be
"did the retrieved content *cause* the answer" or "was the decoy preferred over the target".

### 4. `AppStateAdapter.teardown()` fails silently
`shutil.rmtree(self.persist_dir)` raises on Windows when the chroma SQLite handle is still
open, is caught by the bare `except`, and returns `False`. The store directory is left on disk.
Not blocking (a new adapter instance is used per run), but it makes teardown unreliable.

### 5. PytestReturnNotNoneWarning in restart tests
`test_save_state`, `test_load_state`, `test_restart_simulation` returned `True`. Fixed this
session by removing the returns.

### 6. No mechanism attribution
The runner reports `found_correct_rate` per condition but does not compute the difference
between conditions that differ by one adapter. "Mechanism attribution" is listed as a measure
in the preregistration but not implemented.

### 7. No leakage test
The hidden answer keys (`correct_answer`, `decoy_answer`) are in the scenario record and in
the result JSON. The runner does not verify they never reach a prompt, filename, log or
metadata available to a tested model. In this harness there is no model call, so leakage is
less relevant, but the check does not exist.

### 8. No cross-scenario contamination test
Each scenario's store is torn down after use, but nothing verifies that scenario i's facts
do not appear in scenario i+1's retrieval results.

### 9. Empty-store / wrong-session / corrupted-state controls not implemented
Specified in the preregistration, not in code.

### 10. No process-restart in the runner
`run_condition` calls `adapter.save_state()` but never kills and restarts a process. The
restart test exists separately (`recovery/restart_test.py`) but is not wired into the runner.

## What survives the red team

- The store genuinely retrieves (correct answer appears in retrieved content).
- Application state survives a real process restart (`RESTORED:True` verified).
- The test suite passes (5 tests).
- The harness runs end to end and produces a machine-readable result.