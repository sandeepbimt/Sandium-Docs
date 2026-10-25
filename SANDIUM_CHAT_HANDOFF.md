# SANDIUM — Chat Handoff

**Updated:** 2026-10-25  
**Current source:** Bare Browser only  
**Current branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)  
**Status:** Bare-only source preflight is opt-in; full build fails closed. Five-stage compile/restore/publish is not wired pending proof of source/output persistence.

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
- The five-stage compile/restore/publish workflow is not yet wired because the existing CircleCI account's persistence capacity for Chromium source and build output has not been proven.
- The separate no-build preflight branch verifies the pinned Bare patch repository and keeps the existing protected credential name; it does not run Chromium sync or compilation.
- Static YAML parsing and shell syntax checks passed for the no-build preflight content. CircleCI server validation/execution has not been run.
- Existing recorded Siso authentication check passed at `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`; remote action execution, cache hits and APK production remain unverified.
- No token/secret was changed, no cache was cleared, and no browser build was triggered.

## Non-negotiable continuity rules

- Never use superseded source-specific scripts, pins, patch flows, Siso presets or cache assumptions.
- Reuse the existing GitHub/CircleCI/BuildBuddy/Siso integration and credentials; do not re-establish or rotate them.
- Preserve all existing cache data. Do not restore old local checkpoints unless the exact source identity is compatible.
- Do not set `run_sandium_bare_source_ready=true` until the complete pipeline is Bare-compatible and reviewed.
- Do not run a CircleCI pipeline, Chromium sync, GN generation, compilation or APK build during this migration step.
- Keep SANDFOX completely separate.

## Single next action

Prove where Chromium source and build output can persist within the existing CircleCI account. Then wire the new identity/checkpoint scripts into five stages with new Bare-specific cache keys. Keep the full-build gate closed; no pipeline, sync, compile or APK build.
