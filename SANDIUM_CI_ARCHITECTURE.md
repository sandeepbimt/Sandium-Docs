# SANDIUM — CI Architecture

**Status:** PROPOSED; not implemented or validated.  
**Boundary:** All build jobs, workflow files, caches, checkpoints, artifacts, credentials and logs are Sandium-specific. SANDFOX is reference-only.

## Goals

- Record every candidate clean base in [SANDIUM_CLEAN_BASE_LEDGER.md](SANDIUM_CLEAN_BASE_LEDGER.md), including GitHub and CircleCI run identities, exact config path/commit, achievement, tests, artifacts and limitations.
- Use purpose-oriented CircleCI workflow/job names; identify each run by workflow name plus pipeline number/ID and source commit. Do not create naming-only runs.

- Establish reproducible Brave Android build within actual resource/cost constraints.
- Use exactly five sequential, purpose-defined stages. Stage boundaries must be measured and optimized, but the five-stage contract is mandatory; each stage must do definitive work without repeating completed actions.
- Prove same-workflow checkpoint restoration before cross-run reuse.
- Preserve diagnostics and avoid repeated work.

## Required five-stage responsibilities

1. **Source and dependency readiness:** validate source/config identity, restore compatible persistent source/dependency state, and synchronize only missing or invalid inputs.
2. **Toolchain and build graph:** reuse or generate the pinned toolchain/hook/GN/Siso configuration needed for this build identity without repeating Stage 1 work.
3. **Compile/checkpoint:** execute only outstanding build-graph actions, persist compatible state and outputs, and detect a completed APK as soon as it exists.
4. **Restore/continue:** validate and restore the prior state, then execute only remaining required actions. If a complete verified APK is available, skip expensive work.
5. **Finalize/verify/publish:** when an acceptable APK is not already available, complete only remaining actions, verify source/config identity and APK integrity, and persist the artifact plus diagnostics.

Each stage has one primary responsibility, explicit inputs/outputs and a handoff manifest. Stage responsibilities may be refined only to fit verified Brave build-graph dependencies; the five-stage requirement is not optional. A stage must not redo completed work unless inputs changed or state is missing, corrupt, stale or incompatible.

## Mandatory execution, handover and reuse contract

- **One-hour ceiling:** budget each stage for no more than 50 minutes end-to-end, leaving safety margin against the CircleCI one-hour job limit. The timed work includes preparation, restore/sync, build graph generation, compilation, checkpoint packaging, uploads/downloads, validation, artifact handover and diagnostics. Record handover time separately and measure total pipeline elapsed time as well. No planned stage may depend on the full 60-minute ceiling.
- **Same-run continuity:** each stage consumes compatible outputs from its predecessor. Preserve source/dependency state, generated inputs, toolchain/configuration, build outputs and checkpoints with an identity/checksum manifest. Demonstrate forward progress with action/output counters and logs; an archive or cache-hit label alone is not proof.
- **Cross-run reuse:** use persistent Sandium-specific storage and a remote action cache across runs. Keys must follow stable source/pin/platform/toolchain/GN/config identity rather than run ID or timestamp. Document retention, invalidation and cost for each cache layer and checkpoint. Test a second run with identical inputs and prove actual reuse; safely reject incompatible or corrupt state.
- **Early APK fast path:** once any stage has produced a complete, integrity-checked APK that matches the requested build identity, that stage must persist the artifact and manifest before exiting. Every later stage checks the ready marker before expensive work, does not sync/restore/compile, and exits successfully within 60 seconds of job start (queue wait excluded). A later run with the same identity must check for that verified artifact and reusable state before rebuilding.
- **Correctness precedes reuse:** artifact manifests carry source/config/toolchain identity, target, size and SHA-256. Missing, corrupt, incomplete or mismatched artifacts must never trigger a skip. Changed inputs invalidate only affected data where proven safe.
- **No cross-project dependencies:** all persistent storage, action-cache namespace, checkpoints and artifacts are Sandium-specific. SANDFOX is reference-only.

The detailed pass/fail checklist and required evidence are in [SANDIUM_TEST_PLAN.md](SANDIUM_TEST_PLAN.md). These are design acceptance gates, not evidence that the implementation has passed and not authorization to start a build.

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

- A preflight-only CircleCI config is staged on [branch ci/sandium-buildbuddy-siso-preflight](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight), commit 3610ff348694d9cf923dbcffaf633017fade4edc. It has a workflow parameter defaulting false and defines no source-sync or build job. Local YAML and bash syntax parsing passed; CircleCI server-side validation, CircleCI project linkage, secret wiring and workflow execution are not verified.
- The preflight checks only source metadata and presence of configured values. It does not call BuildBuddy, authenticate the key, prove cache isolation, or compile. SANDIUM_CACHE_SCOPE_CONFIRMED is only an explicit operator acknowledgment, not technical proof.

## Current status

No Sandium CI workflow or checkpoint implementation has been validated. This document is a proposal, not evidence of a working pipeline.


## Recordkeeping workflow boundary

The scheduled [project recordkeeper](.github/workflows/project-recordkeeper.yml) and [evidence recorder](.github/scripts/record_workflow_evidence.py) are separate from browser-build CI. They collect GitHub workflow metadata only and must never trigger a Brave/Chromium build. General workflow outcomes belong in the experiment log; build notes are updated only for build-related workflows; the clean-base ledger is reserved for relevant build/artifact candidates. End-to-end behavior is not yet verified. CircleCI ingestion is a separate future integration and must use Sandium-specific credentials/configuration only.
