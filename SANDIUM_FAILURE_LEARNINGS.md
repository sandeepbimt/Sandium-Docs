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
