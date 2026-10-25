# SANDIUM — Authoritative Source Boundary

**Effective:** 2026-10-25  
**Status:** ACCEPTED — governs all future Sandium work  
**Product:** SANDIUM Android browser  
**Only browser source of truth:** [Bare Browser](https://github.com/BareBrowser/bare-browser)  
**Bare source pin reviewed:** `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`  
**Chromium pin declared by that Bare snapshot:** `1228231501697ff7a4a0150ea8ae6df37bb99331` (`156.0.8078.25`)

## Non-negotiable rule

From this decision onward, all Sandium source investigation, implementation, patches, source pins, build instructions, debugging and future recommendations must use **Bare Browser and the Chromium revision pinned by the selected Bare snapshot**. Do not consult, compare against, derive code from, or return to any superseded browser-source choice. If a future record, code comment, workflow, cache manifest or ChatGPT handoff conflicts with this file, stop and follow this file until a newer explicit source decision is committed.

Do not silently switch source because an old script, cache, workflow or note points elsewhere. Treat such material as stale migration residue and adapt or disable it. Do not use old-source-specific package scripts, patch handlers, build presets, source pins or assumptions as technical guidance for Bare.

## Preserve the existing integration

This is a source migration inside the existing Sandium environment, not an infrastructure rebuild.

- Keep the existing Sandium GitHub repository, CircleCI project/integration, BuildBuddy account/endpoint, Siso integration, secret names/values, project/context assignments, webhooks and permissions.
- Do not create a new CircleCI project, regenerate/rotate/reassign tokens, recreate contexts, reconnect GitHub, or change BuildBuddy organization settings just to accommodate the source migration.
- Do not print or store credentials. Reuse existing secret references as-is. If a required value is unavailable, stop and report the exact missing *setting name* without asking to recreate it by default.
- Keep existing caches and stored state intact. Do not delete, rename or clear them during source migration.
- Existing source-specific checkpoints and local build outputs are not automatically compatible with Bare. Preserve them, but do not restore or consume them unless the source/pin/config identity is proven compatible.
- Keep the existing remote execution/cache integration, but replace only source-dependent configuration. Bare uses a patch series over Chromium; source preparation and Siso configuration must be adapted to that model.
- Do not trigger a full build during source migration. No expensive sync, compilation or APK job without a separate, explicit approval after a no-build preflight.

## Verified source facts

- Bare is a patch series, not a full Chromium source checkout.
- The inspected Bare snapshot identifies Chromium commit `1228231501697ff7a4a0150ea8ae6df37bb99331`, version `156.0.8078.25`.
- Bare's build notes apply the ordered patch series with `git am` and package its separately maintained uBlock Origin CRX as an input outside the patch series.
- Bare's published local builder uses Docker and a persistent source volume. It is not proof that its local builder can be transplanted unchanged into CircleCI.
- The existing Sandium records show a successful isolated Siso authentication check against `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`, in GitHub Actions run [39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682). This proves authentication for that check only—not CircleCI secret visibility, remote action execution, cache reuse or APK production.
- Existing CircleCI and BuildBuddy settings must be reused, not re-created. Their current values must be read from the already-configured services without exposing secret contents.

## Active migration branch

- Canonical work branch: [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter). It is isolated from the default branch.
- Its active CircleCI config is Bare-only: the source preflight is opt-in/default off, and the full-build workflow is fail-closed. No five-stage build is enabled.
- The separate [`ci/sandium-buildbuddy-siso-preflight`](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight) branch is an earlier source-metadata prototype; use the canonical migration branch for current adapter work.
- Historical build branches are not valid current source guidance. Do not enable a workflow on any branch until the Bare source boundary and pin checks pass.

## Required migration order

1. Read this file and [SANDIUM_STARTER.md](SANDIUM_STARTER.md) before any Sandium task.
2. Inspect current GitHub/CircleCI/BuildBuddy/Siso wiring read-only. Record existing project IDs, secret *names* (never values), endpoint, instance, cache namespace and configuration paths.
3. Design a Bare source adapter that uses the existing integration. It must fetch the pinned Bare patch series, check out the exact Chromium revision, apply patches deterministically, provide the bundled extension input, and generate Chromium-native Siso/REAPI configuration for the existing BuildBuddy service.
4. Preserve infrastructure credentials and cache namespaces. Do not reuse source-specific local checkpoints without a matching identity manifest. Keep cache entries; let correct source/action keys determine valid reuse.
5. Validate the source adapter, generated configuration and YAML/shell syntax without Chromium sync or compilation.
6. Only after the no-build preflight is reviewed may a separate build be explicitly approved.

## Cache identity requirements

At minimum, a build/cache manifest must include Bare repository commit, Chromium commit, ordered patch-series digest, target ABI, toolchain/Siso revision, GN arguments, backend configuration digest and build mode. A changed source identity must not claim to resume an old local build checkpoint. Preserve remote action-cache configuration and namespace; prove useful hits for the new source rather than assuming them.

## Current single next action

Continue the migration on [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter). Before implementing five compile stages, prove a compliant persistence path for the Chromium source and build output using the existing CircleCI account. Keep `run_sandium_bare_source_ready=false`; do not run a pipeline or browser build.
