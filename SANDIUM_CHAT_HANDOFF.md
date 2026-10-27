# SANDIUM — Chat Handoff

**Updated:** 2026-10-27  
**Current source:** Bare Browser only  
**Current branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)  
**Status:** Latest no-build test workflow passes after a test-call fix; Bare-only source preflight remains opt-in and full build fails closed. Stage-ledger schema 2 is validated by unit tests; the five-stage build runner is not yet wired.

## Read these first

1. [Source of truth](SANDIUM_SOURCE_OF_TRUTH.md)
2. [Project charter](SANDIUM_STARTER.md)
3. [Current status](SANDIUM_STATUS.md)
4. [Bare adapter](SANDIUM_BARE_BUILD_ADAPTER.md)
5. [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md)
6. [CI architecture](SANDIUM_CI_ARCHITECTURE.md)
7. [Automation contract](SANDIUM_AUTOMATION_RULES.md)

## Verified work

- Bare source snapshot reviewed: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`; Chromium pin `1228231501697ff7a4a0150ea8ae6df37bb99331`, version `156.0.8078.25`.
- The authoritative source boundary and Bare-specific adapter/design docs are committed in Sandium-Docs.
- `migration/bare-source-adapter` is isolated from the default branch. Its active CircleCI config is Bare-only: an opt-in source preflight and a fail-closed full-build stub.
- The five-stage compile/restore/publish workflow is not yet wired. The user's prior successful Afterbird APK on the same existing CircleCI plan is the operational precedent; do not re-open plan constraints absent a concrete Bare-specific failure. The outstanding work is the Bare-specific source/output handoff, stage identity continuity, remote Siso execution/cache evidence and APK verification.
- Historical Stage 2 failure #657 exposed invalid cumulative action-count accounting (prior baseline 103,735 plus current invocation count 55,453 against a 109,040 normalized total). The canonical Bare branch stores invocation-local metrics in [`cce70d9`](https://github.com/sandeepbimt/Sandium/commit/cce70d9028ac1662e1a3a22e40fcbb4ca53c140c); regression workflow [`40442432290`](https://github.com/sandeepbimt/Sandium/actions/runs/40442432290) passed. The source bootstrap was then corrected to configure `.gclient`, fetch the exact Chromium pin directly, verify it before/after dependency sync, and time-bound/log both network phases in [`952eb6f`](https://github.com/sandeepbimt/Sandium/commit/952eb6f0b3b6eea206b250b954d7f44a2b4d02db); no-build workflow [`40443430796`](https://github.com/sandeepbimt/Sandium/actions/runs/40443430796) passed.
- The separate no-build preflight branch verifies the pinned Bare patch repository and keeps the existing protected credential name; it does not run Chromium sync or compilation.
- Static YAML parsing and shell syntax checks passed for the no-build preflight content. CircleCI server validation/execution has not been run.
- Existing recorded Siso authentication check passed at `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`; remote action execution, cache hits and APK production remain unverified.
- Stage-ledger schema 2 has stage-specific evidence: Stage 1 source-preparation marker; Stage 2 generated GN args/build graph; Stage 3 uncached remote Siso execution; Stage 4 remote-cache hit plus additional uncached remote execution; Stage 5 direct APK/signature verification. Stable pre-build identity is separated from the generated GN fingerprint. Commits: [`b430976`](https://github.com/sandeepbimt/Sandium/commit/b430976590588cac211dd3321a8459dfe5cabe85), [`25f4347`](https://github.com/sandeepbimt/Sandium/commit/25f43470e9f383a53f2907092b7a5839c341316a), [`05aa490`](https://github.com/sandeepbimt/Sandium/commit/05aa490da9d02ec97b30565f27224f5c0a096538), [`a344207`](https://github.com/sandeepbimt/Sandium/commit/a344207e970e43562397067d14a9c01c87190be8), and [`440aaa9`](https://github.com/sandeepbimt/Sandium/commit/440aaa98980e498d5bea551d0097a51fac68f31f). The latest no-build workflow is confirmed green: [run 40449280006](https://github.com/sandeepbimt/Sandium/actions/runs/40449280006) on commit [`f369449`](https://github.com/sandeepbimt/Sandium/commit/f3694497db2cfe43cc079f3ff49c740a8ac80738). All 23 tests and static checks passed; the run explicitly did not sync Chromium, generate GN, run Siso or build an APK.
- No token/secret was changed, no cache was cleared, and no browser build was triggered.

## Non-negotiable continuity rules

- Never use superseded source-specific scripts, pins, patch flows, Siso presets or cache assumptions.
- Reuse the existing GitHub/CircleCI/BuildBuddy/Siso integration and credentials; do not re-establish or rotate them.
- Preserve all existing cache data. Do not restore old local checkpoints unless the exact source identity is compatible.
- Do not set `run_sandium_bare_source_ready=true` until the complete pipeline is Bare-compatible and reviewed.
- Do not run a CircleCI pipeline, Chromium sync, GN generation, compilation or APK build during this migration step.
- Keep SANDFOX completely separate.

## Single next action

Review and wire the Bare-specific five-stage source/output handoff using current evidence and the existing Afterbird success as the operational precedent. Do not investigate plan limits absent a concrete failure; do not clear/recreate caches; keep `run_sandium_bare_source_ready=false` and require separate approval before any full build.

<!-- SANDIUM_AUTO_STATUS_START -->
- No completed GitHub workflow run was available from the API.\n
<!-- SANDIUM_AUTO_STATUS_END -->


## Stage-ledger schema 2 update — 2026-10-27

The source-level mismatch between five-stage responsibilities and ledger requirements has been corrected. The stable source/toolchain identity does not include generated GN state; the GN fingerprint is established at Stage 2 and enforced thereafter. Stage-local Siso counters are not summed. Stage 5 checks artifact identity and invokes direct APK/signature verification rather than relying only on manifest flags. This does not wire the five-stage workflow or prove persistence feasibility. No-build test results must be checked; no Chromium sync, GN generation, Siso compile or APK job was launched for this redesign.


## CircleCI Free feasibility — public review completed, account check still required

The public plan documentation shows Free at 30,000 credits/month, 1 GB included network transfer and 2 GB-months storage; Bare documents roughly 50 GB Chromium source, 100 GB free disk and 32 GB RAM. Public resource tables list a possible Linux VM class with 32 GB RAM/150 GB disk, but whether the existing account can use it and has sufficient credits is not exposed by the connected tools. Details and official citations are in [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md). No CircleCI setting, cache, credential, or build was touched. Next, inspect the current account's Plan/Usage, Network/Storage, available resource classes, and effective timeout; keep the full-build gate false.
