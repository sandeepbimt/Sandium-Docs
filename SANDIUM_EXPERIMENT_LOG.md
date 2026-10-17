# SANDIUM — Experiment Ledger

Append one record per consequential experiment, including failed, interrupted and inconclusive runs. IDs are never reused. Link exact commits, workflow runs, logs and artifacts.

## Template

### EXP-XXX — Objective
- **Status:** PLANNED | RUNNING | PASS | FAIL | INCONCLUSIVE | INTERRUPTED
- **Date:**
- **Question:**
- **Hypothesis and falsification:**
- **Baseline:** Repository, branch, commit, config and restored state.
- **Exact change / command:**
- **Environment:** Runner, OS, CPU, RAM, disk and tool versions.
- **Expected / actual cost:** Runtime, resources, retries and spend.
- **Evidence:** Run URL, stage/job IDs, logs, metrics and artifacts.
- **Observed result:**
- **Conclusion:** VERIFIED | HYPOTHESIS | REJECTED | INCONCLUSIVE
- **What it proves / unknowns:**
- **Learning / prevention rule:**
- **Related failure / decision IDs:**
- **Next action:** One action or NONE.

---

## Experiment history

No Sandium Android build or CI experiment has been run. Documentation-only validation should also be recorded if it changes the automation design.

## ID allocation and automation

Choose the next unused ID after checking this ledger and any structured records. Automation must use repository plus workflow run ID as an idempotency key so reruns do not create duplicate records.


### EXP-AUTO-001 — Evidence-driven recordkeeping

- **Status:** RUNNING (implementation committed; end-to-end validation pending)
- **Date:** 2026-10-17
- **Question:** Can Sandium maintain factual GitHub run records automatically while leaving semantic decisions to ChatGPT, with no manual user maintenance?
- **Hypothesis and falsification:** A scheduled GitHub Actions workflow can ingest completed workflow metadata and commit records idempotently. Falsified if it fails to fetch runs, misclassifies docs-only runs, creates duplicates/idle commits, cannot push, or triggers browser builds.
- **Baseline:** Repository sandeepbimt/Sandium, branch main; no browser build workflow or APK established.
- **Exact change / command:** Added SANDIUM_AUTOMATION_RULES.md, .github/scripts/record_workflow_evidence.py, .github/workflows/project-recordkeeper.yml, and updates to validator/status/handoff/charter.
- **Environment:** GitHub Actions ubuntu-latest; workflow uses repository GITHUB_TOKEN; no external paid service configured.
- **Expected / actual cost:** Expected low-cost scheduled metadata polling only; actual runtime/spend not yet measured.
- **Evidence:** [Recordkeeper workflow](.github/workflows/project-recordkeeper.yml), [recorder](.github/scripts/record_workflow_evidence.py), [validator](.github/scripts/validate_docs.py).
- **Observed result:** Files committed. End-to-end workflow result and resulting commit are not yet verified.
- **Conclusion:** HYPOTHESIS pending.
- **What it proves / unknowns:** Design intent is recorded. API permissions, successful run ingestion, idempotency, failure handling and automatic commit are still unknown.
- **Learning / prevention rule:** Do not conflate committed code with working automation; validate the complete trigger → run → record update → commit path.
- **Related failure / decision IDs:** OPS-001; DEC-004.
- **Next action:** Inspect the recordkeeper workflow run, fix any errors, and verify the exact generated changes without starting a browser build.
