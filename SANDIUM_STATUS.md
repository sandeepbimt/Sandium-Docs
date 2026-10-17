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
- [x] Evidence-driven automation contract and GitHub Actions run recorder committed (end-to-end run still needs verification).
- [x] Automation decision, experiment record, operational risk and end-to-end acceptance checklist documented.
- [ ] Official Brave Android build feasibility is documented for a pinned revision.
- [ ] Sandium-only CI architecture is reviewed against the selected Brave revision.
- [ ] Sandium-specific CircleCI/BuildBuddy/Siso setup is independently validated.
- [x] Brave-native Siso/REAPI integration points inspected; Sandium-only design documented (not implemented or tested).
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

The Brave-native Siso/REAPI route is source-supported but not validated against Sandium's Chromium 156 pin. Sandium-specific CircleCI project/context, a protected BuildBuddy API key, isolated REAPI cache namespace, account quota/cost, and compatibility of Brave's generated google.star default plus -config googlechrome with BuildBuddy remain unresolved. CircleCI Free has a one-hour job cap; remote execution does not remove source-sync, GN, packaging or test costs. The docs recordkeeper's end-to-end operation is also unverified.

## Single next action

Complete Sandium-only infrastructure preflight without compiling: confirm CircleCI resource class/runtime/credits and arrange a protected Sandium-specific BuildBuddy key plus isolated cache namespace. Then prepare a disabled-by-default CircleCI configuration that validates pins and remote configuration before any expensive source sync or build. Do not launch an APK build or reuse SANDFOX infrastructure.

## Records

- [Charter](SANDIUM_STARTER.md) · [Remote build design](SANDIUM_REMOTE_BUILD_DESIGN.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md) · [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md) · [Recordkeeper](.github/workflows/project-recordkeeper.yml) · [Recorder script](.github/scripts/record_workflow_evidence.py)
- [Documentation validator](.github/scripts/validate_docs.py) · [Validation workflow](.github/workflows/docs-validation.yml) · [Automation test plan](SANDIUM_TEST_PLAN.md)

## Automation state

The GitHub recordkeeper is committed but is not yet considered operational until a real end-to-end run and resulting commit are verified. ChatGPT owns conversation-derived updates; CircleCI evidence remains pending a Sandium-only integration. The user is not expected to maintain Markdown manually. See [automation contract](SANDIUM_AUTOMATION_RULES.md), [DEC-004](SANDIUM_DECISIONS.md), [EXP-AUTO-001](SANDIUM_EXPERIMENT_LOG.md) and [test plan](SANDIUM_TEST_PLAN.md).

<!-- SANDIUM_AUTO_STATUS_START -->
- No completed non-documentation workflow run has been verified as a project/build result yet.
- Documentation-validation run #18 failed due to a malformed newline in the validator; source fix was committed at `63d0d723e5d8ee67e1725ab65bcf12dcb61f6223`, and later validation still needs inspection.
- **Boundary:** Documentation runs are excluded from the latest project/build snapshot and clean-base ledger. CircleCI is not covered until a Sandium-only integration is configured and tested. ChatGPT must still record decisions and findings GitHub cannot observe.
<!-- SANDIUM_AUTO_STATUS_END -->
