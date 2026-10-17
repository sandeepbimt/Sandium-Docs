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
- [ ] Sandium-specific BuildBuddy key and isolated REAPI cache instance/namespace verified; a separate key alone is insufficient.
- [ ] Brave-native generated Siso configuration reviewed, including google.star override and -config googlechrome interaction.
- [ ] Decision record states feasibility under constraints.

## Phase 2 — Sandium-only CI plumbing

- [ ] Workflow exists only in Sandium and has no accidental build trigger.
- [ ] Least-privilege permissions.
- [ ] No SANDFOX resources, caches, credentials or artifacts used as dependencies.
- [ ] Remote execution remains opt-in; default build configuration is unchanged.
- [ ] Sandium-specific CircleCI project/context and protected secret are configured before any remote build run.
- [ ] Source/config identity recorded for each run/checkpoint.
- [ ] Diagnostics survive failures/timeouts.

## Phase 2A — Five-stage CI acceptance criteria (mandatory)

These are release gates for the Sandium CI design. They describe required behavior; they do not authorize a browser build or a CI experiment by themselves.

### Stage structure and definitive work

- [ ] The build workflow has exactly five sequential, purpose-named stages. Each stage has one clear primary responsibility and declared inputs/outputs; no stage exists only for naming or to repeat work.
- [ ] Stage 1 — **Source and dependency readiness:** validate source/config identity and reuse a compatible persisted checkout/dependency state; synchronize only what is missing or invalid.
- [ ] Stage 2 — **Toolchain and build graph:** reuse or generate the required toolchain/hook/GN/Siso configuration for the exact build identity; do not repeat Stage 1 work.
- [ ] Stage 3 — **Compile/checkpoint:** execute only outstanding build-graph actions, persist compatible build state and outputs, and detect whether a complete APK has already been produced.
- [ ] Stage 4 — **Restore/continue:** validate and restore the prior stage's state, then execute only remaining required graph actions. If a complete, verified APK already exists, take the fast-skip path instead.
- [ ] Stage 5 — **Finalize/verify/publish:** if no acceptable APK exists, complete only remaining actions, verify APK integrity and source/config identity, publish the artifact and diagnostics, and record checksums.
- [ ] Every handoff carries a manifest with source commit, Brave/Chromium pins, toolchain and GN/build arguments, configuration identity, required state/artifact paths, checksums where applicable, and a clear completion marker.
- [ ] A stage must not repeat a completed sync, graph-generation, compile, archive, or verification action unless its evidence shows that the result is missing, invalid, incompatible, or stale. Normal incremental build logic and explicit cache/checkpoint validation determine what remains.

### One-hour per-stage limit, including handover

- [ ] Each stage's runbook and measured duration include environment/preparation work, source/dependency restore or transfer, configuration, build work, checkpoint packaging, upload/download, integrity checks, artifact handoff, and failure diagnostics—not compilation time alone.
- [ ] Target each stage to finish within **50 minutes end-to-end**, leaving margin against the CircleCI one-hour job ceiling. No planned stage may require 60 minutes; if measured work approaches the target, redesign/split the responsibility before proceeding.
- [ ] Capture stage wall time and separately report handover/restore/package/transfer time so preparation overhead is visible. Report total pipeline elapsed time as well, including inter-stage handover and scheduling where measurable.
- [ ] Save essential diagnostics and the last-known state before timeout where possible. A timeout must not silently discard the evidence needed to resume.

### Reuse within one five-stage run

- [ ] Each stage consumes the previous stage's verified source, dependency, generated configuration, build outputs, and/or checkpoint rather than recreating them from scratch.
- [ ] Handoff integrity is proven by identity/checksum/metadata validation plus action/output counters and elapsed times. Merely seeing an archive, cache-hit label, or green preceding stage is not sufficient proof.
- [ ] Logs show completed work carried forward and show that already-completed actions were not needlessly repeated. If state is incompatible or corrupt, reject it explicitly and record why.

### Reuse across separate CI runs

- [ ] The workflow persists useful Sandium Chromium source/dependency state, toolchain/generated inputs where compatible, build outputs/checkpoints, and Siso/BuildBuddy remote action-cache results beyond an individual pipeline, subject to provider retention/quota.
- [ ] Reuse keys derive from stable build identity—source revision/pins, platform, toolchain, GN/build arguments and relevant CI configuration—not run ID or timestamp. Cache layers and checkpoints have separate documented keys, lifetimes, invalidation rules and storage/transfer costs.
- [ ] A repeated run with identical inputs demonstrates cross-run reuse with logs/counters and lower redundant download/compile work. A source/config/toolchain change invalidates only the affected data, while incompatible state is rejected safely.
- [ ] Cache/checkpoint behavior is verified for Sandium's pinned Siso/Chromium combination and an isolated Sandium namespace. SANDFOX caches, checkpoints, artifacts and credentials are not dependencies.

### Early APK short-circuit

- [ ] If a stage produces a **complete, valid APK for the exact requested build identity**, that producing stage immediately persists the APK plus a manifest containing source/config/toolchain identity, target, size and SHA-256, and finishes required integrity verification before marking the artifact ready.
- [ ] Every downstream stage checks the ready marker before checkout, dependency sync, cache/checkpoint restore, graph generation, compilation or other expensive preparation. When the APK matches and validates, all remaining stages skip that work and exit successfully with an explicit reason.
- [ ] Each downstream fast-skip stage completes its actual job logic within **60 seconds after job start**, excluding provider queue wait. It must not restore large archives or transfer the Chromium tree just to discover that work is complete.
- [ ] Artifact publication and the handoff marker are durable before the producer stage exits, so a downstream stage or later pipeline can find the artifact. A missing, corrupt, incomplete, or identity-mismatched APK must not activate the fast path.
- [ ] A later pipeline with the same requested build identity checks for an already-published, verified APK and reusable state before doing expensive work; it reuses or short-circuits safely rather than rebuilding the same target from zero.

### Required acceptance demonstrations

- [ ] **Cold run:** captures per-stage work, resource use, checkpoint/handover times, total elapsed time and artifact identity.
- [ ] **Same-run handoff:** proves every stage reuses prior compatible data and does not repeat completed work.
- [ ] **Warm cross-run:** reruns the same build identity and proves reusable source/dependencies, checkpoints/build outputs and remote-cache results are actually reused.
- [ ] **Early APK path:** deliberately validates the downstream skip behavior when a verified APK is available before Stage 5; every later stage does no expensive work and finishes its job logic within 60 seconds.
- [ ] **Invalidation/rejection:** changed pins/config and a corrupt or incompatible checkpoint are detected; only affected work is repeated and the reason is logged.
- [ ] No acceptance item is marked passed from design claims alone; retain run IDs, config/source identities, logs, timing, action/output counters, artifact SHA-256 and relevant cache/checkpoint evidence.

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


## Phase 0A — Recordkeeper end-to-end validation

- [ ] Recorder Python syntax passes the repository validator.
- [ ] Scheduled/manual workflow starts and fetches GitHub workflow runs with the provided token.
- [ ] It records a completed non-documentation run once, including run ID, source SHA, jobs, conclusion, artifact metadata and evidence URL.
- [ ] A second poll creates no duplicate records and no commit when nothing has changed.
- [ ] Recordkeeper excludes its own runs and successful docs-validation runs from the latest-project-run snapshot, preventing a workflow feedback loop.
- [ ] Failure/cancelled outcomes are recorded without inventing a root cause.
- [ ] Documentation-only runs are excluded from the clean-base ledger.
- [ ] Build notes/clean-base ledger receive only relevant build/artifact candidates; artifact presence alone does not accept a clean base.
- [ ] Generated status/handoff snapshots are correct and do not overwrite human-authored sections.
- [ ] Recorder cannot trigger browser builds; no browser build starts during these tests.
- [ ] The final automation commit is inspected and linked here.
- [ ] CircleCI integration is separately marked pending until a Sandium-only endpoint/token is configured and tested.
