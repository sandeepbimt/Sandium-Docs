# SANDIUM — Decision Register

Append decisions; never silently overwrite history. Supersede with a new linked entry.

## Template

### DEC-XXX — Title
- **Status:** PROPOSED | ACCEPTED | REJECTED | SUPERSEDED
- **Date:**
- **Problem:**
- **Evidence:** Exact revision, file, log, experiment or test.
- **Prior learning reviewed:**
- **Options considered:**
- **Decision and rationale:**
- **Trade-offs and risks:**
- **Validation criteria:**
- **Rollback:**
- **Revisit when:**

---

## DEC-001 — Keep all Sandium build work independent

- **Status:** ACCEPTED
- **Date:** 2026-10-17
- **Problem:** Avoid coupling to SANDFOX's experimental build history.
- **Evidence:** Explicit project requirement and independent repository.
- **Prior learning:** SANDFOX had costly experiments and uncertainty around cache/checkpoint behavior.
- **Options:** Direct reuse; independently implement reviewed ideas; ignore all prior learning.
- **Decision:** All Sandium code, CI, builds, artifacts, checkpoints and logs belong to Sandium or separately configured Sandium infrastructure. SANDFOX is reference-only.
- **Validation:** No SANDFOX workflow is triggered and no SANDFOX artifact/cache is a Sandium build dependency.
- **Revisit:** Only through explicit documented decision.

## DEC-002 — Documentation-first, evidence-based engineering

- **Status:** ACCEPTED
- **Date:** 2026-10-17
- **Problem:** Avoid repeated experiments and loss of learning across chats.
- **Evidence:** Project charter and explicit continuity requirement.
- **Decision:** Versioned GitHub documents are authoritative; consequential experiments include evidence, cost, outcome and learning; every session updates status and handoff. Deterministic facts may be automated; AI conclusions must be evidence-linked and reviewable.
- **Validation:** A new chat can reconstruct state from repository records and links.
- **Revisit:** If continuity tests fail or maintenance cost outweighs value.


## DEC-003 — Maintain an evidence-backed clean-base ledger and meaningful CI names

- **Status:** ACCEPTED
- **Date:** 2026-10-17
- **Problem:** Clean CI results can become untraceable across GitHub, CircleCI, configuration revisions and future chats; generic run names are hard to distinguish over time.
- **Evidence:** Explicit project requirements; prior CI work showed the importance of preserving exact commits, configs, outcomes and artifacts.
- **Decision:** Maintain [SANDIUM_CLEAN_BASE_LEDGER.md](SANDIUM_CLEAN_BASE_LEDGER.md) as an append-only record of candidate and accepted clean bases. Capture GitHub repository/workflow/run/job details and CircleCI project/pipeline/workflow/job details, exact config path and commit, source pins, achievement, test results, artifact hashes, logs, costs/resource usage and limitations. Use purpose-oriented CircleCI workflow/job names and identify each run by workflow name + pipeline number/ID + source commit. Never assume a green run is automatically a clean base.
- **Trade-offs and risks:** More record fields require discipline; unknown fields must be explicitly marked UNKNOWN rather than guessed. CircleCI may not support arbitrary per-run display names, so stable IDs in the ledger remain authoritative.
- **Validation criteria:** A future reviewer can identify the exact repository, config revision, pipeline run, achievement and evidence for any accepted clean base without relying on chat history.
- **Rollback:** None; entries are append-only and may be superseded with a linked explanation.
- **Revisit when:** CI provider capabilities or the project workflow changes.
