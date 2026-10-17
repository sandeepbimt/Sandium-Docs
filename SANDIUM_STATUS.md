# SANDIUM — Project Status

**Last reviewed:** 2026-10-17  
**Status:** Documentation validation passes; Brave build feasibility audit in progress  
**Repository:** https://github.com/sandeepbimt/Sandium

## Current state

- [x] Independent Sandium repository exists.
- [x] Core project records and handoff protocol committed.
- [x] Documentation-only GitHub Actions workflow and validator committed.
- [x] Documentation validation workflow passes (run #4).
- [x] Cross-platform clean-base ledger and CI run-naming convention committed.
- [ ] Official Brave Android build feasibility is documented for a pinned revision.
- [ ] Sandium-only CI architecture is reviewed against the selected Brave revision.
- [ ] Sandium-specific CircleCI/BuildBuddy/Siso setup is independently validated.
- [ ] Reproducible Android APK is produced.

Do not mark work complete without evidence.

## Verified facts

- Repository: sandeepbimt/Sandium, default branch main.
- Documentation files and a documentation-only workflow exist on main.
- The workflow is limited to documentation-related changes, pull requests, and manual dispatch; it has read-only repository permissions and does not build the browser.
- No Sandium Android build result is established yet.
- SANDFOX is reference-only, not a build dependency.

## Current blocker

A reproducible, affordable Android build path and safe checkpoint/cache strategy must be established before expensive builds. Chromium's official Android instructions require at least 100 GB free disk and recommend more than 16 GB RAM; a standard hosted GitHub runner is not an adequate assumption for a full build.

## Single next action

Complete a pinned-revision feasibility report: verify the selected Brave Core revision, its Chromium pin, toolchain, build targets, storage/RAM requirements, and a genuinely available free/persistent Linux x86-64 builder. Do not start a Brave build until the report and approval gate are satisfied.

## Records

- [Charter](SANDIUM_STARTER.md) · [Knowledge](SANDIUM_KNOWLEDGE.md) · [Decisions](SANDIUM_DECISIONS.md) · [Experiments](SANDIUM_EXPERIMENT_LOG.md) · [Failure learnings](SANDIUM_FAILURE_LEARNINGS.md) · [Build notes](SANDIUM_BUILD_NOTES.md) · [Test plan](SANDIUM_TEST_PLAN.md) · [Chat handoff](SANDIUM_CHAT_HANDOFF.md) · [CI architecture](SANDIUM_CI_ARCHITECTURE.md)
- [Documentation validator](.github/scripts/validate_docs.py) · [Validation workflow](.github/workflows/docs-validation.yml)

## Update rule

Update after every meaningful session and consequential experiment. Record confirmed state only; label hypotheses explicitly.
