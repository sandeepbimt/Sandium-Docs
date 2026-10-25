# SANDIUM — Project Status

**Last reviewed:** 2026-10-25  
**Status:** Bare-only source boundary committed; full five-stage integration isolated on a gated migration branch; no browser build triggered  
**Repository:** https://github.com/sandeepbimt/Sandium  
**Source authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)

## Current source of truth

- Browser source: [Bare Browser](https://github.com/BareBrowser/bare-browser), pinned for this review at `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`.
- Chromium source pin: `1228231501697ff7a4a0150ea8ae6df37bb99331`, version `156.0.8078.25`.
- Bare is a patch series; it is not a full Chromium checkout. The source adapter must check out the exact Chromium pin, apply Bare's ordered patches and supply the separately versioned/checksummed uBlock CRX.
- The source choice in older records is superseded. Do not use their source-specific scripts, pins or Siso assumptions. Preserve historical records; follow the source boundary above.

## Existing integration — preserve it

- Keep the existing Sandium GitHub repository, CircleCI project/integration, BuildBuddy endpoint/instance, Siso wiring, existing secret assignments, webhooks, contexts, permissions and cache namespace.
- Do not create projects, rotate/reassign tokens, recreate contexts, reconnect integrations or clear caches.
- Existing GitHub Actions Siso authentication check passed in [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682) for `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`. This proves authentication for that check only. It does not prove CircleCI secret visibility, remote action execution, cache hits or APK production.
- If a required setting is not visible to an existing integration, report the setting name and stop; do not create replacement credentials.

## Completed during this session

- [x] Read the current project charter and existing source/build integration records.
- [x] Verified the Bare README and build notes at source level.
- [x] Established a strict source-of-truth rule and a Bare adapter design.
- [x] Adapted `.circleci/config.yml` on `ci/sandium-buildbuddy-siso-preflight` to verify the pinned Bare patch repository and existing integration settings without compiling; static YAML and shell syntax checks passed.
- [x] Created [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter) from the most complete existing five-stage integration branch.
- [x] Added `ci/bare/prepare_source.sh` to verify the pinned Bare commit, Chromium pin/version, ordered patch count/digest and uBlock CRX checksum; Bash syntax check passed. It was not executed against a checkout.
- [x] Added `ci/bare/configure_siso.py` to inspect/write the existing REAPI endpoint, instance, backend and credential-helper paths in the generated `.gclient`; it never reads the API key or runs sync/build. Python syntax compilation and a local `.gclient` fixture test passed; no real workspace or build was used.
- [x] Added a closed `run_sandium_bare_source_ready=false` gate to every workflow in the migration branch so inherited source-specific jobs cannot run accidentally.
- [x] Preserved existing infrastructure; no secrets changed and no browser build triggered.
- [ ] Full five-stage source-dependent steps, checkpoint/cache manifests, artifact names and tests still need Bare adaptation and review. The safety gate must remain false.

## Still unverified

- [ ] Existing CircleCI project/context can access all existing required secret names without re-assignment.
- [ ] Bare source adapter and ordered patch application are implemented and pass no-build validation.
- [ ] Existing Siso/BuildBuddy endpoint, instance, credential helper and cache namespace work with the Bare-pinned Chromium/Siso revision.
- [ ] Useful remote action execution and cache hits are proven for Bare.
- [ ] Reproducible APK is produced, verified, installed and smoke-tested.

## Single next action

Continue adapting the five-stage config to use `ci/bare/prepare_source.sh` and Bare/Chromium source identity throughout cache, checkpoint, compile and artifact paths while keeping all workflows gated. Preserve credentials and cache namespace; do not execute the workflow or run Chromium sync, compilation or APK build.

## Records

- [Charter](SANDIUM_STARTER.md) · [Source of truth](SANDIUM_SOURCE_OF_TRUTH.md) · [Bare adapter design](SANDIUM_BARE_BUILD_ADAPTER.md)
- [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md)
- [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md)

## Safety

No browser build, Chromium sync, credential mutation, cache deletion or SANDFOX infrastructure change was performed for this source pivot.
