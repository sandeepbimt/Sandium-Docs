> **SOURCE BOUNDARY — 2026-10-25:** Current browser source is Bare Browser only. Read [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md) before interpreting this historical record. Older source-specific experiments, pins, cache identities and build assumptions are superseded; preserve them as history but do not reuse them as current technical guidance. The existing Sandium GitHub/CircleCI/BuildBuddy/Siso integration and credential assignments must be preserved. Do not clear caches or trigger builds during source migration.

---

# SANDIUM — Clean-Base Ledger

**Purpose:** Authoritative, append-only record of every CI run proposed as a clean base, whether it runs through GitHub Actions, CircleCI, or both. A green run is not automatically a clean base; it must satisfy the declared scope and evidence gates.

## Rules

- One row per candidate run; never overwrite prior outcomes. Corrections are appended with a link to the superseded entry.
- Capture both GitHub and CircleCI identities when both participate. If a system was not involved, write `N/A`; do not infer.
- Record exact repository URL, branch, commit SHA, CircleCI project/pipeline/workflow/job, GitHub workflow/run/job, and the exact config file path and commit containing it.
- Give every CircleCI workflow a meaningful purpose-oriented name. Identify each individual run by the workflow name plus CircleCI pipeline number/ID and source commit; do not rely on a generic label such as “Build” or “Release”.
- A candidate is not a clean base until source/config identity, stated scope, build/test results, artifact integrity, and exclusions are recorded. Preserve logs and artifact links.
- Never record secret values, tokens, signing credentials, or sensitive environment values.
- Distinguish facts observed in logs from interpretations. Use `UNKNOWN` where evidence is missing.
- No candidate build may run until the project's feasibility and approval gates are satisfied.

## Naming convention

**CircleCI workflow name:** `sandium-<purpose>-<achievement-or-stage>`

Examples (use only when they accurately describe the run):
- `sandium-docs-validation`
- `sandium-source-preflight`
- `sandium-checkpoint-restore-validation`
- `sandium-android-debug-apk`

For a specific run, use a stable identity in records and handoffs:
`<workflow-name> | pipeline #<number> | <short-commit-sha> | <YYYY-MM-DD>`

Job names should also describe their actual responsibility, e.g. `verify-source-pins`, `validate-checkpoint-restore`, `verify-apk-integrity`. Do not create extra CI runs solely to test naming; introduce meaningful names with the next justified CI change. If CircleCI's UI does not support arbitrary per-run display names, keep the workflow name meaningful and use the pipeline number/ID plus commit SHA as the unique run identity.

## Candidate clean-base entry template

### CB-XXX — <short purpose / achievement>

- **Status:** CANDIDATE | ACCEPTED CLEAN BASE | REJECTED | SUPERSEDED
- **Recorded on:**
- **Purpose / intended change:**
- **Achievement / acceptance criteria:**
- **GitHub repository URL:**
- **GitHub branch / commit SHA:**
- **GitHub workflow file / workflow name / run URL / run ID:**
- **GitHub job IDs and results:**
- **CircleCI project slug / project URL:**
- **CircleCI config path:**
- **CircleCI config commit SHA:**
- **CircleCI workflow name:**
- **CircleCI pipeline number / pipeline ID / URL:**
- **CircleCI workflow and job names / job IDs:**
- **Source pins:** Brave Core, Chromium, Sandium patch-set, toolchain, GN args
- **Build target / command:**
- **Run type:** docs-only | preflight | compile | artifact build | tests
- **Clean-base predecessor (CB ID and source commit):**
- **What was achieved (evidence-linked):**
- **Tests and outcomes:**
- **Artifact path / URL / size / SHA-256 / integrity check:**
- **Logs / diagnostics URLs:**
- **Cache/checkpoint identity and evidence of reuse or forward progress:**
- **Runtime / resource usage / cost (or UNKNOWN):**
- **Known limitations / failures / exclusions:**
- **Why this qualifies or does not qualify as a clean base:**
- **Rollback / recovery notes:**
- **Related experiment, decision and failure-learning entries:**

## Ledger

No Sandium browser CI run has yet been executed or accepted as a clean base.

| ID | Date | Candidate purpose | GitHub repo / commit | GitHub workflow/run | CircleCI workflow/pipeline | Config path + commit | Outcome / achievement | Artifact + SHA-256 | Decision |
|---|---|---|---|---|---|---|---|---|---|
| — | — | No browser CI run yet | — | — | — | — | — | — | No clean base established |


## Automation classification rule

The GitHub recorder may append an entry here only for a relevant build/artifact workflow that actually reports artifacts, and must label it CANDIDATE ONLY. Documentation validation, recordkeeper runs, generic CI checks and other non-build workflows must not be entered as clean-base candidates. An artifact alone does not establish a clean base: source/config identity, integrity/checksum, install or smoke-test evidence, and required test results must be present before acceptance. The recorder is committed but its end-to-end behavior remains unverified.
