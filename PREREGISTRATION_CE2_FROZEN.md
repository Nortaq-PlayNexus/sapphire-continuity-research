# PREREGISTRATION CE-2 — PROTOCOL CANDIDATE (NOT FROZEN)

**Status:** CANDIDATE — not frozen. Do not run confirmatory experiments against this document.
**Candidate version:** 0.1.0-draft
**Candidate timestamp:** 2026-10-28
**Source:** `PREREGISTRATION_CE2.md`
**Source SHA-256:** `7FF859B571829EDB8CDF786E44C4AC784FE09A6D2F3DDDB18FE2EB955A430986`
**Git commit at candidate creation:** `cf84fda0b0fd0130e9648d5a33d2c4636020e1e7`
**Evidence grade:** PROPOSED — see the gating conditions below.

## Why this is not frozen

The master prompt and the preregistration's own §11 list the gating conditions:

1. Test harness passes validation — **PARTIAL.** 5 tests pass, but the runner has a
   known defect (decoy inclusion was silently broken until this session) and the
   red-team report lists 10 open items.
2. Exploratory runs complete — **PARTIAL.** One exploratory run exists
   (`C:\tmp\ce2_results_20261028_014602\`), n=12, all non-fresh conditions at 100%
   found_correct, which is not a discriminating result.
3. Protocol reviewed and hash recorded — **NOT DONE.** This document records the hash of
   the *source* preregistration, not of a frozen protocol.
4. Explicit approval if external APIs needed — **N/A.** No API calls are used.

Until those gates close, this document is a **candidate** that can be diffed against the
preregistration to see what changed. It is not a frozen protocol and must not be described
as one.

## What must change before freezing

Taken from `RED_TEAM_REPORT.md`:

1. Fix the decoy-inclusion gate so decoys are always included when the episodic store is
   used. (Done in the runner this session.)
2. Implement mechanism attribution (difference between conditions differing by one adapter).
3. Add leakage detection (hidden answer keys never reach prompts, filenames, logs, metadata).
4. Add cross-scenario contamination test.
5. Add empty-store, wrong-session, and corrupted-state controls.
6. Wire process restart into the runner (currently only `recovery/restart_test.py`).
7. Replace `found_correct` with a metric that measures whether the retrieved content *caused*
   the answer, not just whether it contained it.
8. Validate the test harness end to end with a discriminating exploratory run.

## What this candidate contains

The full text of `PREREGISTRATION_CE2.md` (v0.1.0-draft, 2026-10-27) is reproduced below
unchanged, so the hash above applies to it. Any future change must produce a new hash and a
new version, and must record the deviation.

---

## Reproduced preregistration

(The text of `PREREGISTRATION_CE2.md` follows; see that file for the authoritative copy.)