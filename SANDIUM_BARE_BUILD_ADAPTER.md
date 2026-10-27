# SANDIUM — Bare Source Adapter and Existing CI Integration

**Status:** Bare-only source preflight and adapter tooling committed on `migration/bare-source-adapter`; full build fails closed; five-stage workflow not wired; no build  
**Authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Existing infrastructure:** Reuse; do not recreate

## Source inputs

- Bare repository: https://github.com/BareBrowser/bare-browser
- Reviewed Bare commit: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`
- Chromium commit: `1228231501697ff7a4a0150ea8ae6df37bb99331`
- Chromium version: `156.0.8078.25`
- Target ABIs documented by Bare: `arm64` and `arm`; Android 10+; no x86 build.
- Bare's patch series is the product-specific delta. Keep the ordered patch list and its digest in every build manifest.

## Existing integration to retain

Use the existing Sandium GitHub repository and branch/workflow wiring, existing CircleCI project and configured contexts, existing BuildBuddy endpoint and instance, existing Siso integration, and existing secret names/values. Do not create a new project, rotate or reassign credentials, or clear any cache.

The Sandium record for GitHub Actions run [39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682) reports that an isolated Siso authentication check succeeded against `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`. This does not prove that CircleCI can read the same-named secret, nor that a build action executes remotely. Verify access without displaying values; if a setting is absent, stop and report its name rather than creating a replacement.

## Current implementation checkpoint

- Added [`ci/bare/prepare_source.sh`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/prepare_source.sh) on the migration branch. Its `inspect` mode fetches the pinned Bare patch repository and validates the Chromium pin/version, expected patch count/digest and uBlock CRX checksum without checking out Chromium. Its explicit `apply` mode requires an existing clean Chromium checkout at the exact pin and aborts a failed patch application. Bash syntax validation passed; the script has not been executed against source.

- Created [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter) as an isolated branch. Its active CircleCI config is now Bare-only: an opt-in source preflight plus a fail-closed full-build stub. The five-stage build is intentionally not wired until the account's persistence limits are proven.
- The previous five-stage config is retained in Git history/default branch only as historical state. Do not use it as implementation guidance. The migration branch's full-build workflow cannot run a build; it exits before source sync. The branch is not a build-ready pipeline.

- Modified `.circleci/config.yml` on branch [`ci/sandium-buildbuddy-siso-preflight`](https://github.com/sandeepbimt/Sandium/blob/ci/sandium-buildbuddy-siso-preflight/.circleci/config.yml), commit `851c944a714012118e0bb9406b3cb7414f437848`.
- The existing opt-in parameter name is preserved to avoid reconfiguring existing API triggers. The default remains `false`.
- The job fetches the pinned Bare patch repository and checks the Chromium pin, version, patch presence and ordered patch digest. It only checks that existing integration settings are present; it does not reveal the credential or alter settings.
- Static YAML parsing and `bash -n` validation passed using the fetched config content. This was not CircleCI server validation. The workflow has not been executed and no CircleCI pipeline was manually triggered; no Chromium sync, compile or APK build occurred.

## Implemented Bare-specific tooling

- [`source-pin.txt`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/source-pin.txt) pins the Bare commit, exact Chromium commit/version, ARM64 Debug target and Sandium artifact name.
- [`gn_args.gn`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/gn_args.gn) makes the intended Android ARM64/Siso GN settings reviewable and fingerprintable.
- [`write_cache_identity.py`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/write_cache_identity.py) computes a stable pre-build identity from the pinned Bare patch series, extension checksum, toolchain revision, GN arguments, backend configuration and credential-helper file; it never reads the API key.
- [`build_identity.py`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/build_identity.py) records and validates source/build identity independent of the CI commit SHA. APK acceptance requires ZIP integrity, Android manifest and DEX presence, a passing `apksigner` verification, and matching size/SHA-256.
- [checkpoint.py](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/checkpoint.py) binds a compressed Android output checkpoint to source/build identity and archive hash. It is not for CircleCI Free-plan storage; use only with an explicitly provisioned external/local store.
- [stage_ledger.py](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/stage_ledger.py) uses schema 2: Stage 1 records only stable source/toolchain identity and source/dependency readiness (it deliberately ignores any pre-existing GN fingerprint); Stage 2 establishes the generated GN/build-graph identity, Stage 3 requires actual uncached Siso remote execution, Stage 4 requires both a current-invocation remote-cache hit and additional uncached remote work, and Stage 5 independently verifies the packaged APK and signature. It binds a stable source/toolchain identity across the GN transition while separately pinning the generated GN-argument fingerprint. Siso progress counters remain stage-local.
- [package_artifact.sh](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/package_artifact.sh) copies the built APK to the Sandium artifact name and writes/validates the manifest and checksum.
- [`bootstrap_chromium.sh`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/bootstrap_chromium.sh) describes the source bootstrap path. Its full sync mode is fail-closed unless `SANDIUM_ALLOW_CHROMIUM_SYNC=true` is separately supplied. It has not been run.

The opt-in `sandium-bare-source-preflight` CircleCI workflow now includes script syntax checks, unit tests, pinned source metadata checks and extension checksum validation. It defaults off and has not been executed.

## Required source adapter behavior

- Added [`ci/bare/configure_siso.py`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/configure_siso.py) to inspect or write the existing BuildBuddy REAPI settings into the generated Chromium `.gclient` file. It uses the already configured endpoint/instance and existing credential-helper path, never reads or prints the API key, and does not run `gclient sync`, Siso or a build. Python syntax compilation and a local fixture test passed; no real `.gclient` file, credential, Siso process or build was used.

1. Resolve the exact Bare commit and verify the expected Chromium pin from that commit's build notes.
2. Check out the exact Chromium commit in the existing persistent source workspace. Do not run a source updater for any other browser project.
3. Fetch the patch series from the pinned Bare commit, verify patch count/order and compute a digest, then apply the ordered series with `git am`. Stop on any mismatch or patch conflict.
4. Provide the uBlock Origin CRX as the separately versioned/checksummed build input required by Bare. Do not put the binary in the patch series or log secrets.
5. Use Chromium's native Siso setup and the existing Sandium BuildBuddy REAPI endpoint, instance and authentication secret. Generate the backend configuration required by the pinned Chromium/Siso revision; verify the generated `.gclient` custom vars, `.sisoenv`, credential-helper path and runtime config.
6. Keep source checkout, patch application, dependency synchronization, GN generation, local-only actions, packaging and artifact verification as explicit phases. Remote execution only accelerates eligible actions; it does not remove the other phases.
7. Emit a manifest containing Bare SHA, Chromium SHA/version, patch digest, uBlock input digest/version, Siso revision, toolchain, target ABI, GN args, backend-config digest, build mode, artifact path, size and SHA-256.

## Do not carry over source-specific machinery

Do not use old source-specific package scripts, source pins, patch application commands, override directories, custom Siso presets or generated config assumptions. Bare is a patch series over Chromium; use its patch series and the Chromium revision it pins. Keep only infrastructure-level wiring that remains compatible: existing CircleCI orchestration, BuildBuddy service/authentication, Siso client path, secret references and cache configuration.

## Cache and checkpoint policy

The new cache-identity writer produces `.sandium-bare-cache-identity.txt` from the Bare commit, Chromium pin, ordered patch digest, extension checksum, toolchain revision, GN arguments, backend configuration and credential-helper file. Use it to bind stage ledgers and diagnostics to a stable source/build identity. Do not use CircleCI storage for the full Chromium source/output tree: CircleCI Free includes 2 GB storage and overage consumes credits ([official pricing](https://circleci.com/pricing/)). Preserve all existing cache objects; do not purge them or restore incompatible historical outputs. Prefer BuildBuddy/Siso's content-addressed remote action cache for cross-stage compile reuse, with the stage ledger proving real remote execution and cache hits. The full-output checkpoint helper is only for a separately provisioned external/local store, not CircleCI Free.

- Preserve all existing cache objects and checkpoints. Do not purge, rename or recreate the cache namespace during migration.
- A remote action cache may return valid hits only when the action key/input identity matches; prove useful hits for the Bare source.
- Existing local build outputs/checkpoints must not be restored unless a manifest proves exact source, Chromium pin, patch digest, toolchain, GN args and target compatibility.
- Use stable identity keys; never use only run IDs or timestamps.
- Record cache keys, restored state, action counts, local/remote/cache counters, elapsed time and output identity. A cache-hit label alone is not proof.
- A changed Bare or Chromium pin invalidates source-dependent state; it must not silently fall back to a previous source.

## No-build preflight pass criteria

- Existing GitHub/CircleCI/BuildBuddy/Siso integration identifiers and secret references are unchanged.
- No token value is printed, rotated, recreated or copied.
- Bare and Chromium pins match the pinned Bare source metadata.
- Patch order/count/digest and extension input are verified.
- Generated Siso/REAPI configuration points to the existing configured endpoint and instance, and uses the expected credential helper without exposing its output.
- YAML, shell and source-adapter checks pass without Chromium sync, GN generation, compilation or APK packaging.
- The run is explicitly identified as `FAST — BARE SOURCE PREFLIGHT`, and a full build is impossible unless separately enabled and approved.

## Known unknowns

- Whether the existing CircleCI context exposes every required secret under the same variable names.
- Whether the current BuildBuddy instance, executor image and cache namespace support Bare's exact Chromium/Siso pin.
- Whether the current runner has sufficient persistent source/build storage and runtime for the Bare workflow.
- Whether remote action execution and useful action-cache hits occur for this source.
- Whether a complete APK can be produced within current limits.

Do not resolve these unknowns by recreating the integration. Inspect the existing configuration and stop safely if access or compatibility is unproven.


## Progress accounting and reuse proof — 2026-10-27

A historical Stage 2 run rejected progress after adding a previous-stage baseline of 103,735 to a current-invocation Siso count of 55,453 against a normalized graph total of 109,040. The formula is invalid because a Siso/Ninja progress count is scoped to a build invocation/graph; stage counts are not a globally unique, disjoint set of actions. See [FAIL-LEDGER-002](SANDIUM_FAILURE_LEARNINGS.md#fail-ledger-002--stage-local-siso-progress-was-added-to-a-prior-stage-baseline).

- Active-branch fix: [`cce70d9`](https://github.com/sandeepbimt/Sandium/commit/cce70d9028ac1662e1a3a22e40fcbb4ca53c140c) adds `action_count_scope=STAGE_LOCAL_ONLY_NOT_CUMULATIVE` and retains exact identity plus per-stage Siso remote/cache evidence checks.
- Regression suite: [`test_stage_ledger.py`](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/test_stage_ledger.py) checks structured metrics, summary parsing, that endpoint text is not proof, current-stage cache-hit requirements, and the no-summation invariant.
- The no-build workflow [`d89423f`](https://github.com/sandeepbimt/Sandium/commit/d89423fbaf32bbe30ed6d87bb491a328b727c2f7) runs only Python tests and shell syntax; no Chromium sync/build steps are present.
- Do not weaken graph-total or identity checks to make the old run green. For this migration, stage-local progress is diagnostic only; continuation must be proved by source identity/ledger linkage and current-stage Siso remote-cache/action metrics.
- No-build workflow [40442432290](https://github.com/sandeepbimt/Sandium/actions/runs/40442432290) passed stage-ledger/source-identity tests and shell syntax checks. It explicitly confirmed no Chromium sync, GN generation, Siso build or APK build. Full-build readiness remains disabled.


## Source-only five-stage feasibility review — 2026-10-27

### Corrected source-bootstrap sequence

The source adapter review found that `bootstrap_chromium.sh` still invoked `fetch --nohooks android`, despite the prior status note saying the source fetch was pin-first. That command can perform an initial dependency sync before the explicit Chromium pin is enforced. Commit [`952eb6f`](https://github.com/sandeepbimt/Sandium/commit/952eb6f0b3b6eea206b250b954d7f44a2b4d02db) now configures `.gclient` first, writes the existing Sandium Siso settings, fetches the exact Chromium commit directly, verifies HEAD, performs a bounded/logged dependency sync against that pin, and verifies HEAD again. No network bootstrap or build was run by this code change. The no-build regression suite passed in [run 40443430796](https://github.com/sandeepbimt/Sandium/actions/runs/40443430796).

### Blockers before wiring the five jobs

1. **Ledger responsibility mismatch — corrected in source, not yet integrated to a build workflow:** schema 2 now maps evidence to the stage that can produce it and separates stable source/toolchain identity from the generated GN fingerprint. Stage 3 must prove an uncached remote action, Stage 4 must prove a current-stage remote-cache hit, and Stage 5 rechecks the artifact directly with the APK verifier. The updated unit tests cover these rules. A passing CI result must be checked before claiming the test suite is green; the pipeline is still not wired.
2. **Source/output persistence:** Bare's current build instructions state that the Chromium checkout is about 50 GB, at least 100 GB free disk is required, and the builder VM should have 32 GB allocated. CircleCI's cache documentation says caches are immutable per key and large restores have material transfer/expansion costs; CircleCI Free's included storage allowance is much smaller than the Chromium source tree. Do not use a full source/output archive as the default handoff.
3. **No persistent source store has been proven:** CircleCI workspaces can pass data between jobs in a workflow but do not, by themselves, provide a reusable source checkout across future workflows. BuildBuddy/Siso remote action cache evidence proves reuse of compatible action results; it does not establish that a later CircleCI job has a local Chromium checkout and generated build graph available. Re-fetching and reconstructing those inputs in every stage would undermine the current runtime target and has not been measured.

**Conclusion:** the current five-stage plan is **not yet demonstrated feasible under the existing constraints**. Keep the build gate false. Do not wire a workflow that would silently re-sync Chromium or claim continuation from a ledger alone.


## Stage-ledger contract redesign — 2026-10-27

The source-only implementation now defines a stage-specific evidence contract in [stage_ledger.py](https://github.com/sandeepbimt/Sandium/blob/migration/bare-source-adapter/ci/bare/stage_ledger.py), schema 2:

1. **Stage 1 — source/dependency readiness:** requires a positive source-preparation/cache marker and a pinned source identity. It does not invent Siso compile evidence.
2. **Stage 2 — toolchain/build-graph readiness:** requires generated GN arguments and the Ninja graph. It establishes the GN fingerprint separately from the stable source/toolchain identity; Stage 1 explicitly records no GN fingerprint, even if partial/stale GN files happen to exist.
3. **Stage 3 — remote compilation:** requires at least one uncached remote Siso action in that invocation.
4. **Stage 4 — cache-backed continuation:** requires both at least one current-invocation remote action-cache hit and at least one additional uncached remote action in that same invocation; this prevents a cache-only stage from being mistaken for forward progress.
5. **Stage 5 — artifact gate:** requires the same identity/GN fingerprint, the prior remote/cache chain, a matching build manifest, and direct APK structure and `apksigner` verification. Manifest status strings alone are not accepted as proof.

Every stage must link to the immediately preceding stage ledger and preserve source identity; generated GN identity may be established at Stage 2 and must then remain identical. Current implementation commits include [`7307a08`](https://github.com/sandeepbimt/Sandium/commit/7307a08495facb2d5e2fd1be302d9d74157184b3), [`05aa490`](https://github.com/sandeepbimt/Sandium/commit/05aa490da9d02ec97b30565f27224f5c0a096538), stable identity fix [`a344207`](https://github.com/sandeepbimt/Sandium/commit/a344207e970e43562397067d14a9c01c87190be8), and regression test [`440aaa9`](https://github.com/sandeepbimt/Sandium/commit/440aaa98980e498d5bea551d0097a51fac68f31f). Invocation-local Siso counts are never summed into a synthetic cumulative action count. The test suite was expanded to check stage-role requirements, GN identity continuity, source/graph/artifact evidence, and the no-summation invariant.

**Scope limitation:** these changes correct the ledger contract only. The CircleCI five-stage jobs remain unwired, no source/output persistence mechanism has been proven for the current account, and the full-build gate remains false. No Chromium sync, GN generation, Siso compilation or APK build was run for this change.
