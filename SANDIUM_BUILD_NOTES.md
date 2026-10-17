# SANDIUM — Reproducible Build Notes

## Current status

No Sandium Android build has been run. Do not treat SANDFOX pins, commands, outputs or credentials as a Sandium baseline.

## Source pins

- Brave Core URL / exact commit:
- Brave Android URL / exact commit or tag:
- Chromium revision resolved by that Brave revision:
- Sandium patch-set commit:
- Dependency synchronization method:
- Pin date and rationale:
- Security/update strategy:

## Environment

- Runner/provider/image and architecture:
- OS:
- CPU / RAM / free disk:
- Git / Python / Node / package manager:
- JDK / Android SDK / NDK / build tools:
- GN / Ninja / Siso versions:
- BuildBuddy endpoint/instance identifier (never credentials):
- Remote execution availability, quota and pricing:

## Reproducible procedure

Only add commands verified against the selected source revision. For each, document working directory, purpose, expected output and diagnostics.

1. Preflight:
2. Source checkout and dependency sync:
3. Toolchain setup:
4. Build graph generation:
5. Build command/target:
6. APK path and integrity verification:
7. Install and smoke test:

## Cache and checkpoint contract

For each layer record purpose, identity key, stored paths, source/config compatibility checks, Siso state/journal behavior, required file metadata, archive size, pack/transfer/restore time, hit evidence, forward-progress evidence, invalidation, retention, cost and recovery.

Distinguish source/dependency reuse, remote action cache, runner-local cache, serialized checkpoint archive and same-workflow workspace. A cache-hit count alone is not proof of successful resume.

## Resource measurements

| Experiment / run | Checkout + deps | Peak disk | Peak RAM | Runtime | Archive size | Restore time | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Not measured | — | — | — | — | — | — | No Sandium build run |

## Artifact contract

Record source/config identity, workflow run, artifact path, size, SHA-256, archive integrity, signing/debug state and device install/smoke test. Never commit signing keys or secrets.

## Official source feasibility findings (2026-10-17)

- Brave's official Android development guide documents dependency installation followed by `pnpm run sync --target_os=android` and `pnpm run build --target_os=android`. For a debug APK it documents `pnpm run build Debug --target_os=android --target_arch=arm --target_android_output_format=apk`. These are source-documented commands, not yet executed in Sandium.
- Brave's `brave-core` README says initialization downloads Chromium source and can take a long time; its general build note says builds may take hours depending on processor and memory.
- Chromium's official Android build guide states Linux x86-64, at least 8 GB RAM, more than 16 GB RAM highly recommended, and at least 100 GB free disk. These are Chromium minimum/recommendation figures, not a promise that a constrained hosted runner can complete a Brave build.
- Chromium documents Siso as the main build tool and `autoninja` as its build wrapper. Remote execution is configured with `use_remoteexec = true` in Chromium GN args, but this alone does not establish free remote-execution access, correct credentials, reusable checkpoints, or a working Brave build.
- Source references: [Brave Android Development Environment](https://github.com/brave/brave-browser/wiki/Android-Development-Environment), [Brave Core README](https://github.com/brave/brave-core/blob/master/README.md), [Chromium Android build instructions](https://chromium.googlesource.com/chromium/src/+/main/docs/android_build_instructions.md).

### Feasibility conclusion

The documented build path is clear; the affordable execution environment is not. No Sandium build should start until a pinned source revision is verified against its Chromium DEPS pin, and a free/persistent Linux x86-64 builder with sufficient storage and RAM plus a validated remote-build/cache entitlement is identified. The exact Brave Core pin was re-verified on 2026-10-17 against Sandium master: commit `06cd65a7e4fcea784e73c6deb9e4ce52889dc710`, package version `1.100.10`, Chromium pin `156.0.8078.39`. Re-read these files and capture the actual checkout SHA before implementation; branch master is mutable.


## CircleCI + BuildBuddy + Siso architecture review (2026-10-17)

- Source inspection confirms Brave Core has its own native Siso/REAPI path. config.ts reads rbe_service, use_remoteexec, and siso_cache_dir; when rbe_service is set, generated Chromium custom vars default to reapi_address, reapi_instance=default, and reapi_backend_config_path=google.star before project custom-var overrides are merged.
- A Sandium-owned BuildBuddy backend path must explicitly override google.star. Brave's sisoUtils.ts also automatically adds -config googlechrome when rbe_service is set. This is a revision-specific integration risk to validate, not assume correct or remove speculatively.
- The build option --use_remoteexec true exists and remote execution defaults off. Preserve opt-in behavior; do not enable RBE globally.
- SANDFOX's saved Chromium M151 proof demonstrated one real remote C++ action, but its counters reported cache:0. It does not prove remote-cache hits, reusable checkpoints, the pinned M156 source, or full APK production.
- CircleCI should orchestrate and host the source workspace; BuildBuddy executes eligible remote actions. Remote compilation does not remove dependency sync, GN generation, local-only actions, packaging or device tests.
- A Sandium-specific BuildBuddy API key and independently verified instance/cache namespace are required. A new key alone does not prove cache isolation. Do not reuse SANDFOX credentials, cache entries, checkpoints, artifacts, or workflows.
- CircleCI currently documents a one-hour maximum job on the Free plan. Resource class, disk/RAM headroom, credits and source/artifact storage need account-level verification. Do not copy SANDFOX's artificial 35/36-minute timeout.
- Detailed design and rollout gates: [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md). No build or CI workflow has been executed.
- A disabled-by-default, no-build CircleCI preflight was staged on [branch ci/sandium-buildbuddy-siso-preflight](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight), commit 3610ff348694d9cf923dbcffaf633017fade4edc. It contains .circleci/config.yml and ci/siso/buildbuddy_backend.star. Local YAML and bash syntax checks passed; CircleCI server-side validation and execution are not established. It has no source sync or build job and its workflow parameter defaults false. The preflight only checks metadata and presence of environment variables; it does not contact BuildBuddy or prove key validity/cache isolation.


## Documentation automation boundary

The recordkeeper is a metadata/documentation workflow only; it must never check out or compile Brave, sync Chromium dependencies, or trigger browser CI. Its successful execution is not a browser build result and must not qualify as a clean base. No Sandium Android build or APK has been produced as part of this documentation work. End-to-end recordkeeper execution remains unverified; see [automation rules](SANDIUM_AUTOMATION_RULES.md) and [experiment EXP-AUTO-001](SANDIUM_EXPERIMENT_LOG.md).

## Pinned non-Google REAPI investigation (2026-10-17)

- Chromium pin 156.0.8078.39 declares reapi_address, reapi_instance, reapi_backend_config_path and reapi_credential_helper and pins Siso to c574896b272b40aac6e44c228ee0b471ea7e3d7d. DEPS passes these settings to configure_siso.py. The official non-Google RBE guide documents a custom backend.star, host:port address, namespace, helper, and a digest-pinned siso-chromium container image.
- BuildBuddy's documented REAPI endpoint candidate is remote.buildbuddy.io:443; its Bazel example uses grpcs://remote.buildbuddy.io. The proposed stable instance string is sandium/android-arm64/ci. Neither endpoint authentication nor this instance's acceptance has been tested against the Sandium account.
- Brave config.ts overlays projects_chrome_custom_vars after its Google defaults. The .env prefix mechanism can override reapi_address, reapi_instance, reapi_backend_config_path and reapi_credential_helper. The recommended value for the backend path is relative to Chromium's backend_config directory: ../../../../brave/ci/siso/buildbuddy_backend.star, assuming the workspace has Chromium in src and Sandium in src/brave.
- Image candidate documented in Chromium's non-Google RBE guide and the pinned chromium revision: docker://gcr.io/chops-public-images-prod/rbe/siso-chromium/linux@sha256:d7cb1ab14a0f20aa669c23f22c15a9dead761dcac19f43985bf9dd5f41fbef3a. BuildBuddy custom container-image support is documented, but account image pullability and action compatibility remain untested. Do not copy Google-specific action_default/action_large labels.
- BuildBuddy auth uses x-buildbuddy-api-key. A credential helper using the standard get / JSON stdin / JSON headers protocol is feasible in principle; exact pinned-Siso compatibility and runtime execution remain unverified. The key must only be stored as a protected CircleCI secret and never in .env or source.
- CircleCI workspaces transfer persisted data only within one workflow (15-day max on CircleCI Cloud); cache retention max is 15 days and large caches cost time to restore. Official Chromium docs report roughly 30 GB for its Git cache and about 30 minutes for a fast fetch. Therefore the full five-stage source/state handoff remains a capacity risk until Git-cache restore, worktree materialization, Siso checkpoint and transfer times are measured. Do not archive the full source tree by default.
- The review branch making -config googlechrome opt-in remains unmerged. Keep the option false for initial connection/action qualification, then test the broader preset separately before enabling it for BuildBuddy.
- No .env generation test, Siso auth-check, REAPI request, source sync, CI run, compile or APK build was performed in this investigation.
- Sources: [Chromium pinned DEPS](https://chromium.googlesource.com/chromium/src.git/+/8a02fdbdfd14beedbb001c49e39d4d8666488921/DEPS), [Chromium non-Google RBE guide](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#non-Google-RBE), [BuildBuddy RBE setup](https://www.buildbuddy.io/docs/rbe-setup/), [BuildBuddy auth](https://www.buildbuddy.io/docs/guide-auth/), [Credential Helper spec](https://github.com/EngFlow/credential-helper-spec/blob/main/spec.md), [CircleCI workspaces](https://circleci.com/docs/guides/orchestrate/workspaces/), [CircleCI cache guide](https://circleci.com/docs/guides/optimize/caching/).
