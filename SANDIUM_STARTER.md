# SANDIUM — Android Browser Project Charter

**Product:** SANDIUM Browser  
**Platform:** Android  
**Authoritative browser source:** [Bare Browser](https://github.com/BareBrowser/bare-browser)  
**Source boundary:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Status:** Source migration to Bare; preserve the existing Sandium integration.

## Mission

Build a polished, fast, privacy-conscious Android browser with real extensions and uBlock Origin, reliable PWA installation and standalone behavior, excellent dark-page rendering, and maintainable updates. Use Bare's patch-based Chromium source model as the only browser-source reference.

## Mandatory source boundary

- Bare Browser and the Chromium revision pinned by the selected Bare snapshot are the **only** permitted browser-source references for current and future work.
- Read [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md) first. It overrides older source-specific notes, scripts, pins and designs.
- Do not return to a superseded browser source or use its implementation, source-specific build scripts, patch machinery, Siso preset, pins or assumptions.
- If old source-specific content remains in historical logs, treat it as historical evidence only. Do not use it to design or debug the Bare build.
- Bare is a patch series, not a full Chromium checkout. Pin the Bare commit and its exact Chromium commit; apply the ordered patches reproducibly.

## Preserve the existing Sandium environment

The task is to replace the browser source, **not** to rebuild the integration.

- Reuse the existing Sandium GitHub repository, CircleCI integration/project, BuildBuddy account/endpoint, Siso setup, secret assignments, webhooks, permissions and cache configuration.
- Do not recreate projects, reassign or rotate tokens, reconnect integrations, create new contexts or clear caches.
- Keep credential values secret. Reuse the existing secret references. If a required setting is missing or inaccessible, stop and report its name; do not silently create a replacement.
- Keep old caches and checkpoints intact. Source-specific local checkpoints are not automatically compatible with Bare; preserve them and verify identity before any restore.
- Change only source-dependent checkout, patch application, Chromium revision, Siso backend generation, build command and artifact verification.

## Mandatory project separation

Sandium is independent from SANDFOX.

- Do not trigger or depend on SANDFOX workflows, credentials, caches, checkpoints, artifacts, source checkout or infrastructure.
- Do not modify SANDFOX infrastructure.
- Do not transplant its scripts or assume its cache/checkpoint behavior works for Sandium.

## Engineering method: DIRTFT

UNDERSTAND → MINIMAL CHANGE → TEST → LEARN → PRESERVE → PROCEED.

Inspect actual files and logs, distinguish verified facts from hypotheses, make the smallest justified change, inspect the diff, run one targeted validation, and preserve the result. No speculative commits or overlapping expensive builds.

## Resource and build gates

- No paid GitHub upgrade is planned.
- Do not assume full Chromium checkout/build fits a CI budget without evidence.
- Do not trigger Chromium sync, compilation or APK builds during source migration.
- Before any separately approved build, document exact source pins, ordered patches, dependencies, storage, memory, bandwidth, cache behavior, remote execution, expected runtime/cost, pass criteria and diagnostics.
- Do not start a build until the Bare source adapter, resource/persistence plan and no-build preflight have been reviewed and separate explicit build approval is recorded.
- Do not claim remote execution, resumability or cross-run reuse until logs prove it.

## Scope order

1. Read-only inventory of the existing integration and Bare source adapter requirements.
2. Static Bare source/configuration preflight with no Chromium sync or compile.
3. Prove the existing Siso/BuildBuddy path is configured for the Bare-pinned Chromium revision.
4. Explicitly approve one controlled baseline APK build.
5. Install and launch on a real Android device.
6. Verify navigation, extensions/uBlock, PWA behavior, dark rendering and performance.
7. Make carefully scoped Sandium UI, privacy and branding changes.
8. Maintain Bare/Chromium pins and patch compatibility through documented updates.

Every stage needs explicit pass criteria and retained evidence.

## Documentation and automation

The user is not expected to maintain project Markdown manually. Follow [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md); update the source-of-truth, decisions, experiments, failure learnings, build notes, status and handoff as evidence changes. Unknown facts stay UNKNOWN. Preserve history, label superseded decisions, and never store secrets. Documentation automation must never trigger a browser build.

## Definition of progress

Progress means reducing uncertainty with reliable evidence, preserving the existing working integration, producing a reproducible Bare-based Android browser, and avoiding wasted resources or source confusion.
