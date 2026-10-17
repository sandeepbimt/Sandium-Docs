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
