# SANDIUM — Documentation Automation Contract

**Policy:** Human-maintained Markdown is not an acceptable operating model. The owner is not expected to edit project records. The repository and CI evidence are the source of truth; ChatGPT must update the repository records during work sessions when the conversation contains decisions or evidence that GitHub cannot observe.

## Automation tiers and trust boundaries

1. **Machine facts — update automatically.** Commit SHA, branch, workflow/pipeline/run/job IDs, timestamps, conclusion, logs, artifacts, checksums, test outputs, source pins, config paths, durations, and links are written only from the corresponding API, command output, or artifact.
2. **Derived state — update automatically from machine facts.** Current status, latest verified commit/run, pass/fail counts, outstanding gates, and handoff links are regenerated from repository evidence. Never infer success from a green job if artifact/test checks did not pass.
3. **Engineering interpretation — ChatGPT owns updates.** During each work session, ChatGPT updates decisions, knowledge, failure learnings, experiment interpretation, test-plan changes, build notes, and handoff from the actual conversation and logs. The user must not be asked to maintain these files manually.
4. **Unknowns remain unknown.** Missing credentials, unavailable APIs, incomplete logs, missing artifacts, or unverified cache restoration are explicitly recorded as UNKNOWN/UNVERIFIED, never guessed.
5. **No false clean bases.** A successful CI run is only a candidate. Accept a clean base only when the exact source/config, APK artifact, integrity/checksum, install or smoke-test evidence, and required tests are captured. Rejected candidates remain in the ledger with reasons.
6. **Preserve history.** Experiment and clean-base ledgers are append-only. Correct errors by adding a correction/superseding entry, not silently deleting past outcomes. Decisions are marked superseded, not erased.
7. **No secret capture.** Never write tokens, keys, credentials, signed URLs with sensitive query values, or environment dumps to Markdown, logs, artifacts, or summaries.
8. **No expensive build from a recorder trigger.** Documentation automation must never trigger a browser build. Build execution remains behind a separately reviewed feasibility/cost/approval gate.
9. **No cross-project coupling.** SANDFOX is reference-only. Do not read its credentials/caches/artifacts as dependencies or modify its infrastructure.
10. **Fail visibly.** If an updater fails or lacks permission, the workflow must fail and report the exact missing permission/secret/evidence. Do not silently report the records as current.

## Decisive update triggers

| Trigger / event | Automatic record changes |
|---|---|
| Any Sandium CI workflow completes | Clean-base ledger gets a run entry; experiment log gets outcome and links; status/handoff refresh from latest verified run. |
| CI fails, is cancelled, times out, or is skipped after starting | Append failure/limitation to failure learnings with exact run/log links and what is/isn't proved; never overwrite an earlier diagnosis. |
| APK/build artifact is produced | Build notes and ledger record artifact name/link/size/checksum where obtainable, source/config pins, and verification status. Artifact presence alone does not mean install/test success. |
| Test suite or device smoke test completes | Test plan/build notes record exact test result, device/environment, build SHA and evidence; status gates change only when their criteria are met. |
| Source revision, Chromium pin, toolchain, build target, CI config, cache/checkpoint scheme changes | Re-run source preflight/targeted validation; record changed pins/config SHA, decision rationale, and whether the prior clean base remains compatible. |
| Cache/checkpoint restore is attempted | Record cache key, source identity, restored state, action/item counts, logs, elapsed time and explicit proof of reuse. A cache hit label alone is insufficient. |
| A design/architecture/priority decision is made in ChatGPT | ChatGPT updates decisions, knowledge, status and handoff in the same work session; user is not asked to edit files. |
| An experiment is proposed, started, interrupted or concluded in ChatGPT | ChatGPT updates experiment log before moving to another experiment; failures and wasted runs are retained. |
| A failure is diagnosed or an earlier diagnosis changes | ChatGPT appends the evidence, root-cause confidence, rejected hypotheses, smallest justified fix and non-repeat warning. |
| Session ends, context is near limit, or user requests a handoff | ChatGPT reconciles the repo with the conversation, updates all affected records, validates links, and leaves one next action. |
| Documentation changes | Validator checks required files, links, newline/format rules and safeguards. Validation itself is not proof that semantic records are current. |
| CircleCI pipeline completes | A Sandium-only CircleCI webhook or authenticated polling integration must ingest pipeline/workflow/job/artifact metadata into the same ledger. Until a Sandium-specific token/webhook is configured and tested, CircleCI events are NOT automatically covered. |
| ChatGPT conversation changes without a repo event | GitHub cannot read private ChatGPT history by itself. ChatGPT must commit the session's decisions and findings directly; no GitHub-only workflow can infer unseen conversation content. |

## Update order for ChatGPT work sessions

1. Read status, handoff, knowledge and relevant detailed records.
2. Verify the repository, branch, commit and run evidence before changing anything.
3. Record the experiment/result and failures first, including failed or cancelled attempts.
4. Update decisions/knowledge only when the conversation establishes a durable conclusion; label confidence and evidence.
5. Update build notes/test plan when source, build, artifact or test evidence changes.
6. Regenerate status and handoff last, with exactly one next action and links to evidence.
7. Run documentation validation and inspect the resulting diff/commit.
8. Report what was actually updated, commit IDs, what remains unknown, and whether any integration is not yet automated.

## Automation maturity (must remain honest)

- **Implemented initially:** deterministic Markdown validation.
- **Required next:** automatic ingestion of GitHub workflow completions and generated evidence summaries.
- **Not automatically available from GitHub alone:** private ChatGPT conversation semantics and CircleCI events without an explicitly configured Sandium-only integration.
- **Never claim full automation** until GitHub run ingestion, CircleCI ingestion (if CircleCI is used), artifact/test evidence, and session handoff updates have each been demonstrated end-to-end.


## Current implementation status (2026-10-17)

- **Committed:** Automation contract, GitHub Actions recordkeeper, evidence recorder, validator checks, decision DEC-004, experiment EXP-AUTO-001, operational risk OPS-001, and end-to-end acceptance criteria.
- **Not yet proven:** The complete trigger → GitHub API read → correctly classified record update → commit/push path has not been verified end-to-end. Until that passes, describe the automation as implemented but unverified.
- **Record classification:** Every eligible non-documentation GitHub workflow outcome may be recorded in the experiment log. Build notes are updated only for build-related workflows. The clean-base ledger receives only relevant build-related runs that report artifacts, always as CANDIDATE ONLY. Documentation-validation and recordkeeper runs must not become clean-base candidates.
- **Current priority:** Verify the recordkeeper workflow and resulting commit before resuming browser-source feasibility work. No browser build may be triggered by this test.
- **CircleCI:** Pending a separately configured Sandium-only API/webhook integration. Do not use SANDFOX credentials, caches, artifacts or infrastructure.
- **No manual upkeep:** The user is not responsible for editing Markdown. ChatGPT updates conversation-derived findings in each session; automation captures machine evidence. If either layer misses an update, ChatGPT owns correcting the records and the automation design.


## Anti-loop and ledger-scope safeguards

- The recordkeeper must exclude its own runs and successful documentation-validation runs from new evidence entries.
- Failed or cancelled documentation-validation runs must still be recorded as failures, but never as clean-base candidates.
- The status/handoff "latest workflow" snapshot must exclude both recordkeeper and documentation-validation workflows. Otherwise each generated documentation commit can trigger validation, which can trigger another status commit indefinitely.
- When no relevant non-documentation workflow exists, record that fact instead of substituting a docs-only run as the latest project/build result.
- Idempotency means both no duplicate run entries and no idle commits. A scheduled timestamp alone must not change tracked files.
11. **Immutable source boundary.** Since 2026-10-25, Bare Browser and its pinned Chromium revision are the only active browser-source authority. Source-specific historical records are superseded and must not guide current implementation. The existing Sandium GitHub/CircleCI/BuildBuddy/Siso integration and credential assignments must be reused; recordkeeping must never trigger a browser build or recreate credentials.

