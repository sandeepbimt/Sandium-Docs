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


### FAIL-AUTO-002 — Documentation validator syntax regression

- **Date / experiment ID:** 2026-10-17 / EXP-AUTO-001
- **Status:** CONFIRMED ROOT CAUSE
- **Source revision / configuration:** Commit f1738ad11f04457ca636dddc8b76b7d692b35985; documentation validation workflow.
- **Expected behavior:** Validator should parse and check the required document list.
- **Observed behavior:** GitHub Actions run #18 failed before checks ran.
- **Evidence:** [Failed run #18](https://github.com/sandeepbimt/Sandium/actions/runs/38997172822); log reported SyntaxError at validator line 13 because a literal backslash-n sequence was inserted into the Python list.
- **What it proves / does not prove:** It proves the validator source had a syntax error at that commit. It says nothing about browser build feasibility or recordkeeper operation.
- **Root cause:** Text replacement wrote the two characters \\n instead of a real newline in the REQUIRED list.
- **Fix / mitigation:** Corrected the list formatting in commit 63d0d723e5d8ee67e1725ab65bcf12dcb61f6223.
- **Validation:** Awaiting a new documentation workflow run against the fix commit.
- **Prevention rule:** Inspect fetched source after programmatic string edits; add syntax validation and verify actual workflow output.
- **Do not repeat unless:** Another validator regression occurs.
- **Related records:** [EXP-AUTO-001](SANDIUM_EXPERIMENT_LOG.md), [test plan](SANDIUM_TEST_PLAN.md).
