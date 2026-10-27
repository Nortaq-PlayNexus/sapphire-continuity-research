# CHANGELOG — CE-2 Research Program

## 2026-10-28 — Phase 5-9 progress

### Changed
- `runner/ce2_runner.py`: fixed decoy inclusion. Decoys were only included when
  `"decoy" in condition_name`, which matched none of the condition names, so the
  decoy was never tested. Decoys are now included whenever the episodic store is
  in use, so the experiment can measure whether the store prefers the target over
  a near-duplicate.
- `recovery/restart_test.py`: removed `return True` from test functions to clear
  `PytestReturnNotNoneWarning`.

### Added
- `METHODS.md` — experiment methods and measurement definitions.
- `REPRODUCIBILITY.md` — exact setup, run, and verification commands.
- `DATA_DICTIONARY.md` — schema for scenarios, results and metrics.
- `EVIDENCE_LEDGER.md` — claim-to-artifact mapping.
- `RED_TEAM_REPORT.md` — adversarial findings.
- `PREREGISTRATION_CE2_FROZEN.md` — protocol candidate with hash (not yet frozen
  for confirmatory use).
- `run_ce2.ps1` — PowerShell launcher.
- `tests/test_redteam.py` — leakage and contamination tests.

### Run results (exploratory, n=12, seed 12345)
- C0 (fresh): correct 0%, decoy 0%
- C1 (transcript): correct 100%, decoy 0%
- C2 (episodic real): correct 100%, decoy 100%
- C5 (episodic only): correct 100%, decoy 100%
- C6 (transcript only): correct 100%, decoy 0%

Interpretation: the episodic store retrieves both the target and its near-duplicate
decoy, consistent with the episodic-memory finding that this embedding cannot
separate a pair differing only in a number. The store is not content-specific
under this scenario design; it is content-present.

### Not done this phase
- C3, C4, C7, C8 conditions (specified, not implemented).
- KV cache recovery (no supported engine found).
- Confirmatory run (protocol not frozen).