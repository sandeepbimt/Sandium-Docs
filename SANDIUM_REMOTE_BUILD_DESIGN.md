# SANDIUM — Bare + CircleCI + BuildBuddy + Siso Remote Build Design

**Status:** Source adapter in progress; all build workflows remain gated  
**Authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Active migration branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)

## Source identity

- Bare repository: https://github.com/BareBrowser/bare-browser
- Reviewed Bare commit: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`
- Chromium commit: `1228231501697ff7a4a0150ea8ae6df37bb99331`
- Chromium version: `156.0.8078.25`
- Bare is an ordered patch series over Chromium Desktop Android, not a complete Chromium source checkout.
- Source preparation must fetch the pinned Bare commit, verify its Chromium pin, check out that exact Chromium revision, apply the ordered patches, and supply the separately versioned/checksummed uBlock Origin CRX input.

## Preserve existing integration

Do not create or reconnect any project, account, context, webhook or credential. Reuse the existing Sandium GitHub repository, CircleCI project/integration, BuildBuddy endpoint/instance, protected `BUILDBUDDY_API_KEY` assignment, Siso integration and cache configuration.

The existing recorded endpoint/instance are `remote.buildbuddy.io:443` and `sandium/android-arm64/ci`. The existing GitHub Actions authentication check passed in [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682). That result proves only the isolated authentication check; it does not prove CircleCI secret visibility, remote action execution, useful cache hits or APK production.

If an existing secret or setting is inaccessible, report its name and stop. Do not rotate, recreate or reassign it. Never print a credential.

## Architecture

- **CircleCI:** retain the existing project and orchestration service. The five-stage workflow is a target design and is not yet wired in the migration branch; current config only exposes the opt-in source preflight and a fail-closed build stub.
- **Bare:** the pinned patch series and build/version instructions.
- **Chromium/depot_tools:** checkout and dependency graph at the exact revision declared by the pinned Bare snapshot.
- **Siso:** use the Siso version and configuration contract from that exact Chromium revision. Do not hardcode a Siso version from an older source workflow.
- **BuildBuddy:** keep the existing REAPI service, endpoint, instance and authentication assignment. Adapt the generated Chromium-native Siso/REAPI configuration to the pinned Chromium revision.
- **Remote execution:** enable only after the generated config is verified and a meaningful action proves it. A successful auth check is not proof of remote execution.
- **Cache:** preserve the existing cache service and all existing cache objects. Use a new Bare-specific key namespace for new build state; never clear old cache data or restore incompatible entries. Avoid uploading the full Chromium source/output tree to CircleCI Free storage; use the BuildBuddy/Siso remote action cache for compiled-action reuse and small source-bound stage ledgers for continuity.

## Source adapter requirements

1. Resolve Bare commit and Chromium commit from the pinned source; fail closed on any mismatch.
2. Compute and record the ordered patch count and digest.
3. Verify the Chromium checkout is exactly the pinned commit and clean before applying patches.
4. Apply patches in deterministic filename order with the documented patch-series mechanism; stop on any conflict or already-applied ambiguity.
5. Supply the expected uBlock Origin CRX as a separately versioned/checksummed input.
6. Generate Chromium-native `.gclient` REAPI variables and the credential-helper configuration using existing settings. Inspect generated `.sisoenv` and runtime flags before any remote action.
7. Ensure the build arguments explicitly select the intended Siso/remote-execution path and do not accidentally select a Google-only remote-execution preset.
8. Keep source checkout, hooks, GN generation, local-only actions, compilation, packaging and verification as separate measured phases.
9. Record Bare SHA, Chromium SHA/version, patch digest, extension digest, toolchain/Siso revision, target ABI, GN args, backend config digest, artifact identity and cache evidence.

## Current adapter artifacts

- Source pin and GN args: `ci/bare/source-pin.txt`, `ci/bare/gn_args.gn`.
- Pre-build cache identity: `ci/bare/write_cache_identity.py`.
- Source/build identity and APK verification: `ci/bare/build_identity.py`.
- Identity-checked checkpoint pack/verify/restore: `ci/bare/checkpoint.py`.
- Artifact naming and checksum: `ci/bare/package_artifact.sh`.
- Guarded source bootstrap: `ci/bare/bootstrap_chromium.sh`; it was not executed.

## Cache/checkpoint policy

- Preserve existing cache objects and settings; do not clear them.
- Existing source checkout and local output checkpoints are not presumed compatible with the Bare source identity.
- Reuse content-addressed remote action results only when action inputs and toolchain identity match; prove useful hits with Siso counters/logs.
- Use stable identity keys containing Bare commit, Chromium commit, patch digest, target, toolchain/Siso revision, GN args and backend-config digest.
- Do not key by only branch, run ID or timestamp.
- Reject incomplete, stale, corrupt or mismatched checkpoints. A cache hit, archive restore or green job alone is not proof of useful reuse.

## No-build gates

The migration branch's full-build workflow fails closed. Keep `run_sandium_bare_source_ready=false` until the five stages are wired to the Bare adapters, new source-identity key namespace, small stage ledgers and artifact verifier, and actual remote execution/cache behavior is separately proven.

Before a build is considered:
- validate YAML and shell syntax;
- verify Bare and Chromium pins and patch digest;
- inspect the actual generated Siso configuration without compiling;
- prove the existing secret references and endpoint/instance are unchanged;
- establish storage, runtime and cost from existing account configuration;
- obtain explicit approval for one controlled build.

No Chromium sync, GN generation, compilation, APK packaging or CircleCI pipeline was run as part of this design update.


## Source-only feasibility review — 2026-10-27

### Source bootstrap correction

The active migration branch had drifted from the previous written status: `bootstrap_chromium.sh` still ran `fetch --nohooks android`, which may start a dependency sync before the workflow enforces its pinned Chromium revision. Commit [`952eb6f`](https://github.com/sandeepbimt/Sandium/commit/952eb6f0b3b6eea206b250b954d7f44a2b4d02db) replaces that sequence with `.gclient` configuration, direct fetch of the exact pinned Chromium commit, pin verification before and after a bounded/logged dependency sync, and no build operation. No source sync was run while making this change. No-build workflow [40443430796](https://github.com/sandeepbimt/Sandium/actions/runs/40443430796) passed.

### Persistence feasibility verdict: BLOCKED / NOT PROVEN

Bare's official [README](https://github.com/BareBrowser/bare-browser) and [BUILDING.md](https://github.com/BareBrowser/bare-browser/blob/main/BUILDING.md) describe a roughly 50 GB Chromium checkout, at least 100 GB free disk, 32 GB allocated VM memory, and a build that takes hours. The current CircleCI config on the migration branch uses a small Python Docker executor for source preflight and a fail-closed stub for the full build; no suitable build resource class or durable source store is configured/proven there.

CircleCI's [cache guide](https://circleci.com/docs/guides/optimize/caching/) says cache entries are immutable for a given key and large caches have restore/expansion costs. Its [persist-data guide](https://circleci.com/docs/guides/optimize/persist-data/) describes caches as reuse across jobs/workflows, but the included Free storage allowance and this account's overage/credit eligibility do not prove that a 50 GB source tree or large output checkpoints can be stored affordably. A cache miss also lets a job proceed by doing the work again; a successful restore step is not proof that useful build work was reused.

BuildBuddy/Siso remote action cache can reuse outputs only for compatible action keys. It does not, by itself, prove that a later CircleCI job has the local Chromium source checkout, dependencies, generated GN graph and toolchain state needed to continue. A five-job workflow that uploads the whole source/output tree is not accepted; a five-job workflow that re-syncs/re-generates from scratch at every stage is not accepted either.

### Required next design change

Before wiring any build job, redesign the stage ledger so stages 1 (source/dependencies) and 2 (toolchain/graph) do not require Siso action counts they cannot generate, and so a stable source/build identity survives the transition from planned GN args to verified effective GN args. Then identify a durable source/output state-transfer mechanism within existing account entitlements, or explicitly conclude that the five-stage requirement cannot be met under current constraints. Keep `run_sandium_bare_source_ready=false`; no build is authorized.
