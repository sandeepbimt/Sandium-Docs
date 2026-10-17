# SANDIUM — Chat Handoff

Purpose: resume from repository evidence without reconstructing history from chat memory.

## Current handoff

- **Repository:** https://github.com/sandeepbimt/Sandium
- **Branch:** main
- **Phase:** Documentation validation passes; official Brave build feasibility audit in progress. No Android build has run.
- **Charter:** [SANDIUM_STARTER.md](SANDIUM_STARTER.md)
- **Status:** [SANDIUM_STATUS.md](SANDIUM_STATUS.md)
- **Must-read learnings:** [SANDIUM_KNOWLEDGE.md](SANDIUM_KNOWLEDGE.md)
- **Detailed records:** Follow links in status and knowledge index.
- **Documentation automation:** [validator](.github/scripts/validate_docs.py) and [GitHub Actions workflow](.github/workflows/docs-validation.yml). This is documentation-only; it does not compile Brave or trigger browser builds.
- **Next action:** Complete the pinned-revision Brave Android build feasibility report; no build until the resource/cost/approval gates pass.
- **Clean-base governance:** [SANDIUM_CLEAN_BASE_LEDGER.md](SANDIUM_CLEAN_BASE_LEDGER.md) records exact GitHub + CircleCI identities, config path/commit, achievements, tests and artifact evidence. CircleCI workflow/job names must be purpose-oriented; each run is uniquely identified by workflow name + pipeline number/ID + source commit. Do not run CI solely for naming.
- **Do not:** Trigger builds before feasibility/cost is documented; use SANDFOX as a build dependency; assume cache/checkpoint behavior; store secrets.

## Session close checklist

1. Inspect repository commit and work performed this session.
2. Append consequential experiments, including failed/interrupted attempts, with links and actual costs where known.
3. Update failure learnings and decisions without erasing history.
4. Update knowledge index for reusable evidence-backed lessons.
5. Update build notes/test results when evidence changes.
6. Update status with confirmed state, blockers and exactly one next action.
7. Refresh this handoff with exact branch/commit/run/artifact links and must-not-repeat warnings.
8. Run documentation validation and review the diff.
9. Append every candidate clean base to the ledger, including rejected/failed candidates when they inform decisions.
10. Never claim a file was saved until the repository commit is verified.

## New-chat startup checklist

1. Read handoff and status.
2. Read charter and knowledge index.
3. Read relevant detailed decisions, experiments and failure records.
4. Verify repository/branch/commit and workflow state.
5. Resolve contradictions against source/log evidence.
6. State verified current state and one next action before editing or running anything.
