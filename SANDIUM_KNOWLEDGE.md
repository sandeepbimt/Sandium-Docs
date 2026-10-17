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
