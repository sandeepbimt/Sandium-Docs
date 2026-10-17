# SANDIUM — Project Status

**Last reviewed:** 2026-10-17  
**Status:** Recordkeeping automation implementation committed; end-to-end verification pending; no browser build started  
**Repository:** https://github.com/sandeepbimt/Sandium

## Current state

- [x] Independent Sandium repository exists.
- [x] Core project records and handoff protocol committed.
- [x] Documentation-only GitHub Actions workflow and validator committed.
- [x] Documentation validation workflow passes (run #4).
- [x] Cross-platform clean-base ledger and CI run-naming convention committed.
- [x] Evidence-driven automation contract and GitHub Actions run recorder committed (end-to-end run still needs verification).\n- [x] Automation decision, experiment record, operational risk and end-to-end acceptance checklist documented.
- [ ] Official Brave Android build feasibility is documented for a pinned revision.
- [ ] Sandium-only CI architecture is reviewed against the selected Brave revision.
- [ ] Sandium-specific CircleCI/BuildBuddy/Siso setup is independently validated.
- [ ] Reproducible Android APK is produced.

Do not mark work complete without evidence.

## Verified facts

- Repository: sandeepbimt/Sandium, default branch main.
- Documentation files and a documentation-only workflow exist on main.
- The docs validator is read-only and does not build the browser. A separate scheduled recordkeeper has Actions read / repository contents write permission to record completed GitHub runs; it must be verified end-to-end.
- No Sandium Android build result is established yet.
- SANDFOX is reference-only, not a build dependency.

## Current blocker

A reproducible, affordable Android build path and safe checkpoint/cache strategy must be established before expensive builds. Chromium's official Android instructions require at least 100 GB free disk and recommend more than 16 GB RAM; a standard hosted GitHub runner is not an adequate assumption for a full build.

## Single next action

Complete a pinned-revision feasibility report: verify the selected Brave Core revision, its Chromium pin, toolchain, build targets, storage/RAM requirements, and a genuinely available free/persistent Linux x86-64 builder. Do not start a Brave build until the report and approval gate are satisfied.

## Records

- [Charter](SANDIUM_STARTER.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md) · [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md)
- [Automation contract](SANDIUM_AUTOMATION_RULES.md) · [Recordkeeper](.github/workflows/project-recordkeeper.yml) · [Recorder script](.github/scripts/record_workflow_evidence.py)\n- [Documentation validator](.github/scripts/validate_docs.py) · [Validation workflow](.github/workflows/docs-validation.yml) · [Automation test plan](SANDIUM_TEST_PLAN.md)

## Update rule

Update after every meaningful session and consequential experiment. Record confirmed state only; label hypotheses explicitly.

<!-- SANDIUM_AUTO_STATUS_START -->
- **Latest observed completed GitHub run:** Sandium documentation validation / run #18 (failure) — https://github.com/sandeepbimt/Sandium/actions/runs/38997172822
- **Commit:** `f1738ad11f04457ca636dddc8b76b7d692b35985`; branch `main`
- **Boundary:** GitHub evidence is polled automatically. CircleCI is not covered until a Sandium-only integration is configured and tested. ChatGPT must still record decisions and findings GitHub cannot observe.
<!-- SANDIUM_AUTO_STATUS_END -->
