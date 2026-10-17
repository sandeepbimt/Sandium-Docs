# SANDIUM — Failure Learnings

Record significant failures and inconclusive runs. Unknown root cause is a valid result; do not invent one.

## Template

### FAIL-XXX — Description
- **Date / experiment ID:**
- **Status:** CONFIRMED ROOT CAUSE | PARTIAL EVIDENCE | UNKNOWN | SUPERSEDED
- **Source revision / configuration:**
- **Expected behavior:**
- **Observed behavior:**
- **Evidence:** Exact run/log/artifact URL and relevant lines.
- **What it proves / does not prove:**
- **Root cause:**
- **Fix / mitigation:**
- **Validation:**
- **Prevention rule:**
- **Do not repeat unless:**
- **Related records:**

---

## Current entries

No Sandium build failures are recorded because no Sandium Android build has run. This does not prove the build path works.

### Reference-only caution

SANDFOX history included costly build experiments and uncertainty around checkpoint restoration, Siso state, remote cache hits and forward progress. These are cautionary prompts, not Sandium-specific verified failures. Sandium must validate its own implementation independently.


### OPS-001 — Recordkeeper not yet end-to-end verified

- **Date:** 2026-10-17
- **Status:** PARTIAL EVIDENCE
- **Source revision / configuration:** Sandium main; see [recordkeeper workflow](.github/workflows/project-recordkeeper.yml) and [evidence recorder](.github/scripts/record_workflow_evidence.py).
- **Expected behavior:** Poll completed GitHub Actions runs, record factual evidence idempotently, and update the appropriate records without triggering a browser build.
- **Observed behavior:** The contract, scheduled workflow and recorder have been committed. No end-to-end recorder result has yet been verified.
- **Evidence:** Repository files are present; workflow execution and generated commit remain to be inspected.
- **What it proves / does not prove:** File presence proves implementation was committed, not that API permissions, parsing, idempotency, Markdown updates, or push permissions work.
- **Root cause:** UNKNOWN; no failure has yet been confirmed.
- **Fix / mitigation:** Validate recorder Python syntax, inspect the workflow run and its logs, then verify any resulting commit and record classification. Ensure docs-only workflows do not become clean-base candidates.
- **Validation:** Pending.
- **Prevention rule:** Never claim recordkeeping is fully automated until a real end-to-end run passes.
- **Do not repeat unless:** A new failure or regression occurs.
- **Related records:** [Automation rules](SANDIUM_AUTOMATION_RULES.md), [Decision DEC-004](SANDIUM_DECISIONS.md), [Test plan](SANDIUM_TEST_PLAN.md).
