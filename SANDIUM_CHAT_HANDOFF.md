# SANDIUM — Chat Handoff

Purpose: resume from repository evidence without reconstructing history from chat memory.

## Current handoff

- **Repository:** https://github.com/sandeepbimt/Sandium
- **Branch:** main
- **Phase:** Brave-native CircleCI + BuildBuddy + Siso integration reviewed and documented. A disabled-by-default no-build preflight is staged on Sandium branch ci/sandium-buildbuddy-siso-preflight; CircleCI project linkage, secrets, server validation and run remain unverified. No Android build has run.
- **Required CI acceptance contract:** exactly five sequential stages; each does definitive work only; 50-minute end-to-end stage target with all handover/preparation counted and a strict under-one-hour ceiling; proven same-run and cross-run Chromium/build-state reuse; downstream fast-skip within 60 seconds after a matching, integrity-checked APK is durably published. This is documented in the [test plan](SANDIUM_TEST_PLAN.md) and [CI architecture](SANDIUM_CI_ARCHITECTURE.md), not yet implemented or validated.
- **Charter:** [SANDIUM_STARTER.md](SANDIUM_STARTER.md)
- **Status:** [SANDIUM_STATUS.md](SANDIUM_STATUS.md)
- **Remote build design:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md) records the proposed Brave-native Siso/BuildBuddy adapter and rollout gates.
- **Preflight branch:** [ci/sandium-buildbuddy-siso-preflight](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight), commit 3610ff348694d9cf923dbcffaf633017fade4edc. Its only job is parameter-gated and performs no source sync, BuildBuddy request or compilation.
- **Must-read learnings:** [SANDIUM_KNOWLEDGE.md](SANDIUM_KNOWLEDGE.md)
- **Detailed records:** Follow links in status and knowledge index.
- **Documentation automation policy:** [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md) defines decisive event triggers. [Validator](.github/scripts/validate_docs.py), [docs validation workflow](.github/workflows/docs-validation.yml), [evidence recorder](.github/scripts/record_workflow_evidence.py), and [scheduled recordkeeper](.github/workflows/project-recordkeeper.yml) are committed. The recorder is intended to poll completed GitHub workflow runs and update machine-evidenced records; end-to-end execution must be verified. It must never build the browser. The user is not expected to edit Markdown manually.
- **Next action:** Continue the read-only compatibility review of the pinned Siso revision and BuildBuddy REAPI contract: verify endpoint/instance semantics, the exact credential-helper contract and cache isolation. Only after the evidence is clear should the Sandium-only no-build preflight be considered. No source sync or APK build yet.
- **Clean-base governance:** [SANDIUM_CLEAN_BASE_LEDGER.md](SANDIUM_CLEAN_BASE_LEDGER.md) records exact GitHub + CircleCI identities, config path/commit, achievements, tests and artifact evidence. CircleCI workflow/job names must be purpose-oriented; each run is uniquely identified by workflow name + pipeline number/ID + source commit. Do not run CI solely for naming.
- **Do not:** Ask the user to manually update records; claim automation works before end-to-end verification; trigger builds before feasibility/cost is documented; use SANDFOX as a build dependency; assume cache/checkpoint behavior; store secrets.

## Session close protocol (owned by ChatGPT, not the user)

1. Inspect repository commit and work performed this session.
2. Apply the triggers in [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md): preserve experiments/failures, decisions, reusable knowledge, build/test evidence, status and handoff.
3. Append candidate clean bases and rejected/failed candidates when they inform decisions; never promote a green run without artifact and test evidence.
4. Run documentation validation, review the diff and verify the repository commit.
5. Report what was updated and what remains unautomated; never tell the user to manually update these records.

## New-chat startup checklist

1. Read handoff and status.
2. Read charter and knowledge index.
3. Read relevant detailed decisions, experiments and failure records.
4. Verify repository/branch/commit and workflow state.
5. Resolve contradictions against source/log evidence.
6. State verified current state and one next action before editing or running anything.

<!-- SANDIUM_AUTO_STATUS_START -->
- No completed GitHub workflow run was available from the API.\n
<!-- SANDIUM_AUTO_STATUS_END -->
