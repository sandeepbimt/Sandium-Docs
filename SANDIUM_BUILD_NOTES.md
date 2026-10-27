> **SOURCE BOUNDARY — 2026-10-25:** Current browser source is Bare Browser only. Read [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md) before interpreting this historical record. Older source-specific experiments, pins, cache identities and build assumptions are superseded; preserve them as history but do not reuse them as current technical guidance. The existing Sandium GitHub/CircleCI/BuildBuddy/Siso integration and credential assignments must be preserved. Do not clear caches or trigger builds during source migration.

---

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
- Detailed design and rollout gates: [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md). A lightweight CircleCI preflight attempt did execute but failed before BuildBuddy access because SANDIUM_REAPI_ADDRESS was unset at that time. No Chromium source sync, compile or APK build has run.
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
- Local .env generation and the pinned configure_siso.py path were tested in a temporary offline workspace as recorded below. No Siso auth-check, REAPI request, source sync, CircleCI browser-build/preflight, compile or APK build was run. Documentation-only GitHub Actions validation is separate from browser build work.
- Sources: [Chromium pinned DEPS](https://chromium.googlesource.com/chromium/src.git/+/8a02fdbdfd14beedbb001c49e39d4d8666488921/DEPS), [Chromium non-Google RBE guide](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#non-Google-RBE), [BuildBuddy RBE setup](https://www.buildbuddy.io/docs/rbe-setup/), [BuildBuddy auth](https://www.buildbuddy.io/docs/guide-auth/), [Credential Helper spec](https://github.com/EngFlow/credential-helper-spec/blob/main/spec.md), [CircleCI workspaces](https://circleci.com/docs/guides/orchestrate/workspaces/), [CircleCI cache guide](https://circleci.com/docs/guides/optimize/caching/).


## Offline source-adapter validation (2026-10-17)

- **Review branch:** [review/sandium-buildbuddy-backend-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/sandium-buildbuddy-backend-2026-10-17), final patch commit 806f565ea44e256344f05cafe1b2b80b577aecfc. Compared with master, the branch is four commits ahead, zero behind; the diff contains only two previously reviewed Siso source edits and four new adapter/test files. There is no PR and no merge.
- **Files:** ci/siso/buildbuddy_backend.star; ci/siso/buildbuddy-credential-helper.py; ci/siso/write_buildbuddy_env.py; tests/ci/test_siso_buildbuddy_config.py. Runtime settings are placed in the ignored Brave Core .env; the helper key is read from BUILDBUDDY_API_KEY and is not written to .env or logged.
- **Offline tests:** 14 standard-library unittest cases passed after tightening one assertion that initially matched an explanatory comment rather than a configured Starlark property. Tests use fake values only.
- **Pinned config check:** exact Chromium 156.0.8078.39 configure_siso.py blob SHA cb0ce6aadd79bf1e0fa88f3da6b0b82ffee366e5 was copied to a temporary minimal workspace; its Git blob hash matched the upstream source. It generated SISO_REAPI_INSTANCE=sandium/android-arm64/ci, SISO_REAPI_ADDRESS=remote.buildbuddy.io:443 and the absolute SISO_CREDENTIAL_HELPER path, then copied backend.star byte-for-byte. No Chromium checkout or toolchain was needed.
- **Environment:** local temporary Linux workspace and Python standard library; no BuildBuddy secret, network request, Siso executable, gclient, GN, source sync, compile or APK build. This validates configuration generation only, not Brave EnvConfig integration, Siso helper protocol at runtime, remote execution, cache isolation, executor image pullability or speed.
- **First test failure / fix:** an assertion searched for the raw text label:action_default, which also appeared in a comment. The backend comment was made descriptive without the literal property string and the assertion was narrowed to quoted property syntax. The corrected suite passed 14/14. See FAIL-SISO-001.
- **Next gate:** separate explicit approval for the pinned Siso auth-check against BuildBuddy. Do not run it, start CI, or begin compilation until that gate is approved.


## Siso auth workflow bootstrap failure (2026-10-17)

- Isolated workflow: [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682), Sandium branch `review/sandium-buildbuddy-backend-2026-10-17`, workflow commit `dea3e5ee0b214098117d26c823fc32c080022f4d`.
- Attempt 1 stopped because the GitHub Actions secret `BUILDBUDDY_API_KEY` was absent. User confirmed the secret was added; attempt 2 was started.
- Attempt 2 passed checkout but failed in Siso installation: `Error: no such package: infra/tools/siso/linux-amd64`. The auth-check step was skipped; no BuildBuddy authorization result exists.
- Next: verify the pinned Siso revision's exact CIPD package/install method from authoritative Chromium/Brave source and package metadata, correct the workflow minimally, and rerun only the auth-only workflow.
- No Chromium sync, GN, compilation, APK build, or SANDFOX operation occurred. See EXP-SISO-002 and FAIL-SISO-002.


## Historical Stage 2 accounting failure — 2026-10-27 (not an accepted build)

The uploaded CircleCI build #657 log on historical branch `build/bare-apk-once-20261025` records a restored Stage 1 output checkpoint (11,320,374,898 bytes) and then a Stage 2 ledger rejection: previous baseline 103,735 plus current invocation progress 55,453 exceeded normalized total 109,040. The failure is in cumulative progress accounting; it does not establish a compiler error or prove complete action-cache reuse. No verified APK was produced.

The corrective source change is on the authoritative Bare migration branch, commit [`cce70d9`](https://github.com/sandeepbimt/Sandium/commit/cce70d9028ac1662e1a3a22e40fcbb4ca53c140c). Its regression tests are run by a no-build GitHub Actions workflow. Preserve the existing CircleCI caches and credentials; do not rerun the historical workflow. Current Bare build readiness remains closed, and no full build was launched for this fix.
