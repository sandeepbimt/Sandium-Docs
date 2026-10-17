# SANDIUM — Durable Knowledge Index

Read this before proposing technical changes. Detailed evidence belongs in linked records. Do not treat hypotheses as facts.

## Governing rules

1. All Sandium code, CI, builds, artifacts, logs and checkpoints use Sandium-owned repository configuration and separately configured infrastructure.
2. SANDFOX is reference-only. Do not trigger or depend on its jobs, credentials, caches, Siso state, checkpoints, artifacts or source checkout.
3. Do not start an expensive build until the question, cost, pass/fail signals and next decision are documented.
4. A green job, cache hit, archive upload or increasing counter alone does not prove successful incremental resume.
5. Never claim resume/cross-run reuse without evidence of restored state and useful forward progress.
6. Preserve history; correct records by linking new entries rather than erasing old conclusions.
7. Separate VERIFIED, HYPOTHESIS, REJECTED and SUPERSEDED findings.
8. Each consequential experiment records identity, cost, evidence, outcome and learning.
9. End each work session with updated status and chat handoff.
10. Never store secrets or token values in repository docs or logs.
11. Sandium CI must use exactly five sequential, purpose-defined stages, avoid repeating completed work, include all handover preparation in per-stage runtime, prove same-run and cross-run reuse, and fast-skip downstream work after a valid matching APK is persisted. This is an acceptance requirement, not proof that CI has passed; see SANDIUM_TEST_PLAN.md and SANDIUM_CI_ARCHITECTURE.md.

## Verified state

- Repository: https://github.com/sandeepbimt/Sandium
- Product: Android browser initially based on official Brave Android.
- No Sandium-specific build, cache or checkpoint behavior is proven yet.

## Brave-native Siso/BuildBuddy integration (2026-10-17)

- **VERIFIED:** Sandium master commit 06cd65a7e4fcea784e73c6deb9e4ce52889dc710 pins Brave Core 1.100.10 and Chromium 156.0.8078.39.
- **VERIFIED from source code:** Brave Core supports REAPI through .env/gclient custom vars and Siso; --use_remoteexec true is available and remote execution defaults off.
- **Critical adapter detail:** With rbe_service, Brave initially sets reapi_backend_config_path=google.star; Sandium must override that to a Sandium-owned BuildBuddy backend. Brave sisoUtils.ts also writes -config googlechrome; compatibility with BuildBuddy must be validated, not assumed.
- **Reference-only proof:** SANDFOX's Chromium M151 checkpoint reports one successful real C++ remote action with remote:1, local:0, cache:0. This validates the concept for that action only; it does not prove cache hits, checkpoint restore, Chromium M156 behavior or a complete APK.
- **Architecture direction:** CircleCI orchestrates and hosts the source workspace; Siso drives the build; BuildBuddy executes eligible remote actions. Remote execution does not remove source sync, GN generation, local-only actions, packaging or tests.
- **Isolation:** A new API key alone does not guarantee cache isolation. Verify a Sandium-specific REAPI instance/namespace or a separate BuildBuddy project; otherwise disable remote-cache writes until scope is clear. Never copy SANDFOX credentials, caches, checkpoints, artifacts or workflows.
- **No build yet:** Account/project configuration, quotas/cost, actual resource class, generated .sisoenv/.sisorc, remote execution at the pinned revision and APK completion remain unverified.
- **Detailed record:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md).

## Lesson entry format

ID; status; concise rule; conditions/scope; evidence links; originating experiment/decision; date. Add entries only when evidence supports them. Keep narrative in detailed records.

## Automation is a project requirement

- **User constraint (2026-10-17):** The user will not manually update any ledger or Markdown record. ChatGPT owns session-level updates; automated workflows own machine-observable evidence.
- **Automation contract:** [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md) is authoritative for event triggers and trust boundaries.
- **Implemented but not yet proven end-to-end:** A scheduled GitHub Actions recordkeeper and evidence recorder exist. They must be tested against real workflow metadata and verified commits before being considered operational.
- **Scope split:** GitHub can record workflow/run/job/artifact metadata. ChatGPT must record decisions, hypotheses, conclusions and user instructions from conversations because GitHub cannot access private ChatGPT history.
- **CircleCI:** Not automated until a separately configured Sandium-only API/webhook integration is tested. Never borrow SANDFOX credentials or infrastructure.
- **Safety:** Recorder workflows must never trigger browser builds. Do not add every successful workflow to the clean-base ledger; only relevant build/artifact candidates belong there. A candidate is not accepted without artifact integrity and test evidence.

## Additional source-level findings: BuildBuddy compatibility (2026-10-17)

- **VERIFIED:** Chromium 156.0.8078.39 passes reapi_address, reapi_instance, reapi_backend_config_path and reapi_credential_helper into configure_siso.py. The same revision pins Siso to c574896b272b40aac6e44c228ee0b471ea7e3d7d.
- **VERIFIED:** Brave's EnvConfig merges projects_chrome_custom_vars after its rbe_service-derived defaults. This gives Sandium a supported way to override the Google backend defaults.
- **VERIFIED:** The official Chromium non-Google RBE guide provides a custom backend.star example using the digest-pinned siso-chromium Linux image. BuildBuddy documents custom container-image platform properties.
- **CANDIDATE, not tested:** REAPI host remote.buildbuddy.io:443; a stable BuildBuddy instance name such as sandium/android-arm64/ci; the official pinned image; and a host-scoped get credential helper emitting x-buildbuddy-api-key. The organization account's authentication, executor image pull and instance behavior remain unverified.
- **SECURITY:** Keep the BuildBuddy API key only in a protected Sandium CircleCI secret. The helper must reject unexpected hosts/protocols and must never log the key. Do not enable insecure REAPI.
- **SISO PRESET:** Chromium's googlechrome preset is specifically maintained for Google's RBE, separate from backend.star. Keep it opt-in during initial qualification; compare the broader remote action rules on BuildBuddy before enabling for speed.
- **CAPACITY RISK:** CircleCI workspace data is workflow-scoped and is transferred to each downstream job; cross-run reuse needs cache or other persistent state. Full Chromium source snapshot packaging is not the default; source materialization and checkpoint times must be measured separately against the 50-minute stage target.
- **NEXT GATE:** The source-only adapter patch and deterministic offline tests are complete on review/sandium-buildbuddy-backend-2026-10-17. Fourteen unit tests passed and pinned configure_siso.py generated the expected local config. Next, obtain separate explicit approval for Siso auth-check; no CI, REAPI request, sync or build has been performed.
- **Details and references:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md).


## Offline adapter evidence (2026-10-17)

- Branch: [review/sandium-buildbuddy-backend-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/sandium-buildbuddy-backend-2026-10-17); final commit 806f565ea44e256344f05cafe1b2b80b577aecfc. Four commits ahead of master, zero behind, no PR/merge.
- 14 local tests pass for fake credential-helper requests, rejected hosts/protocols/ports, missing credentials, malformed input, runtime env idempotence and secret exclusion, endpoint/namespace guards, helper chmod, and backend image/property checks.
- Chromium 156.0.8078.39 configure_siso.py blob SHA cb0ce6aadd79bf1e0fa88f3da6b0b82ffee366e5 matched exactly and generated the expected .sisoenv plus byte-identical backend.star in a temporary workspace.
- This is offline configuration evidence only. Actual Siso helper invocation, BuildBuddy auth/instance/image behavior, remote cache, source-state reuse, speed and APK production remain unverified.
