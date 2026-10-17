# SANDIUM — Project Status

**Last reviewed:** 2026-10-17  
**Status:** CircleCI + BuildBuddy + Siso architecture reviewed against Brave Core; Sandium-only setup unconfigured; no browser build started  
**Repository:** https://github.com/sandeepbimt/Sandium

## Current state

- [x] Independent Sandium repository exists.
- [x] Core project records and handoff protocol committed.
- [x] Documentation-only GitHub Actions workflow and validator committed.
- [x] Documentation validation workflow passed historically (run #4).
- [ ] Validator regression from run #18 is fixed in source; validation of the later fix commits has not yet been verified.
- [x] Cross-platform clean-base ledger and CI run-naming convention committed.
- [x] Five-stage, reuse-first CI acceptance criteria documented in the test plan and CI architecture; implementation and runtime behavior remain unvalidated.
- [x] Evidence-driven automation contract and GitHub Actions run recorder committed (end-to-end run still needs verification).
- [x] Automation decision, experiment record, operational risk and end-to-end acceptance checklist documented.
- [ ] Official Brave Android build feasibility is documented for a pinned revision.
- [ ] Sandium-only CI architecture is reviewed against the selected Brave revision.
- [ ] Sandium-specific CircleCI/BuildBuddy/Siso setup is independently validated.
- [x] Brave-native Siso/REAPI integration points inspected; Sandium-only design documented.
- [x] Disabled-by-default, no-build CircleCI preflight staged on [Sandium branch](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight); local YAML and shell syntax checks passed, but CircleCI server validation/execution are unverified.
- [ ] Reproducible Android APK is produced.

Do not mark work complete without evidence.

## Verified facts

- Browser source repository: sandeepbimt/Sandium, default branch master; verified fork parent is brave/brave-core.
- Source reviewed: 06cd65a7e4fcea784e73c6deb9e4ce52889dc710; Brave Core 1.100.10; Chromium pin 156.0.8078.39.
- Documentation files and a documentation-only workflow exist on main.
- The docs validator is read-only and does not build the browser. A separate scheduled recordkeeper has Actions read / repository contents write permission to record completed GitHub runs; it must be verified end-to-end.
- No Sandium Android build result is established yet.
- SANDFOX is reference-only, not a build dependency.

## Current blocker

The pinned source path is now understood: Chromium 156.0.8078.39 passes reapi_address, reapi_instance, reapi_backend_config_path and reapi_credential_helper into configure_siso.py; Brave's projects_chrome_custom_vars overlay can override its google.star/default defaults. The documented REAPI endpoint candidate is remote.buildbuddy.io:443; Chromium's official non-Google example includes a digest-pinned siso-chromium Linux image. Still unverified: the account's REAPI/auth/instance/image behavior, exact pinned Siso helper execution, broad googlechrome preset compatibility, and five-stage source/state handoff time. The staged backend lacks a container image and the current preflight only checks environment-value presence, so neither is final readiness proof. No REAPI call, source sync, CircleCI browser build or APK build was run in this investigation. Detailed findings are in SANDIUM_REMOTE_BUILD_DESIGN.md.

## Single next action

Prepare a separate source-review patch (no CI trigger and no REAPI call) that adds the pinned executor image, runtime custom-var generation, a host-scoped BuildBuddy credential helper and deterministic fake-credential tests. Keep remote execution disabled by default and keep siso_use_googlechrome_config=false for initial qualification. First perform a no-build configure_siso.py generation check against the exact Chromium pin. This is the next action proposed for approval; it must not start source sync or compile. SANDFOX remains reference-only.

## Records

- [Charter](SANDIUM_STARTER.md) · [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md) · [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md) · [Recordkeeper](.github/workflows/project-recordkeeper.yml) · [Recorder script](.github/scripts/record_workflow_evidence.py)
- [Documentation validator](.github/scripts/validate_docs.py) · [Validation workflow](.github/workflows/docs-validation.yml) · [Automation test plan](SANDIUM_TEST_PLAN.md)

## Automation state

The GitHub recordkeeper is committed but is not yet considered operational until a real end-to-end run and resulting commit are verified. ChatGPT owns conversation-derived updates; CircleCI evidence remains pending a Sandium-only integration. The user is not expected to maintain Markdown manually. See [automation contract](SANDIUM_AUTOMATION_RULES.md), [DEC-004](SANDIUM_DECISIONS.md), [EXP-AUTO-001](SANDIUM_EXPERIMENT_LOG.md) and [test plan](SANDIUM_TEST_PLAN.md).

<!-- SANDIUM_AUTO_STATUS_START -->
- No completed GitHub workflow run was available from the API.\n
<!-- SANDIUM_AUTO_STATUS_END -->
