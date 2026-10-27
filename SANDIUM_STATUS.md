# SANDIUM — Project Status

**Last reviewed:** 2026-10-27  
**Status:** Stage-ledger schema 2 redesign committed; five-stage build remains blocked on durable source/build-state persistence and unproven resource entitlements  
**Repository:** https://github.com/sandeepbimt/Sandium  
**Source authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)

## Latest controlled build investigation — 2026-10-25

- Source-only CircleCI preflight on `fix/bare-stage-handoff-review` passed: adapter syntax/tests, 164 Bare patch files, pinned Chromium commit/version and uBlock CRX checksum/cache identity checks.
- The first full attempt completed the initial `fetch android` command in 8m23s, then its separate pinned `gclient sync --verbose --no-history --nohooks --revision src@1228231501697ff7a4a0150ea8ae6df37bb99331` hit the 20-minute timeout (exit 124). Available logs showed repeated `Still working on: src`, but did not include the underlying Git transport error. No GN generation, Siso compile or APK resulted.
- A later live log showed a Git fetch retry warning for `src/third_party/clang-format/script` at commit `9f796802e5d633c96dbe97e0b6683d5e625949f9`. That warning alone does not prove whether the cause was transport failure or shallow-fetch/server behavior.
- Online evidence: depot_tools’ `fetch` flow runs `gclient config` followed by `gclient sync`, and `--no-history` requests shallow clones. Chromium’s official dependency docs confirm dependencies are pinned by hashes in `DEPS`. A Chromium-dev report of the same retry pattern describes HTTP 400 shallow-info failures; another reports connection reset/early EOF. These are relevant failure modes, **not proof of this run’s exact cause**: [depot_tools fetch source](https://github.com/columbia/depot_tools/blob/main/fetch.py), [Chromium dependency documentation](https://github.com/chromium/chromium/blob/main/docs/dependencies.md), [Chromium-dev HTTP 400 case](https://groups.google.com/a/chromium.org/g/chromium-dev/c/pRDAs6tm-Zs), [Chromium-dev connection-reset case](https://groups.google.com/a/chromium.org/g/chromium-dev/c/UFZ7B19A1eM).
- Code change: bypass `fetch android` because its internal dependency sync occurs **before** the later pin step. The script now configures `.gclient` only, fetches and checks out the exact Chromium pin, then runs one dependency sync against that pinned source. Both the direct source fetch (15-minute bound) and dependency sync (20-minute bound) are time-limited. Git command tracing and separate config/fetch/sync artifacts are enabled. The source sequencing fix is [`8009f34`](https://github.com/sandeepbimt/Sandium/commit/8009f34419ca807f004a2176741f8c7a166c0bc1); log-initialization, pre-network syntax-check and direct-fetch timeout follow-ups are [`cd74848`](https://github.com/sandeepbimt/Sandium/commit/cd74848bf7e866772ce05e2a3dfa0afb48e85dd6), [`a4e9f64`](https://github.com/sandeepbimt/Sandium/commit/a4e9f6469059bdb024201392987cfc524c357877) and [`f0cb6c7`](https://github.com/sandeepbimt/Sandium/commit/f0cb6c7cd055fb4c9b4686ab6c23bea70a1a7add). The five-stage runner now transfers only small stage ledgers through CircleCI cache and relies on BuildBuddy/Siso remote action cache for compiled-action reuse; a final job fails unless stage 5 reports a ZIP- and signature-verified APK. These behaviours remain unverified by a successful run. Related commits: [`e8f643f`](https://github.com/sandeepbimt/Sandium/commit/e8f643f219309c1fac15408e4a6616d79583e55b), [`d3a613f`](https://github.com/sandeepbimt/Sandium/commit/d3a613f9f3f1a63c4ba95d393d1117373ca5c5cf), [`a890529`](https://github.com/sandeepbimt/Sandium/commit/a89052989a9c19a70286950192114c96d0ddf31d) and [`6a9bf6d`](https://github.com/sandeepbimt/Sandium/commit/6a9bf6d29b94c22659da502821dee6e5dad5fc28).
- **Status of fix:** committed but not yet tested by a new CircleCI run. No APK has been produced. This branch remains experimental and is not an accepted clean base.


## Latest progress-accounting diagnosis — 2026-10-27

- Historical run evidence: CircleCI build #657 on `build/bare-apk-once-20261025`, control head `a8617078ceda724451e474a7bd09eacafdb1a92a`. It restored a 11,320,374,898-byte output checkpoint and then failed Stage 2 on `103735 + 55453 > 109040`.
- Root cause: invalid cumulative arithmetic across invocation-scoped Siso progress counts. Ninja defines the displayed numerator/denominator as finished edges and edges that must be run for the current graph. See [Ninja manual](https://ninja-build.org/manual.html#environment-variables).
- Corrective change: active Bare branch commit [`cce70d9`](https://github.com/sandeepbimt/Sandium/commit/cce70d9028ac1662e1a3a22e40fcbb4ca53c140c) records stage-local metrics only and keeps real per-stage remote/cache proof requirements.
- Lightweight no-build tests: [workflow run 40442432290](https://github.com/sandeepbimt/Sandium/actions/runs/40442432290) passed. It ran stage-ledger/source-identity tests and shell syntax checks; no Chromium sync, GN generation or Siso compilation occurred.
- The historical build is not current source guidance. Continue only on [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter); keep `run_sandium_bare_source_ready=false`. The pinned-bootstrap fix in [`952eb6f`](https://github.com/sandeepbimt/Sandium/commit/952eb6f0b3b6eea206b250b954d7f44a2b4d02db) passed no-build run [40443430796](https://github.com/sandeepbimt/Sandium/actions/runs/40443430796). No CircleCI run, Chromium sync, GN generation, compile or APK build was started.

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
- [x] Added `ci/bare/checkpoint.py` for identity-bound output archives; documented that large archives must not be stored in CircleCI Free storage.
- [x] Added `ci/bare/stage_ledger.py` to bind small stage records to the exact source/build identity and require Siso remote-execution/cache evidence.
- [x] Added `ci/bare/package_artifact.sh` and unit tests for source-pin parsing and APK integrity.
- [x] Added `ci/bare/bootstrap_chromium.sh`; full Chromium sync is fail-closed unless `SANDIUM_ALLOW_CHROMIUM_SYNC=true` is explicitly supplied. It was not executed.
- [x] Added the opt-in `sandium-bare-source-preflight` CircleCI workflow (default off) to run syntax checks, unit tests, pinned-source checks and extension checksum validation without Chromium sync or compilation.
- [x] Kept the Bare source preflight opt-in and wired a separate, explicitly user-approved experimental five-stage APK lane on `fix/bare-stage-handoff-review`; it is branch- and parameter-gated, and ordinary pushes do not select it.
- [x] Preserved existing integrations; no credentials were changed, no caches were cleared and no SANDFOX infrastructure was touched. A user-approved experimental build ran on the review branch; no APK has been produced.
- [ ] The new Bare bootstrap, identity, checkpoint and packaging scripts have not been executed against a real Chromium workspace; the preflight workflow has not been run.
- [ ] The five-stage runner has not completed a successful full run; source sync, stage handoff, remote-cache reuse, compilation and APK publication remain unverified.
- [x] Checked current CircleCI official pricing/docs: Free includes 2 GB of storage; storage beyond the allowance consumes credits. Public open-source projects may qualify for up to 400,000 monthly credits, but account eligibility is not verified. See [CircleCI pricing](https://circleci.com/pricing/) and [persisting data](https://circleci.com/docs/guides/optimize/persist-data/).
- [x] Decided not to persist the full Chromium source or build-output tree in CircleCI caches/workspaces. Keep only small identity/ledger metadata there; actual cross-stage reuse must come from proven BuildBuddy/Siso remote action-cache hits.
- [ ] BuildBuddy/Siso remote action execution and useful cache hits are not yet proven for the pinned Bare build. The current explicitly approved attempt is experimental; do not claim success until logs prove remote execution/cache hits and a verified APK.

## Current blocker

The Bare five-stage pipeline is not yet wired. The source-level ledger contract has been redesigned in schema 2: Stage 1 requires source-preparation evidence; Stage 2 requires generated GN args and a Ninja graph; Stage 3 requires an uncached remote Siso action; Stage 4 requires a current-stage remote-cache hit; Stage 5 verifies artifact identity and reruns APK/signature checks. The stable source/toolchain identity no longer changes when the GN fingerprint first appears, and Siso counters remain invocation-local. The updated no-build workflow must be confirmed green before claiming test validation. The remaining major blocker is persistence/resource feasibility: Bare describes roughly 50 GB of Chromium source, 100 GB free disk and 32 GB allocated VM, while the existing CircleCI config is a small Python preflight and account entitlements/state-transfer are not proven. Keep `run_sandium_bare_source_ready=false`.

## Still unverified

- [ ] Existing CircleCI project/context can access all existing required secret names without re-assignment.
- [ ] Bare source adapter and ordered patch application are implemented and pass no-build validation.
- [ ] Existing Siso/BuildBuddy endpoint, instance, credential helper and cache namespace work with the Bare-pinned Chromium/Siso revision.
- [ ] Useful remote action execution and cache hits are proven for Bare.
- [ ] Reproducible APK is produced, verified, installed and smoke-tested.

## Single next action

Prove a safe, durable source/build-state transfer and sufficient existing runner/storage entitlements for the Bare workflow without creating or clearing caches, changing credentials, or launching a build. Keep `run_sandium_bare_source_ready=false`; no Chromium sync, GN generation, compilation or APK packaging.

## Records

- [Charter](SANDIUM_STARTER.md) · [Source of truth](SANDIUM_SOURCE_OF_TRUTH.md) · [Bare adapter design](SANDIUM_BARE_BUILD_ADAPTER.md)
- [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md)
- [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md)

## Safety

An explicitly approved experimental Chromium source-sync build was attempted on the review branch. No APK was produced. No credentials were mutated, no cache was deleted and no SANDFOX infrastructure was changed.

<!-- SANDIUM_AUTO_STATUS_START -->
- No completed GitHub workflow run was available from the API.\n
<!-- SANDIUM_AUTO_STATUS_END -->


## Stage-ledger redesign recorded — 2026-10-27

The active [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter) branch now carries schema 2 stage-specific ledger evidence in commits [`b430976`](https://github.com/sandeepbimt/Sandium/commit/b430976590588cac211dd3321a8459dfe5cabe85) and [`25f4347`](https://github.com/sandeepbimt/Sandium/commit/25f43470e9f383a53f2907092b7a5839c341316a). This is source-level work only. The latest no-build workflow outcome still needs explicit confirmation; there is no claim that a full build, remote action, or APK has been produced. The build gate remains false while state persistence and resource feasibility are unresolved.
