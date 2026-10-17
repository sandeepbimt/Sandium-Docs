# SANDIUM — CI Architecture

**Status:** PROPOSED; not implemented or validated.  
**Boundary:** All build jobs, workflow files, caches, checkpoints, artifacts, credentials and logs are Sandium-specific. SANDFOX is reference-only.

## Goals

- Record every candidate clean base in [SANDIUM_CLEAN_BASE_LEDGER.md](SANDIUM_CLEAN_BASE_LEDGER.md), including GitHub and CircleCI run identities, exact config path/commit, achievement, tests, artifacts and limitations.
- Use purpose-oriented CircleCI workflow/job names; identify each run by workflow name plus pipeline number/ID and source commit. Do not create naming-only runs.

- Establish reproducible Brave Android build within actual resource/cost constraints.
- Use five sequential stages only if measured boundaries provide benefit.
- Prove same-workflow checkpoint restoration before cross-run reuse.
- Preserve diagnostics and avoid repeated work.

## Proposed stage responsibilities

1. **Preflight/source:** verify runner resources, pin source revisions, sync dependencies and record source identity.
2. **Build graph/toolchain:** verify pinned toolchain, run required hooks and validate generated graph and Siso/remote configuration.
3. **Compile/checkpoint:** run a bounded compile segment, collect progress metrics and save a compatible checkpoint.
4. **Restore/continue:** restore and validate checkpoint, verify Siso state/journal reconciliation and forward progress.
5. **Complete/verify:** finish compilation if possible, verify APK integrity and SHA-256, publish artifact and diagnostics.

These responsibilities are a hypothesis to review against the selected Brave build graph. Do not preserve five stages just for appearance if evidence supports another structure.

## Mandatory gates

- No build until feasibility, expected cost, pass criteria and diagnostics are documented and approved.
- No Sandium workflow may trigger or depend on SANDFOX jobs.
- Never copy SANDFOX credentials, caches, checkpoint archives or artifacts.
- Record exact Brave Core, Chromium, toolchain, GN args and patch identity with checkpoints.
- Distinguish remote action-cache reuse from serialized local build-state restoration.
- Cache hit, archive upload, job success or action count alone is not proof of continuation.
- Validate archive integrity, source/config identity, Siso state/journal and required file metadata.
- Compare before/after completed-action and output counters and retain logs proving forward progress.
- Use idempotent run identifiers; preserve diagnostics after failure/timeout; never log secrets.

## Cache layers to distinguish

1. Source/dependency reuse.
2. Remote action cache.
3. Runner-local cache.
4. Serialized checkpoint archive.
5. Same-workflow workspace handoff.

Document persistence, keys, retention, invalidation and cost separately for each layer.

## Implementation sequence

1. Finish source-level Brave build feasibility audit.
2. Establish Sandium-only CI project and least-privilege secrets without triggering compilation.
3. Validate documentation-only/preflight workflow.
4. Validate source pinning and graph generation if cost permits.
5. Test checkpoint archive/restore with a minimal controlled test.
6. Approve one incremental compile experiment only after prior gates pass.
7. Prove same-workflow continuation before cross-workflow persistence.
8. Require a reproducible, verified APK before baseline completion.

## Current status

No Sandium CI workflow or checkpoint implementation has been validated. This document is a proposal, not evidence of a working pipeline.
