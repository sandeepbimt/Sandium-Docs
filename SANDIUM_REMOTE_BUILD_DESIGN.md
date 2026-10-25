# SANDIUM — Bare + CircleCI + BuildBuddy + Siso Remote Build Design

**Status:** Source adapter in progress; all build workflows remain gated  
**Authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Active migration branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)

## Source identity

- Bare repository: https://github.com/BareBrowser/bare-browser
- Reviewed Bare commit: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`
- Chromium commit: `1228231501697ff7a4a0150ea8ae6df37bb99331`
- Chromium version: `156.0.8078.25`
- Bare is an ordered patch series over Chromium Desktop Android, not a complete Chromium source checkout.
- Source preparation must fetch the pinned Bare commit, verify its Chromium pin, check out that exact Chromium revision, apply the ordered patches, and supply the separately versioned/checksummed uBlock Origin CRX input.

## Preserve existing integration

Do not create or reconnect any project, account, context, webhook or credential. Reuse the existing Sandium GitHub repository, CircleCI project/integration, BuildBuddy endpoint/instance, protected `BUILDBUDDY_API_KEY` assignment, Siso integration and cache configuration.

The existing recorded endpoint/instance are `remote.buildbuddy.io:443` and `sandium/android-arm64/ci`. The existing GitHub Actions authentication check passed in [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682). That result proves only the isolated authentication check; it does not prove CircleCI secret visibility, remote action execution, useful cache hits or APK production.

If an existing secret or setting is inaccessible, report its name and stop. Do not rotate, recreate or reassign it. Never print a credential.

## Architecture

- **CircleCI:** retain the existing project and five-stage orchestration; use it for source preparation, validation, dependency/toolchain setup, GN generation, packaging, evidence and artifact handover.
- **Bare:** the pinned patch series and build/version instructions.
- **Chromium/depot_tools:** checkout and dependency graph at the exact revision declared by the pinned Bare snapshot.
- **Siso:** use the Siso version and configuration contract from that exact Chromium revision. Do not hardcode a Siso version from an older source workflow.
- **BuildBuddy:** keep the existing REAPI service, endpoint, instance and authentication assignment. Adapt the generated Chromium-native Siso/REAPI configuration to the pinned Chromium revision.
- **Remote execution:** enable only after the generated config is verified and a meaningful action proves it. A successful auth check is not proof of remote execution.
- **Cache:** preserve the existing cache service and namespace configuration. Use new source-identity keys/manifests for Bare; do not restore old source-specific build outputs or checkpoints without exact identity compatibility proof.

## Source adapter requirements

1. Resolve Bare commit and Chromium commit from the pinned source; fail closed on any mismatch.
2. Compute and record the ordered patch count and digest.
3. Verify the Chromium checkout is exactly the pinned commit and clean before applying patches.
4. Apply patches in deterministic filename order with the documented patch-series mechanism; stop on any conflict or already-applied ambiguity.
5. Supply the expected uBlock Origin CRX as a separately versioned/checksummed input.
6. Generate Chromium-native `.gclient` REAPI variables and the credential-helper configuration using existing settings. Inspect generated `.sisoenv` and runtime flags before any remote action.
7. Ensure the build arguments explicitly select the intended Siso/remote-execution path and do not accidentally select a Google-only remote-execution preset.
8. Keep source checkout, hooks, GN generation, local-only actions, compilation, packaging and verification as separate measured phases.
9. Record Bare SHA, Chromium SHA/version, patch digest, extension digest, toolchain/Siso revision, target ABI, GN args, backend config digest, artifact identity and cache evidence.

## Cache/checkpoint policy

- Preserve existing cache objects and settings; do not clear them.
- Existing source checkout and local output checkpoints are not presumed compatible with the Bare source identity.
- Reuse content-addressed remote action results only when action inputs and toolchain identity match; prove useful hits with Siso counters/logs.
- Use stable identity keys containing Bare commit, Chromium commit, patch digest, target, toolchain/Siso revision, GN args and backend-config digest.
- Do not key by only branch, run ID or timestamp.
- Reject incomplete, stale, corrupt or mismatched checkpoints. A cache hit, archive restore or green job alone is not proof of useful reuse.

## No-build gates

The migration branch has `run_sandium_bare_source_ready=false`. Keep it false until every source-dependent command, test, cache key, checkpoint path, artifact name and verification rule has been adapted and reviewed.

Before a build is considered:
- validate YAML and shell syntax;
- verify Bare and Chromium pins and patch digest;
- inspect the actual generated Siso configuration without compiling;
- prove the existing secret references and endpoint/instance are unchanged;
- establish storage, runtime and cost from existing account configuration;
- obtain explicit approval for one controlled build.

No Chromium sync, GN generation, compilation, APK packaging or CircleCI pipeline was run as part of this design update.
