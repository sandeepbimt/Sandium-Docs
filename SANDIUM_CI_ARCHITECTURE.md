# SANDIUM — Bare-Based CI Architecture

**Status:** Migration design; not build-ready  
**Authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Migration branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)

## Core rule

Preserve the existing Sandium GitHub, CircleCI, BuildBuddy and Siso integration. Change only the source-dependent adapter and identity data. Do not recreate credentials, contexts, projects, webhooks or cache configuration.

Bare is the only active browser source. The pinned Bare commit declares the Chromium commit to use. The ordered patch series, not a second browser source tree, defines the product-specific changes.

## Existing workflow safety

The migration branch's active config is now Bare-only: an opt-in source preflight plus a fail-closed full-build stub. The five-stage compile/restore/publish workflow is not yet wired because persistent source/output storage under the existing CircleCI account has not been proven. The prior workflow remains only in Git history/default branch and must not be used as current source guidance.

## Five-stage responsibilities

1. **Source foundation:** validate the pinned Bare commit and Chromium pin; restore only compatible source state; checkout/sync the exact Chromium revision; apply the ordered patch series and verify the extension input.
2. **Toolchain and graph:** reuse or generate the pinned toolchain/hooks/GN/Siso configuration for this exact source identity; verify required GN args and backend settings.
3. **Compile/checkpoint:** execute only outstanding build-graph actions; capture Siso/BuildBuddy evidence; persist compatible state and diagnostics.
4. **Restore/continue:** verify source/config identity and checkpoint integrity, then run only remaining actions. Never resume from incompatible source-specific output.
5. **Finalize/verify/publish:** complete remaining required actions, verify the APK and signing/integrity metadata, persist the artifact and evidence manifest.

Each stage must have explicit inputs/outputs and prove forward progress. A stage must not repeat completed work unless its inputs changed or state is invalid.

## Current Bare adapter implementation

The migration branch now includes `ci/bare/source-pin.txt`, `gn_args.gn`, `prepare_source.sh`, `configure_siso.py`, `write_cache_identity.py`, `build_identity.py`, `checkpoint.py`, `bootstrap_chromium.sh`, and `package_artifact.sh`. The no-build preflight is opt-in and defaults off. These scripts are not yet wired into five compile stages because the existing account's ability to persist the full Chromium source and output state has not been proven. Keep `run_sandium_bare_source_ready=false`.

## Reuse and performance requirements

- Preserve the existing remote-execution endpoint, instance, protected credential assignment, cache namespace and CircleCI project.
- Preserve all cache data; do not purge or reset the cache.
- Use Bare-specific stable source identity in cache keys/manifests: Bare SHA, Chromium SHA, patch digest, extension digest, toolchain/Siso revision, target ABI, GN args and backend config.
- A remote action cache can be shared only where action keys are genuinely compatible. Old local build output/checkpoints are not assumed compatible with Bare.
- Record local/remote/cache action counts, cache lookup/hit/miss evidence, per-stage timing, source identity, resource use and artifact hashes.
- A verified matching APK should be persisted before downstream stages skip work. A later identical run may fast-skip only after validating the artifact manifest and checksum.
- Keep the existing five-stage structure; do not introduce artificial stage splits or a new build service just to accommodate the source migration.

## Required gates

1. Read-only inspection of existing integration and secret references.
2. Static source adapter and config validation; no Chromium sync or compile.
3. Verify generated Siso/REAPI configuration against the exact Chromium revision.
4. Controlled remote action with explicit approval; prove actual remote execution.
5. One controlled APK build only after source, storage, runtime and cost gates pass.
6. Verify APK integrity and install/smoke-test on a real Android device before accepting a clean base.

## Definition of ready

The source-ready flag may be enabled only after all source-specific commands, source/cache manifests, checkpoint paths, artifact names, tests and evidence recording are Bare-compatible. A successful authentication check is not enough. Do not claim remote execution, cache reuse, resumability or a clean base without matching evidence.

No build is authorized by this document.
