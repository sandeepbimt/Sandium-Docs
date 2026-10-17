# SANDIUM — Chat Handoff

Purpose: resume from repository evidence without reconstructing history from chat memory.

## Current handoff

- **Repository:** https://github.com/sandeepbimt/Sandium
- **Branch:** main
- **Phase:** Isolated BuildBuddy adapter source patch and offline validation completed on review/sandium-buildbuddy-backend-2026-10-17. Fourteen unit tests passed; the exact pinned Chromium configure_siso.py generated the expected .sisoenv and copied backend.star byte-for-byte in a temporary workspace. No Siso auth-check, REAPI request, source sync, CircleCI build, compile or APK run has occurred.
- **Required CI acceptance contract:** exactly five sequential stages; definitive work only; 50-minute end-to-end stage target including prep/handover and a strict under-one-hour ceiling; proven same-run and cross-run Chromium/build-state reuse; downstream fast-skip within 60 seconds after a matching, integrity-checked APK is durably published; and measured end-to-end speed optimization across CircleCI, Brave-native Siso and BuildBuddy. Detailed acceptance and evidence criteria are in the [test plan](SANDIUM_TEST_PLAN.md) and [CI architecture](SANDIUM_CI_ARCHITECTURE.md); not implemented or validated.
- **Charter:** [SANDIUM_STARTER.md](SANDIUM_STARTER.md)
- **Status:** [SANDIUM_STATUS.md](SANDIUM_STATUS.md)
- **Remote build design:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md) records the proposed Brave-native Siso/BuildBuddy adapter and rollout gates.
- **Preflight branch:** [ci/sandium-buildbuddy-siso-preflight](https://github.com/sandeepbimt/Sandium/tree/ci/sandium-buildbuddy-siso-preflight), commit 3610ff348694d9cf923dbcffaf633017fade4edc. Its only job is parameter-gated and performs no source sync, BuildBuddy request or compilation.
- **Must-read learnings:** [SANDIUM_KNOWLEDGE.md](SANDIUM_KNOWLEDGE.md)
- **Detailed records:** Follow links in status and knowledge index.
- **Documentation automation policy:** [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md) defines decisive event triggers. [Validator](.github/scripts/validate_docs.py), [docs validation workflow](.github/workflows/docs-validation.yml), [evidence recorder](.github/scripts/record_workflow_evidence.py), and [scheduled recordkeeper](.github/workflows/project-recordkeeper.yml) are committed. The recorder is intended to poll completed GitHub workflow runs and update machine-evidenced records; end-to-end execution must be verified. It must never build the browser. The user is not expected to edit Markdown manually.
- **Source-level investigation result:** Chromium DEPS at pin 156.0.8078.39 pins Siso c574896b272b40aac6e44c228ee0b471ea7e3d7d and passes the four non-Google REAPI settings to configure_siso.py. Brave's custom-var overlay can override google.star/default. The official Chromium non-Google RBE guide provides a digest-pinned Siso/Chromium executor image. Candidate endpoint: remote.buildbuddy.io:443; candidate stable instance: sandium/android-arm64/ci. Account auth/instance/image execution, exact pinned helper behavior, broad googlechrome preset compatibility, and five-stage transfer time remain unproven. Details and source references are in SANDIUM_REMOTE_BUILD_DESIGN.md.
- **Next action:** Seek separate explicit approval for the pinned Siso auth-check against BuildBuddy (no source sync/compile). Before any remote action, verify auth/instance/image behavior; before an APK run, establish stage handoff/cache timing and confirm the five-stage plan can meet the 50-minute target. Branch and test evidence are in SANDIUM_REMOTE_BUILD_DESIGN.md and SANDIUM_BUILD_NOTES.md. No PR/merge or CI run exists for the source-review branch. SANDFOX remains reference-only.
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
