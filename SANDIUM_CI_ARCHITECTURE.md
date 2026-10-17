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

## Brave-native Siso/BuildBuddy adaptation

Detailed design: [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md). The intended model is CircleCI orchestration/source workspace plus Brave-native Siso plus BuildBuddy REAPI, not an Afterbird build wrapper.

Verified source-code findings at Sandium commit 06cd65a7e4fcea784e73c6deb9e4ce52889dc710:

- Brave Core config.ts generates REAPI custom vars when rbe_service is set and defaults the backend to google.star. Sandium must override that path to its own BuildBuddy backend.
- sisoUtils.ts adds Brave's -config googlechrome Siso flag whenever RBE is configured. Compatibility with BuildBuddy must be validated; do not remove or assume it works without evidence.
- use_remoteexec defaults to false; the build CLI supports --use_remoteexec true. Keep remote execution opt-in.
- The saved SANDFOX checkpoint proves only one real Chromium M151 remote C++ compile. It does not prove Sandium's Chromium 156 pin, cache hits, checkpoint restoration, or full APK production.
- Use a Sandium-specific CircleCI project/secret and independently verified BuildBuddy instance/cache namespace. A separate API key alone is not proof of cache isolation.
- Do not use SANDFOX workflows, credentials, caches, checkpoints, artifacts, or source checkout as Sandium dependencies.
- No artificial 35/36-minute cap. Respect actual CircleCI plan limits; preserve diagnostics and add checkpoint logic only if measurement proves it necessary.

## Current status

No Sandium CI workflow or checkpoint implementation has been validated. This document is a proposal, not evidence of a working pipeline.


## Recordkeeping workflow boundary

The scheduled [project recordkeeper](.github/workflows/project-recordkeeper.yml) and [evidence recorder](.github/scripts/record_workflow_evidence.py) are separate from browser-build CI. They collect GitHub workflow metadata only and must never trigger a Brave/Chromium build. General workflow outcomes belong in the experiment log; build notes are updated only for build-related workflows; the clean-base ledger is reserved for relevant build/artifact candidates. End-to-end behavior is not yet verified. CircleCI ingestion is a separate future integration and must use Sandium-specific credentials/configuration only.
