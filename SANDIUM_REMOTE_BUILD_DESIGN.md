# SANDIUM — CircleCI + BuildBuddy + Siso Remote Build Design

**Status:** Proposed design; disabled-by-default preflight configuration staged on a Sandium branch. CircleCI project/context is not configured or validated, and no browser build has run.
**Reviewed:** 2026-10-17

## Decision

Use CircleCI as Sandium's coordinator/source workspace, Brave Core's native Siso integration as the build scheduler, and BuildBuddy REAPI for eligible remote compile actions. Remote execution must remain opt-in. Do not transplant the Afterbird pipeline or its assumptions into Brave Core.

SANDFOX remains reference-only. This design reuses technical lessons, not SANDFOX credentials, CircleCI project/configuration, cache namespace, checkpoints, artifacts or source checkout.

## Verified source identity

- Repository: https://github.com/sandeepbimt/Sandium
- Source commit reviewed: 06cd65a7e4fcea784e73c6deb9e4ce52889dc710
- Brave Core package version: 1.100.10
- Chromium pin in package.json: 156.0.8078.39
- Relevant files: build/commands/lib/config.ts, build/commands/lib/sisoUtils.ts, build/commands/lib/syncUtils.ts, build/commands/scripts/sync.ts, build/commands/scripts/build.ts, and docs/siso_customization.md.

## Brave-native integration findings

1. Brave reads rbe_service, use_remoteexec, siso_cache_dir and related options from its .env configuration.
2. When rbe_service is set, config.ts initially sets Chromium gclient custom variables for reapi_address, reapi_instance=default and reapi_backend_config_path=google.star, then allows projects_chrome_custom_vars overrides. A BuildBuddy backend therefore needs an explicit Sandium-owned backend-path override.
3. Brave's Siso helper writes .sisorc. With RBE configured, it also adds -config googlechrome, -reapi_keep_exec_stream and related transfer/flush settings, and optionally enables a local disk cache. Compatibility of that generated configuration with BuildBuddy must be validated; do not assume it is correct or remove the flag speculatively.
4. use_remoteexec defaults to false. The build CLI supports --use_remoteexec true. Preserve this opt-in behavior.
5. Source sync, third-party dependency download, GN generation, local-only actions, packaging and device tests remain work for the CircleCI coordinator even when compile actions execute remotely.

## REAPI endpoint, authentication and cache-scope review (2026-10-17)

### Verified from pinned source metadata

Chromium DEPS for Sandium's pin `156.0.8078.39` declares `reapi_address`, `reapi_instance`, `reapi_backend_config_path`, and `reapi_credential_helper` for non-Google REAPI configuration. It pins Siso to `c574896b272b40aac6e44c228ee0b471ea7e3d7d`. The credential-helper variable is documented as a binary available on PATH or an absolute path. Source: [Chromium DEPS](https://chromium.googlesource.com/chromium/src/%2B/8a02fdbdfd14beedbb001c49e39d4d8666488921/DEPS) shows this Siso pin and variable contract; exact pinned source retrieval was not available through the source browser during this review.

Siso's published authentication guide says a non-Google REAPI backend needs a compatible credential helper, mTLS, or insecure mode. Insecure mode must not be used for a public cloud service. The current guide documents `SISO_CREDENTIAL_HELPER` and Bazel-compatible credential-helper support. Compatibility at Sandium's exact pinned Siso hash remains unverified. [Siso authentication guide](https://chromium.googlesource.com/build/%2B/b1d3e7eff1af4e3ddb2fe779cf541a4ea4071cb3/siso/docs/auth.md).

### BuildBuddy endpoint and authentication

- **Documented candidate, not validated for Siso:** BuildBuddy's RBE guide uses `grpcs://remote.buildbuddy.io` as the Bazel remote-execution endpoint. It is a reasonable candidate for a later controlled Sandium check, but does not prove the pinned Siso client, Brave's `-config googlechrome` settings, and this BuildBuddy organization work together.
- BuildBuddy documents API-key authentication using the `x-buildbuddy-api-key` gRPC metadata/header and supports multiple organization API keys. This establishes the header name, not end-to-end Siso integration. [BuildBuddy authentication guide](https://www.buildbuddy.io/docs/guide-auth/).
- The credential-helper specification allows a helper to return request headers, so a helper that emits `x-buildbuddy-api-key` is protocol-plausible. It must accept only the expected REAPI URI, fail closed for other hosts, read the key from a protected environment secret, and never log the key. Do not implement or enable it until tested against the pinned Siso. [Credential-helper specification](https://github.com/EngFlow/credential-helper-spec/blob/main/spec.md).
- BuildBuddy documents `remote.buildbuddy.io` in Bazel RBE examples and describes its managed Cloud remote caching/execution platform. These facts do not prove this account's feature access or quotas. [BuildBuddy RBE setup](https://www.buildbuddy.io/docs/rbe-setup/) · [BuildBuddy Quickstart](https://www.buildbuddy.io/docs/quickstart/).

### Instance namespace and isolation

BuildBuddy documents `remote_instance_name` as a way to namespace separate Bazel caches. Chromium exposes `reapi_instance` for a non-RBE address. However, the exact mapping of a chosen BuildBuddy instance name to Siso's REAPI `instance_name`, account permissions, and resulting cache-isolation boundary have not been verified. A separate API key is authentication separation, not cache isolation. Do not guess an instance string or enable cache writes against an unverified namespace.

### Review conclusion

The next safe technical step remains **read-only contract resolution**: inspect the pinned Siso credential-helper protocol and generated `.sisoenv`/`.sisorc` contract from the exact Chromium dependency revision; confirm BuildBuddy's supported REAPI endpoint and instance semantics for this account; then document the exact helper and cache-isolation design. No repository build, CI run, credential use, or configuration change is part of this step.
## Intended architecture

- CircleCI: pinned source checkout/sync, dependency and toolchain hooks, GN configuration, orchestration, packaging, diagnostic preservation, artifact hashing and later device smoke tests.
- Siso: build graph scheduling and execution client, using Brave's existing scripts and autoninja path.
- BuildBuddy: remote execution and potentially remote action cache, accessed through a Sandium-owned credential helper generated at runtime.
- Protected secret: configure a fresh Sandium-specific API key in a separate CircleCI project/context. Never commit it or print it.
- Cache isolation: a new API key alone does not prove a separate cache namespace. Verify a Sandium-specific REAPI instance/namespace or a separate BuildBuddy project/organization. Until verified, disable remote-cache writes or stop before using shared cache state.
- Initial backend properties: start with the smallest platform declaration justified by a real action. The SANDFOX M151 proof used OSFamily=Linux only but proves that constraint only for its tested action.

## Proposed gates (no builds are authorized by this document)

### Gate 0 — infrastructure and cost
Confirm CircleCI project separation, plan/runtime/credits, machine class and disk/RAM headroom. Confirm BuildBuddy remote execution availability, secret handling and cache isolation. Keep workflows disabled by default. Validate config statically without syncing Chromium or compiling.

### Gate 1 — pinned source/config preflight
Record the actual source SHA, Chromium revision, target architecture and tool versions. Verify generated gclient custom vars, SISO_REAPI_ADDRESS, SISO_REAPI_INSTANCE, SISO_CREDENTIAL_HELPER, generated .sisoenv and .sisorc. Explicitly inspect how Brave's -config googlechrome setting interacts with the BuildBuddy backend. Stop on any mismatch.

### Gate 2 — revision-specific remote action
After cost and build approval, use one small meaningful action from Sandium's actual pinned Chromium/Brave graph; do not repeat a synthetic no-source probe. Capture invocation ID, source SHA, GN args, Siso version, local/remote/cache counters, output, runtime and diagnostics. The existing SANDFOX proof was Chromium M151 and cannot validate Sandium's Chromium 156 pin.

### Gate 3 — controlled APK build
Only after Gate 2 succeeds, approve a single Android APK build. Candidate command, not run or yet validated:
pnpm run build Debug --target_os=android --target_arch=arm64 --target_android_output_format=apk --use_remoteexec true

Confirm the architecture before committing it. Require real APK path, nonzero size, SHA-256, artifact integrity, successful install and a basic device smoke test. Do not add the old artificial 35/36-minute timeout; respect the actual CircleCI limit and preserve diagnostics.

### Gate 4 — cache or checkpoint, only if measurements require it
Measure remote action-cache reuse before inventing serialized checkpointing. A CircleCI workspace is a handoff between jobs in one workflow, not cross-run persistent disk. CircleCI caches, remote action caches and saved GN/Ninja/Siso checkpoints are separate mechanisms. Checkpoint restoration requires source/config identity, archive integrity, Siso state, file metadata/timestamps and forward-progress evidence. An archive upload or cache-hit counter alone is not proof of a correct resume.

## Capacity risks

CircleCI currently documents a one-hour maximum job on the Free plan. Its machine documentation lists Gen1 large as 4 vCPU / 15 GB RAM / 150 GB disk and xlarge as 8 vCPU / 32 GB RAM / 150 GB disk; verify exact class/image availability and credits in the Sandium account. Chromium Android instructions require at least 100 GB free disk and recommend more than 16 GB RAM, leaving limited headroom for source checkout, dependencies, build output, and artifacts on the smaller class.

Remote execution does not guarantee that the full build fits within the CircleCI job limit. It reduces eligible local compilation but does not eliminate source sync, GN generation, local-only actions, APK packaging, checkpoint transfer or smoke testing. Do not use an artificial 36-minute build cutoff.

## References

- Brave Core README: https://github.com/brave/brave-core/blob/master/README.md
- Brave Android guide: https://github.com/brave/brave-browser/wiki/Android-Development-Environment
- Brave Siso customization: https://github.com/brave/brave-core/blob/master/docs/siso_customization.md
- Chromium Android instructions: https://chromium.googlesource.com/chromium/src/+/main/docs/android_build_instructions.md
- Chromium non-Google RBE configuration: https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md
- CircleCI job/resource reference: https://circleci.com/docs/reference/configuration-reference/
- CircleCI machine resources: https://circleci.com/docs/guides/execute/using-linuxvm/
- BuildBuddy remote execution: https://www.buildbuddy.io/docs/remote-build-execution/
- BuildBuddy authentication: https://www.buildbuddy.io/docs/guide-auth/
- Reference-only SANDFOX M151 remote compile checkpoint: https://github.com/sandeepbimt/Sandfox-Chromium/blob/afterbird/docs/SANDFOX_Siso_BuildBuddy_Remote_Build_Checkpoint_2026-10-09.md

## Preflight configuration staged (2026-10-17)

A no-build CircleCI preflight has been staged in [branch ci/sandium-buildbuddy-siso-preflight](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight), commit 3610ff348694d9cf923dbcffaf633017fade4edc:

- [CircleCI config](https://github.com/sandeepbimt/Sandium/blob/ci/sandium-buildbuddy-siso-preflight/.circleci/config.yml)
- [BuildBuddy backend starting point](https://github.com/sandeepbimt/Sandium/blob/ci/sandium-buildbuddy-siso-preflight/ci/siso/buildbuddy_backend.star)

The config has one workflow parameter, run_sandium_rbe_preflight, defaulting to false. The only defined job is a lightweight metadata/configuration check. It does not check out the huge source tree, call BuildBuddy, run gclient, run GN, or compile. It fetches only package.json and the backend file at the exact CircleCI commit SHA. It requires protected CircleCI environment values for the address, explicit REAPI instance, API-key presence, and a cache-scope acknowledgment; it never prints the API key.

Local static checks passed: YAML parsing and bash syntax parsing. This is not CircleCI server-side config validation, does not prove the CircleCI project is linked, does not authenticate the key, and cannot establish cache isolation by itself. The SANDIUM_CACHE_SCOPE_CONFIRMED flag is only an operator acknowledgment, not technical proof. The workflow has not been triggered. No build job exists in this preflight config.

## Verdict

**Architecture fit: promising, not validated for Sandium.** Account access, isolated cache namespace, CircleCI configuration, the generated Brave Siso settings, remote execution on the pinned revision, cost and full APK completion remain unverified. No source build or CI workflow has run for Sandium.


## Source patch review branch (2026-10-17)

After approval, a narrow source-only patch was applied to [review/googlechrome-config-opt-in-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/googlechrome-config-opt-in-2026-10-17). Commits:
- [f748e2d](https://github.com/sandeepbimt/Sandium/commit/f748e2deec3bec90c9ed83cc210c2526f55af7b1): add default-false `siso_use_googlechrome_config` config and typed property.
- [713e07e](https://github.com/sandeepbimt/Sandium/commit/713e07e5dd6bc0340e695e529e7bd7574390612d): emit `-config googlechrome` only when the option is explicitly true.

GitHub compare confirms the branch is two commits ahead of master, zero behind, with only `build/commands/lib/config.ts` and `build/commands/lib/sisoUtils.ts` changed. Static assertions confirmed the option defaults false and the flag is conditional. No TypeScript typecheck/lint, Chromium checkout, CI run, REAPI request, or build was run.

Important limit: this patch addresses only Brave's unconditional Google-specific Siso preset. It does **not** correct the separate `google.star` backend and `default` instance defaults in `config.ts`; Sandium-specific custom variables must override these before any BuildBuddy test. The patch is not a complete BuildBuddy integration and does not authorize remote cache access or writes.
