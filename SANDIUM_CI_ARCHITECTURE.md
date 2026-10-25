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

The migration branch now includes source pins, GN args, source preparation, Siso configuration, cache identity, build identity, checkpoint, stage-ledger, guarded bootstrap and artifact packaging scripts. The no-build preflight is opt-in and defaults off. The five compile stages must use remote action-cache reuse and small ledgers rather than CircleCI storage for the full source/output tree. Keep the full-build gate false until remote execution/cache behavior is proven.

## Storage and cross-stage reuse strategy

CircleCI official Free-plan pricing currently includes 2 GB of storage; storage beyond the included allowance consumes credits. Public open-source projects may qualify for up to 400,000 credits/month, but this account's eligibility is unverified ([pricing](https://circleci.com/pricing/), [persisting data](https://circleci.com/docs/guides/optimize/persist-data/)). Do not upload the full Chromium checkout or output tree to CircleCI caches/workspaces. Each stage should recreate the exact pinned source/build graph and use the existing BuildBuddy/Siso remote action cache to recover completed action outputs. Persist only small stage-ledger JSON and diagnostic summaries through CircleCI workspaces/artifacts. This strategy is viable only if a controlled test proves useful cache hits and real remote execution.

The full-output checkpoint helper can create a compressed output archive, but do not use it for CircleCI Free-plan persistence; reserve it for an explicitly provisioned external/local store. The intended CircleCI stage-to-stage proof is the small source-bound stage ledger, which requires Siso remote-execution/cache metrics.

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
