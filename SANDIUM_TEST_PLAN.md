# SANDIUM — Test and Acceptance Plan

A successful workflow exit is not sufficient where the goal is checkpoint restoration or artifact correctness.

## Phase 0 — Documentation system

- [ ] Required documents exist and cross-link correctly.
- [ ] Documentation validator passes.
- [ ] Repeated validation is idempotent and creates no duplicate records.
- [ ] No credentials/tokens are committed.
- [ ] Handoff states exact current state and one next action.

## Phase 1 — Source/build feasibility (no build)

- [ ] Official source repositories and roles identified.
- [ ] Brave/Chromium pins and dependency-sync flow verified.
- [ ] SDK, NDK, JDK, host packages and tool versions verified for selected revision.
- [ ] Checkout/dependency/output storage supported by sources or measurement.
- [ ] Android targets, APK path and verification method identified.
- [ ] Remote execution/cache availability and cost established.
- [ ] Decision record states feasibility under constraints.

## Phase 2 — Sandium-only CI plumbing

- [ ] Workflow exists only in Sandium and has no accidental build trigger.
- [ ] Least-privilege permissions.
- [ ] No SANDFOX resources, caches, credentials or artifacts used as dependencies.
- [ ] Source/config identity recorded for each run/checkpoint.
- [ ] Diagnostics survive failures/timeouts.

## Phase 3 — Checkpoint/cache validation

- [ ] Archive includes required state and metadata.
- [ ] Restore validates integrity and source/config identity.
- [ ] Siso state/journal behavior is verified for pinned version.
- [ ] Before/after action and output counters are captured.
- [ ] Logs prove useful forward progress.
- [ ] Same-workflow and cross-workflow reuse tested separately.
- [ ] Corrupt/stale checkpoints safely rejected.

## Phase 4 — APK baseline

- [ ] Expected APK exists and is non-empty.
- [ ] APK integrity and SHA-256 recorded.
- [ ] Signing/debug state understood.
- [ ] Installs and launches on a real Android device.
- [ ] Basic navigation smoke tests pass.

## Phase 5 — Feature/performance work

Follow charter scope order. Record device, Android version, workload and measurement method. Never claim performance improvement without comparable measurements.

## Result record

Record test ID, date, source commit, run URL, command, expected/actual result, evidence, status and linked experiment/failure IDs.
