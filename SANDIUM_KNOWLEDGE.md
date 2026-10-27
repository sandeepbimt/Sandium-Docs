# SANDIUM — Durable Knowledge Index

**Read first:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md). Bare Browser is the only active browser-source authority. Older source-specific implementation notes are superseded and must not guide current work.

## Governing rules

1. Current source is exclusively Bare Browser plus the exact Chromium revision pinned by the selected Bare snapshot.
2. Preserve the existing Sandium GitHub/CircleCI/BuildBuddy/Siso integration, credentials, endpoint/instance assignments, webhooks, contexts and cache service. Keep all existing cache objects intact, but use a new Bare-specific key namespace for new source/build state.
3. Do not recreate or rotate tokens, reconnect projects, recreate contexts, or clear caches.
4. Keep `run_sandium_bare_source_ready=false` until all source-dependent pipeline steps are adapted and reviewed.
5. Do not trigger Chromium sync, GN generation, compilation or APK packaging during migration.
6. Do not claim remote execution, cache reuse, checkpoint restoration or APK success without logs and artifact evidence.
7. Preserve history; label older source-specific records superseded rather than treating them as current implementation guidance.
8. Never write credentials or token values to repository docs/logs.
9. ChatGPT owns session-level decisions and handoff updates; automated workflows capture machine-observable evidence.
10. SANDFOX is separate and must never be used as a build dependency.

## Verified Bare source state

- Repository: https://github.com/BareBrowser/bare-browser
- Reviewed Bare commit: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`
- Chromium commit: `1228231501697ff7a4a0150ea8ae6df37bb99331`
- Chromium version: `156.0.8078.25`
- Bare is a patch series over Chromium Desktop Android; apply patches in deterministic order and provide the separately versioned/checksummed uBlock Origin CRX input.
- Bare's published local builder is not proof that the same Docker builder can be used unchanged in CircleCI.

## Verified integration state

- Existing BuildBuddy endpoint/instance recorded in Sandium CI: `remote.buildbuddy.io:443` / `sandium/android-arm64/ci`.
- Existing GitHub Actions authentication check: [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682), successful for authentication only.
- The migration branch's active CircleCI config is Bare-only: opt-in source preflight plus a fail-closed full-build stub. The five-stage build is not yet wired.
- A separate no-build source preflight was adapted on `ci/sandium-buildbuddy-siso-preflight`; static YAML parsing and shell syntax checks passed. The CircleCI workflow has not been executed.
- No Bare remote action, cache hit, full APK build, install or device smoke test is proven.

## Active branches

- Migration workspace: [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter). The closed readiness gate must stay false.
- No-build source metadata prototype: [`ci/sandium-buildbuddy-siso-preflight`](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight).
- Do not use historical build branches as current source guidance.

## Required next technical work

Implement five stages using the pinned Bare source and existing BuildBuddy/Siso remote action cache; pass only small source-bound stage ledgers through CircleCI. Keep all build workflows fail-closed, preserve credentials and old cache objects, use a new Bare-specific key namespace, and request separate approval before any remote-execution/cache proof or browser build.

Detailed requirements: [Bare adapter](SANDIUM_BARE_BUILD_ADAPTER.md), [remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md), [CI architecture](SANDIUM_CI_ARCHITECTURE.md), [automation contract](SANDIUM_AUTOMATION_RULES.md).


## Stage progress and action-cache interpretation (2026-10-27)

- Treat Siso/Ninja `finished/total` values as invocation/graph-scoped progress. Do not add a previous stage's `finished` count to a later invocation's numerator; the action sets may overlap and graph denominators may differ.
- A restored output archive or a green restore step is not proof that Siso consumed those outputs. Keep separate evidence for checkpoint identity/integrity, actual current-stage remote-execution actions, and remote action-cache hits.
- The active Bare ledger now records `action_count_scope=STAGE_LOCAL_ONLY_NOT_CUMULATIVE` and requires stage-specific Siso remote/cache evidence. See [stage_ledger.py](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/stage_ledger.py) and [FAIL-LEDGER-002](SANDIUM_FAILURE_LEARNINGS.md#fail-ledger-002--stage-local-siso-progress-was-added-to-a-prior-stage-baseline).
- Historical branches such as `build/bare-apk-once-20261025` are evidence only, not active workflow guidance. Continue work on `migration/bare-source-adapter`; leave `run_sandium_bare_source_ready=false` until the pipeline and persistence design pass review.
