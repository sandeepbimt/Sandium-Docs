# SANDIUM — Project Status

**Last reviewed:** 2026-10-25  
**Status:** Bare-only source boundary committed; migration branch has a source-only preflight and a fail-closed full-build gate; five-stage build is not yet wired; no browser build triggered  
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
- [x] Created [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter) as an isolated migration branch; the existing default branch and its infrastructure were not changed.
- [x] Added `ci/bare/prepare_source.sh` to verify the pinned Bare commit, Chromium pin/version, ordered patch count/digest and uBlock CRX checksum; Bash syntax check passed. It was not executed against a checkout.
- [x] Added `ci/bare/configure_siso.py` to inspect/write the existing REAPI endpoint, instance, backend and credential-helper paths in the generated `.gclient`; it never reads the API key or runs sync/build.
- [x] Added `ci/bare/source-pin.txt` and `gn_args.gn` as explicit source and build-target pins.
- [x] Added `ci/bare/write_cache_identity.py` to fingerprint the pinned patch series, extension input, toolchain, GN args, backend and credential-helper configuration.
- [x] Added `ci/bare/build_identity.py` for source/build manifests and APK ZIP, DEX/manifest, signature, size and SHA-256 verification.
- [x] Added `ci/bare/checkpoint.py` to verify archive hashes and source/build identity before restore, then recheck after restore; existing output is preserved as a backup if replaced.
- [x] Added `ci/bare/package_artifact.sh` and unit tests for source-pin parsing and APK integrity.
- [x] Added `ci/bare/bootstrap_chromium.sh`; full Chromium sync is fail-closed unless `SANDIUM_ALLOW_CHROMIUM_SYNC=true` is explicitly supplied. It was not executed.
- [x] Added the opt-in `sandium-bare-source-preflight` CircleCI workflow (default off) to run syntax checks, unit tests, pinned-source checks and extension checksum validation without Chromium sync or compilation.
- [x] Replaced the migration branch's active CircleCI config with a Bare-only, opt-in source preflight and an explicit fail-closed full-build workflow. The five-stage build is not advertised as runnable until its source/output persistence path is proven.
- [x] Preserved existing infrastructure; no secrets changed and no browser build triggered.
- [ ] The new Bare bootstrap, identity, checkpoint and packaging scripts have not been executed against a real Chromium workspace; the preflight workflow has not been run.
- [ ] The five-stage compile/restore/publish workflow still needs to be designed around the new identity/checkpoint scripts and source-specific cache keys; no build stages are enabled.
- [x] Checked current CircleCI official pricing/docs: Free includes 2 GB of storage; storage beyond the allowance consumes credits. Public open-source projects may qualify for up to 400,000 monthly credits, but account eligibility is not verified. See [CircleCI pricing](https://circleci.com/pricing/) and [persisting data](https://circleci.com/docs/guides/optimize/persist-data/).
- [x] Decided not to persist the full Chromium source or build-output tree in CircleCI caches/workspaces. Keep only small identity/ledger metadata there; actual cross-stage reuse must come from proven BuildBuddy/Siso remote action-cache hits.
- [ ] BuildBuddy/Siso remote action execution and useful cache hits are not yet proven for the pinned Bare build. The full-build safety gate must remain false.

## Still unverified

- [ ] Existing CircleCI project/context can access all existing required secret names without re-assignment.
- [ ] Bare source adapter and ordered patch application are implemented and pass no-build validation.
- [ ] Existing Siso/BuildBuddy endpoint, instance, credential helper and cache namespace work with the Bare-pinned Chromium/Siso revision.
- [ ] Useful remote action execution and cache hits are proven for Bare.
- [ ] Reproducible APK is produced, verified, installed and smoke-tested.

## Single next action

Design the five stages to re-check out the pinned source and reuse work through the existing BuildBuddy/Siso remote action cache, persisting only small source-bound stage ledgers in CircleCI. Before enabling any build, obtain explicit approval for a small remote-execution/cache proof. Keep the full-build gate false; no pipeline, Chromium sync, compilation or APK build.

## Records

- [Charter](SANDIUM_STARTER.md) · [Source of truth](SANDIUM_SOURCE_OF_TRUTH.md) · [Bare adapter design](SANDIUM_BARE_BUILD_ADAPTER.md)
- [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md)
- [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md)

## Safety

No browser build, Chromium sync, credential mutation, cache deletion or SANDFOX infrastructure change was performed for this source pivot.
