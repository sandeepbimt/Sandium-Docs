> **SOURCE PIVOT — 2026-10-25:** This file contains the prior source-specific design. Its browser-source assumptions are superseded. Do not use its old source pins, source scripts, custom Siso presets, override handlers, patch workflow or build commands. The only current browser-source authority is [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md), and the current adapter design is [SANDIUM_BARE_BUILD_ADAPTER.md](SANDIUM_BARE_BUILD_ADAPTER.md). Reuse only verified infrastructure-level integration details. Do not recreate credentials or clear caches.

---

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

At the time of the initial read-only review, the next safe technical step was contract resolution. That source investigation is now documented below, and an isolated adapter patch plus offline config-generation test has been completed. The remaining blocker is runtime validation of the actual pinned Siso/BuildBuddy path; it requires a separately approved auth-check.
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

Local static checks passed: YAML parsing and bash syntax parsing. This is not CircleCI server-side config validation, does not prove the CircleCI project is linked, does not authenticate the key, and cannot establish cache isolation by itself. The SANDIUM_CACHE_SCOPE_CONFIRMED flag is only an operator acknowledgment, not technical proof. A previous GitHub-triggered CircleCI preflight attempt reached the CircleCI job but failed because SANDIUM_REAPI_ADDRESS was unset at that time. The job stopped before contacting BuildBuddy. No build job exists in this preflight config, and no successful preflight/authenticated REAPI request is established.

## Verdict

**Architecture fit: promising, still not validated end-to-end.** A lightweight CircleCI preflight was attempted but failed before BuildBuddy access due to the missing endpoint variable. The separate source-review branch now passes offline tests and the pinned config-generator check, but account access, cache isolation, helper interoperability, image pull, remote execution, cost and full APK completion remain unverified. No Chromium source sync or browser compile/APK build has run.


## Source patch review branch (2026-10-17)

After approval, a narrow source-only patch was applied to [review/googlechrome-config-opt-in-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/googlechrome-config-opt-in-2026-10-17). Commits:
- [f748e2d](https://github.com/sandeepbimt/Sandium/commit/f748e2deec3bec90c9ed83cc210c2526f55af7b1): add default-false `siso_use_googlechrome_config` config and typed property.
- [713e07e](https://github.com/sandeepbimt/Sandium/commit/713e07e5dd6bc0340e695e529e7bd7574390612d): emit `-config googlechrome` only when the option is explicitly true.

GitHub compare confirms the branch is two commits ahead of master, zero behind, with only `build/commands/lib/config.ts` and `build/commands/lib/sisoUtils.ts` changed. Static assertions confirmed the option defaults false and the flag is conditional. No TypeScript typecheck/lint, Chromium checkout, CI run, REAPI request, or build was run.

Important limit: this patch addresses only Brave's unconditional Google-specific Siso preset. It does **not** correct the separate `google.star` backend and `default` instance defaults in `config.ts`; Sandium-specific custom variables must override these before any BuildBuddy test. The patch is not a complete BuildBuddy integration and does not authorize remote cache access or writes.

## Pinned non-Google REAPI configuration investigation (2026-10-17)

### Verified configuration chain

The source-level gap is narrower than it first appeared. At Sandium's pinned Chromium 156.0.8078.39, Chromium DEPS defines reapi_address, reapi_instance, reapi_backend_config_path, and reapi_credential_helper, and pins Siso to git_revision:c574896b272b40aac6e44c228ee0b471ea7e3d7d. Its configure_siso hook passes all four settings to build/config/siso/configure_siso.py. That script generates .sisoenv and installs the chosen backend configuration as build/config/siso/backend_config/backend.star. Source: [Chromium DEPS at the pinned revision](https://chromium.googlesource.com/chromium/src.git/+/8a02fdbdfd14beedbb001c49e39d4d8666488921/DEPS); [Chromium non-Google RBE guide](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#non-Google-RBE).

Brave Core config.ts sets Google defaults when rbe_service is nonempty: reapi_address=rbe_service, reapi_backend_config_path=google.star, and reapi_instance=default. This is not a hard-coded limitation: projects_chrome_custom_vars is merged after those defaults, and EnvConfig.getMergedObject() supports the corresponding .env prefix form (for example, projects_chrome_custom_vars_reapi_instance=...). Sandium can override the backend path, instance and credential helper without redesigning Brave's sync system. Relevant pinned files: [config.ts](https://github.com/brave/brave-core/blob/06cd65a7e4fcea784e73c6deb9e4ce52889dc710/build/commands/lib/config.ts), [syncUtils.ts](https://github.com/brave/brave-core/blob/06cd65a7e4fcea784e73c6deb9e4ce52889dc710/build/commands/lib/syncUtils.ts), and [Chromium configure_siso.py](https://github.com/chromium/chromium/blob/156.0.8078.39/build/config/siso/configure_siso.py).

### Proposed values — still require controlled validation

- **REAPI endpoint:** remote.buildbuddy.io:443. BuildBuddy's Bazel guide uses grpcs://remote.buildbuddy.io; Chromium's Siso non-Google example expects host:port in reapi_address, so use the scheme-less form in Brave/Chromium custom vars. Do not use sandium.buildbuddy.io, which is the organization web UI rather than the documented REAPI endpoint. [BuildBuddy RBE setup](https://www.buildbuddy.io/docs/rbe-setup/).
- **Instance/cache namespace:** sandium/android-arm64/ci is a proposed stable name, not an account-tested value. BuildBuddy documents REAPI instance names as cache namespaces. Keep it identical across stages and future identical builds so caches can be reused; do not include workflow IDs or timestamps. A namespace is not by itself an authorization boundary. Sandium must use its own BuildBuddy organization/key; never use SANDFOX.
- **Backend config path:** ../../../../brave/ci/siso/buildbuddy_backend.star is the candidate relative path when resolved from Chromium's build/config/siso/backend_config directory in the required workspace layout: <workspace>/src for Chromium and <workspace>/src/brave for Sandium. An absolute path is also supported. A no-build generation check should confirm the actual resolved path before any REAPI call.
- **Credential helper:** point reapi_credential_helper at an absolute runtime path to a Sandium-owned executable, for example <workspace>/src/brave/ci/siso/buildbuddy-credential-helper. Generate the ignored runtime .env only after the working directory is established; do not hard-code CircleCI paths into source. The helper source itself must contain no key.
- **Illustrative runtime-only .env settings (no secrets):**

      rbe_service=remote.buildbuddy.io:443
      projects_chrome_custom_vars_reapi_address=remote.buildbuddy.io:443
      projects_chrome_custom_vars_reapi_instance=sandium/android-arm64/ci
      projects_chrome_custom_vars_reapi_backend_config_path=../../../../brave/ci/siso/buildbuddy_backend.star
      projects_chrome_custom_vars_reapi_credential_helper=<absolute-workspace-path>/src/brave/ci/siso/buildbuddy-credential-helper
      siso_use_googlechrome_config=false

  The last setting exists only on the unmerged review branch [review/googlechrome-config-opt-in-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/googlechrome-config-opt-in-2026-10-17); it has not been merged to master. Never put BUILDBUDDY_API_KEY in .env, source files or logs; it belongs only in a protected Sandium CircleCI secret.

### Remote executor image: evidence-backed candidate

The currently staged ci/siso/buildbuddy_backend.star only declares OSFamily=Linux; it does not select a container image. BuildBuddy's docs say its generic executor image is Ubuntu 16.04 with Java 8, and that custom container-image platform properties are supported. That generic environment is not shown to match Chromium 156's remote action requirements.

The official Chromium non-Google RBE guide itself provides this digest-pinned image in its sample backend:
docker://gcr.io/chops-public-images-prod/rbe/siso-chromium/linux@sha256:d7cb1ab14a0f20aa669c23f22c15a9dead761dcac19f43985bf9dd5f41fbef3a

That is the strongest source-backed image candidate for an initial Sandium test. A Sandium backend should use the pinned image for both default and large action classes without copying Google's label:action_default or label:action_large worker-pool labels. BuildBuddy image pullability and action compatibility still require a controlled test; do not infer success from public docs alone. Sources: [Chromium non-Google RBE example](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#non-Google-RBE), [BuildBuddy RBE platforms](https://www.buildbuddy.io/docs/rbe-platforms/).

### Credential helper contract and security

BuildBuddy documents x-buildbuddy-api-key as the authentication header/metadata and supports organization API keys. The credential-helper specification permits a get helper to read a JSON request containing a uri from stdin and emit JSON headers, so returning {"headers":{"x-buildbuddy-api-key":["..."]}} is protocol-plausible. The helper must fail closed unless the URI is for the expected secure BuildBuddy REAPI host, require BUILDBUDDY_API_KEY, emit no diagnostics containing secret values, and return the key only in the required JSON response. A script committed via GitHub's file contents API may not retain executable mode; CI must explicitly set executable permission or use another verified executable wrapper.

Official references: [BuildBuddy authentication](https://www.buildbuddy.io/docs/guide-auth/), [Credential Helpers specification](https://github.com/EngFlow/credential-helper-spec/blob/main/spec.md), [Siso authentication guide](https://chromium.googlesource.com/build/+/siso/v1.5.9/siso/docs/auth.md). Pinned Chromium DEPS proves the helper path is passed into configure_siso.py; the exact Siso binary at the pinned commit was not independently exercised, so wire-level compatibility remains unproven. Do not use Siso insecure mode on a public cloud endpoint.

### Google-specific Siso preset: keep it gated

Chromium's pinned build/config/siso/config.star describes googlechrome as a preset for Chrome builds using Google's RBE, with remote rules tested/maintained by Google's build team. The preset changes action eligibility across Android, Mojo, Blink, V8, Rust, GRIT and TypeScript rules; it is separate from backend.star selection. The earlier review patch makes Brave's unconditional -config googlechrome opt-in. Keep it disabled for the first connection/action qualification. Once the generic remote path is proven, compare eligible action coverage and failures before enabling it for BuildBuddy. It may be required for broad remote parallelism, but compatibility and performance are not established yet. Source: [Chromium config.star at 156.0.8078.39](https://github.com/chromium/chromium/blob/156.0.8078.39/build/config/siso/config.star), [Brave Siso customization](https://github.com/brave/brave-core/blob/06cd65a7e4fcea784e73c6deb9e4ce52889dc710/docs/siso_customization.md).

### Required workspace layout

Brave Core's rootDir.cjs walks five parent directories from src/brave/build/commands/lib to infer the workspace root. The expected gclient layout is therefore Chromium at <workspace>/src and Sandium/Brave Core at <workspace>/src/brave, with .gclient at <workspace>. A standard CircleCI checkout directly into ~/project would put the code in the wrong location unless the job's working directory/checkout path is explicitly arranged. Establish this layout before generating .env or running Brave sync.

### What this does not settle

- The organization account's actual remote execution entitlement, quota, effective usage or image-pull success.
- Authentication and cache RPC success using Sandium's API key and the pinned Siso binary.
- Whether the proposed instance string is accepted by this organization's cloud endpoint; public docs establish namespace semantics, not account-specific permissions.
- Whether googlechrome can safely expand all remote action types for BuildBuddy.
- Five-stage cross-job source/state transfer time. CircleCI workspaces are scoped to one workflow and attach downloads all persisted contents; caches have a 15-day maximum retention and larger caches take longer to restore. Chromium's official docs say the Git cache alone is about 30 GB and a fast fetch can take about 30 minutes. Do not package the whole Chromium tree as a checkpoint by default. Measure a stable Git-object cache plus workspace/materialization strategy and the Siso output checkpoint separately. If the first stage or handover cannot stay within the 50-minute target, redesign before an APK run. References: [CircleCI workspaces](https://circleci.com/docs/guides/orchestrate/workspaces/), [CircleCI caching](https://circleci.com/docs/guides/optimize/caching/), [Chromium build instructions](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md).
- Local .env generation and the pinned configure_siso.py path have now been tested in a temporary offline workspace (see the source-only adapter evidence below). No Siso auth-check, REAPI call, source sync, CircleCI preflight/browser build, compile or APK build was run.

### Gate status after the source-only adapter patch (2026-10-17)

1. **Source-only adapter patch — complete on a review branch.** Branch: [review/sandium-buildbuddy-backend-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/sandium-buildbuddy-backend-2026-10-17). The branch carries the earlier Google-preset opt-in change plus the BuildBuddy backend, runtime .env generator, host-scoped credential helper and offline tests. The branch is four commits ahead of master, zero behind; no PR or merge exists.
2. **Offline tests — pass within their intended scope.** Fourteen unit tests pass with fake credentials/URIs. They verify the secure-host allowlist, rejection behavior, no secret in diagnostics or generated .env, idempotent managed-block updates, namespace/endpoint guards, helper executable permission set by the generator, and the digest-pinned backend's properties.
3. **Pinned configure_siso.py generation check — pass in a temporary workspace.** The exact Chromium 156.0.8078.39 configure_siso.py source file was verified against Git blob SHA cb0ce6aadd79bf1e0fa88f3da6b0b82ffee366e5. It generated SISO_REAPI_ADDRESS, SISO_REAPI_INSTANCE and SISO_CREDENTIAL_HELPER with the expected values, and copied the backend file byte-for-byte to backend_config/backend.star.
4. **Not tested:** Brave EnvConfig-to-.gclient-to-configure_siso end-to-end parsing; Siso binary/auth-helper interoperability; BuildBuddy account authentication, namespace acceptance or image pull; remote action execution/cache behavior; any CircleCI job, Chromium sync, compilation or APK.

### Required next gates

1. **Next, only with separate approval:** run the pinned Siso executable's auth-check against the BuildBuddy endpoint using the protected Sandium key. This contacts REAPI but must not sync Chromium or compile. Keep credentials redacted and stop on any endpoint, namespace, helper or authorization mismatch.
2. After auth-check passes, and only with separate approval for remote execution/cost, run one meaningful action against Sandium's pinned Chromium graph. Capture invocation ID, remote/local/cache counts, image/worker result, action output, runtime and diagnostics.
3. Only after the action succeeds and capacity/cost are reviewed should a full APK run be considered. The five-stage acceptance criteria remain a later implementation and measurement task, not established by this source-only test.
4. Do not merge this review branch, trigger CircleCI, call REAPI, sync Chromium or build an APK without the corresponding explicit gate approval.

This source-only investigation and local test do not authorize a network/build gate.


## Gate review after successful auth-only run (2026-10-17)

**Decision: do not start remote execution or a browser build yet.** The isolated auth-only run [39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682) verifies that the pinned Siso executable can complete the configured authentication check for the proposed BuildBuddy endpoint/instance. It does not close the separate cost, namespace-isolation, backend/image, or remote-action gates.

- **Gate 0 — partially open:** A Sandium-specific GitHub secret exists and auth passed, but the available evidence does not establish BuildBuddy entitlement/quotas, effective pricing/usage limits, CircleCI project/context configuration, runner capacity, or a complete per-run cost estimate. Do not assume the remote execution plan is free or within budget.
- **Gate 1 — partial only:** Offline tests and pinned configure_siso.py generation passed, and auth passed. Full Brave EnvConfig → gclient → configure_siso integration, generated config inspection from the actual workspace, and technical proof of cache isolation remain outstanding.
- **Gate 2 — not started / requires separate approval:** No meaningful Sandium Chromium graph action has been executed. No image pull, worker compatibility, remote/local/cache action counts, or invocation evidence exists.
- **Gate 3 — not authorized / not started:** No APK build is approved by this review. There is no measured end-to-end time or cost baseline for source sync, GN, local-only work, packaging, transfer and verification.
- **Gate 4 — not started:** No cache/checkpoint restoration or same-run/cross-run reuse has been tested.

**Safe conclusion:** authentication is a necessary gate passed, not a build-feasibility or performance result. Keep remote execution opt-in and do not enable cache writes beyond the verified isolated Sandium namespace. The next step is to close the remaining no-build infrastructure/cost evidence gaps, not to run a compile or APK build.


## No-build Gate 0/1 review — public plan evidence and wiring audit (2026-10-17)

This review was intentionally limited to documentation, public vendor documentation and read-only inspection of the Sandium review branch. No workflow was triggered and no REAPI request was made.

### Public plan facts (not account-specific entitlement)

- BuildBuddy's current public pricing page lists the Personal plan as free, with remote execution up to 80 cores and 100 GB of cache transfer; Team is pay-as-you-go beyond the included transfer. Source: [BuildBuddy pricing](https://www.buildbuddy.io/pricing/).
- BuildBuddy's RBE configuration page says configuring a self-hosted BuildBuddy deployment's remote execution requires Enterprise. This is not the same question as whether BuildBuddy's hosted Personal plan provides remote execution. Source: [BuildBuddy RBE configuration](https://www.buildbuddy.io/docs/config-rbe/).
- CircleCI's current Free plan docs list 30,000 credits/month for personal use and included network/storage allowances; public Linux open-source projects may qualify for up to 400,000 credits/month. Whether Sandium's repo/project qualifies and which resource class the account can use must be checked in the actual CircleCI account. Source: [CircleCI credit usage](https://circleci.com/docs/guides/plans-pricing/credits/) and [CircleCI pricing](https://circleci.com/pricing/).
- These public pages do **not** prove the user's BuildBuddy organization is on a plan with remote execution enabled, what usage remains, or whether any cache transfer overage will apply. No account billing/usage screen was accessible during this review.

### Read-only wiring audit

- **VERIFIED from source:** `ci/siso/write_buildbuddy_env.py` keeps `use_remoteexec=false`, `siso_use_googlechrome_config=false`, and writes the stable candidate instance `sandium/android-arm64/ci`; it points at the Sandium-owned credential helper and backend file.
- **VERIFIED from source:** the helper only returns `x-buildbuddy-api-key` for secure `remote.buildbuddy.io` URI requests on the allowed port and rejects other hosts/schemes. The key is read from the protected environment and is not printed by the helper.
- **VERIFIED from source:** backend image is digest-pinned to Chromium's published Siso Chromium Linux image; the file itself explicitly says image pullability and action compatibility have not been tested.
- **NOT VERIFIED end-to-end:** The generated backend path is the relative value `../../../../brave/ci/siso/buildbuddy_backend.star`. Although the prior offline configure_siso generation test passed, the exact runtime resolution from Brave's actual workspace layout through gclient/configure_siso has not been observed in a real Sandium workspace. The backend path is therefore a specific remaining static/runtime integration question, not a reason to start a build.
- **NOT PROVEN:** A stable-looking instance name is not proof of account-level namespace isolation. The successful auth check establishes authentication against the requested endpoint/instance but does not prove cache reads/writes, executor image pulls, remote actions, or a separate namespace boundary.
- **Cost rule:** Do not infer "free" from a public Personal plan description. Before any remote action, inspect the actual BuildBuddy plan/usage and CircleCI plan/credit state; record the remaining allowance, resource class, expected action and cache transfer, and a hard stop threshold.

### Gate decision

Gate 0 remains **PARTIAL** pending account-specific plan/usage and runner-resource confirmation. Gate 1 remains **PARTIAL** pending confirmation of the actual resolved backend path and generated config in the intended workspace. No remote action, cache write, CircleCI pipeline, Chromium sync, GN generation, compilation or APK build is authorized by this review.
