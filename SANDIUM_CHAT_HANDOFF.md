# SANDIUM — Chat Handoff

Purpose: resume from repository evidence without reconstructing history from chat memory.

## Current handoff

- **Repository:** https://github.com/sandeepbimt/Sandium
- **Branch:** main
- **Phase:** Recordkeeping automation implementation committed; end-to-end verification pending. No Android build has run.
- **Charter:** [SANDIUM_STARTER.md](SANDIUM_STARTER.md)
- **Status:** [SANDIUM_STATUS.md](SANDIUM_STATUS.md)
- **Must-read learnings:** [SANDIUM_KNOWLEDGE.md](SANDIUM_KNOWLEDGE.md)
- **Detailed records:** Follow links in status and knowledge index.
- **Documentation automation policy:** [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md) defines decisive event triggers. [Validator](.github/scripts/validate_docs.py), [docs validation workflow](.github/workflows/docs-validation.yml), [evidence recorder](.github/scripts/record_workflow_evidence.py), and [scheduled recordkeeper](.github/workflows/project-recordkeeper.yml) are committed. The recorder is intended to poll completed GitHub workflow runs and update machine-evidenced records; end-to-end execution must be verified. It must never build the browser. The user is not expected to edit Markdown manually.
- **Next action:** Verify the recordkeeper end-to-end: inspect its workflow run/logs, fix failures, confirm no duplicate/idle commits and no docs-only clean-base entries, then inspect the resulting commit. Do not start a browser build during this check. After recordkeeping is proven, resume pinned-revision Brave feasibility.
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
- **Latest observed completed GitHub run:** Sandium documentation validation / run #18 (failure) — https://github.com/sandeepbimt/Sandium/actions/runs/38997172822
- **Commit:** `f1738ad11f04457ca636dddc8b76b7d692b35985`; branch `main`
- **Boundary:** GitHub evidence is polled automatically. CircleCI is not covered until a Sandium-only integration is configured and tested. ChatGPT must still record decisions and findings GitHub cannot observe.
<!-- SANDIUM_AUTO_STATUS_END -->
