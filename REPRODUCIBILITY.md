# REPRODUCIBILITY — CE-2

## Environment

- Windows 10, PowerShell
- Python 3.14.x
- Git
- No API keys required for the core suite

## Setup (one time)

```powershell
cd C:\Users\natha\projects\sapphire-continuity-research
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The runner also needs the episodic-memory store. It is already installed at
`C:\Users\natha\projects\episodic-memory` and its venv site-packages are added to `sys.path`
automatically by `adapters/episodic_store.py`.

## Run the test suite

```powershell
cd C:\Users\natha\projects\sapphire-continuity-research
python -m pytest -q
```

Expected: 5 passed (3 warnings are PytestReturnNotNoneWarning from the restart tests).

## Run the experiment

```powershell
cd C:\Users\natha\projects\sapphire-continuity-research
$env:ANONYMIZED_TELEMETRY='False'
python -u runner/ce2_runner.py
```

`ANONYMIZED_TELEMETRY=False` is required: ChromaDB's telemetry blocks store initialisation on
this box with no egress.

## Run the restart test standalone

```powershell
cd C:\Users\natha\projects\sapphire-continuity-research
python recovery/restart_test.py
```

## Outputs

Results are written to `C:\tmp\ce2_results_<timestamp>\ce2-<timestamp>_results.json`.
The runner does not overwrite prior runs.

## Determinism

- Scenario generation uses `random.Random(seed)` with seed 12345.
- Episodic store uses ChromaDB with fixed ONNX embeddings (deterministic).
- No model calls, no network calls, no randomness beyond the seeded generator.

## Verifying the artefacts

- Protocol hash (SHA-256 of PREREGISTRATION_CE2.md): `7FF859B571829EDB8CDF786E44C4AC784FE09A6D2F3DDDB18FE2EB955A430986`
- Git commit at time of this document: see `git rev-parse HEAD`
- Test results: see `tests/` and `pytest` output above