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
