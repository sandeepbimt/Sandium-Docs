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


## DEC-004 — Automated project recordkeeping with decisive triggers

- **Status:** ACCEPTED
- **Date:** 2026-10-17
- **Problem:** The user will rely on Sandium's records and will not manually maintain Markdown, ledgers or handoffs. Stale or incomplete records would break continuity and cause repeated work.
- **Evidence:** Explicit user instruction in the 2026-10-17 project conversation; automation contract and recorder files committed in the Sandium repository.
- **Decision:** Recordkeeping is a system responsibility. GitHub Actions records machine-observable workflow outcomes and related evidence; ChatGPT updates semantic records from each session. Every consequential event must trigger the specific files listed in [SANDIUM_AUTOMATION_RULES.md](SANDIUM_AUTOMATION_RULES.md). The clean-base ledger must contain only actual build/artifact candidates, not arbitrary green documentation workflows.
- **Triggers:** Completed/failed/cancelled CI runs; artifact creation; tests; source pin/toolchain/config/cache changes; decisions made in chat; failure diagnoses; and session handoff.
- **Trust boundaries:** Unknown facts stay UNKNOWN. A green run is not a clean base. No browser build is triggered by recordkeeping. SANDFOX remains reference-only.
- **Current limitation:** GitHub recordkeeper is committed but end-to-end operation is not yet verified; CircleCI integration is pending; ChatGPT must still write conversation-derived decisions.
- **Validation criteria:** Demonstrate correct idempotent recording of a real completed run; correct failure classification; no docs-only run falsely entered as a clean base; valid commit and links; no idle-poll commit; no browser build trigger.
- **Revisit when:** End-to-end tests expose a flaw or automation requires a safer architecture.


### DEC-005 — Use CircleCI orchestration with Brave-native Siso and BuildBuddy REAPI

- **Status:** ACCEPTED (architecture direction only; no CI build is authorized by this entry)
- **Date:** 2026-10-17
- **Problem:** Sandium needs a realistic Android build path within CircleCI runtime/storage constraints without making local Chromium compilation the default.
- **Evidence:** Sandium source commit 06cd65a7e4fcea784e73c6deb9e4ce52889dc710; Brave Core 1.100.10; Chromium pin 156.0.8078.39; reviewed config.ts, syncUtils.ts, sisoUtils.ts and buildOptions.ts; SANDFOX M151 remote compile checkpoint; current CircleCI runtime/resource documentation.
- **Prior learning reviewed:** SANDFOX's real remote compile proved one C++ action ran remotely, but counters showed cache:0. Its full APK flow was not proven complete inside the one-hour job ceiling. Checkpoint history showed that archive presence does not prove valid Siso restore or forward progress.
- **Options considered:** Local compile on CircleCI; transplant Afterbird's pipeline; use Brave's native RBE path with a Sandium-owned backend override; stop pending a new provider.
- **Decision and rationale:** Pursue CircleCI as orchestrator/source workspace, Brave-native Siso as build scheduler/client, and BuildBuddy REAPI as remote executor and possible action cache. Do not transplant the Afterbird pipeline wholesale because Brave has its own .env, gclient and Siso generation, and defaults to google.star. Keep remote execution opt-in.
- **Trade-offs and risks:** Source/dependency sync, GN generation, local-only actions, packaging and tests still consume CircleCI time. Brave also adds -config googlechrome when RBE is configured; compatibility is unverified. The M156 pin and complete APK output are untested.
- **Isolation requirements:** Use a Sandium-specific CircleCI project/context/key and independently verified BuildBuddy instance/cache namespace. Never reuse SANDFOX credentials, cache entries, checkpoints, artifacts, workflows, or source checkout as dependencies. A separate key does not prove cache isolation.
- **Validation criteria:** Before any build, establish provider access, cache scope, costs, exact source/toolchain identity and test plan. An approved remote compile must capture remote/local/cache counters, output, invocation ID and diagnostics. Full APK success additionally requires artifact checksum/integrity, installation and smoke-test evidence.
- **Rollback:** Keep remote execution disabled by default and revert only Sandium-specific configuration if remote behavior is unproven.
- **Revisit when:** CircleCI project/resources and BuildBuddy account capabilities are verified or pinned Brave Siso behavior requires a different configuration.
- **Related record:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md).

## DEC-006 — Five-stage, reuse-first CI acceptance contract

- **Status:** ACCEPTED
- **Date:** 2026-10-17
- **Problem:** Avoid repeating expensive Chromium source synchronization, build-graph generation, compilation and handover work across stages and future runs; prevent a stage from consuming the full one-hour CI limit; stop promptly once a valid APK exists.
- **Evidence:** Explicit user requirements recorded on 2026-10-17; criteria are now written in [SANDIUM_TEST_PLAN.md](SANDIUM_TEST_PLAN.md) and reflected in [SANDIUM_CI_ARCHITECTURE.md](SANDIUM_CI_ARCHITECTURE.md).
- **Prior learning reviewed:** Prior SANDFOX experiments demonstrated that full build work can repeat and that cache/archive presence alone does not prove restoration or forward progress. SANDFOX remains reference-only; none of its infrastructure or artifacts may be used as dependencies.
- **Decision and rationale:** Sandium CI must have exactly five sequential, purpose-defined stages. Each stage does definitive work only and consumes validated previous-stage state. Design for at most 50 minutes end-to-end per stage, including all preparation and handover, to leave margin under the one-hour job ceiling. Persist and prove same-run and cross-run reuse. If any stage produces a complete, integrity-checked APK matching the requested build identity, persist it with its manifest and require every downstream stage to skip expensive work and exit quickly.
- **Trade-offs and risks:** Persistent checkpoints and caches increase storage/transfer and invalidation complexity. Incorrect keys or incomplete manifests can cause stale reuse; correctness checks take priority over the fast path. Actual reuse, time limits and fast-skip behavior remain unvalidated.
- **Validation criteria:** Satisfy the complete checklist in the CI section of [SANDIUM_TEST_PLAN.md](SANDIUM_TEST_PLAN.md), including cold run, same-run handover, warm cross-run reuse, early APK fast path, and corruption/change invalidation tests. Preserve stage durations, handover timings, action/output counters, source/config identity, logs and artifact SHA-256.
- **Rollback:** Do not silently weaken these criteria or change the required stage count. If pinned Brave/Siso or provider limits make a criterion infeasible, document the specific evidence and obtain an explicit decision before changing the contract.
- **Revisit when:** Measured implementation evidence or a verified upstream/provider constraint proves a requirement infeasible.

## DEC-007 — Use the pinned Chromium non-Google REAPI path for BuildBuddy

- **Status:** PROPOSED — source-supported design; not yet implemented or runtime-validated.
- **Date:** 2026-10-17
- **Problem:** Brave's default RBE configuration selects google.star and the default instance; BuildBuddy needs an explicit, isolated, reproducible non-Google backend.
- **Evidence:** Sandium pins Chromium 156.0.8078.39 and Siso c574896b272b40aac6e44c228ee0b471ea7e3d7d. Chromium DEPS passes reapi_address, reapi_instance, reapi_backend_config_path and reapi_credential_helper to configure_siso.py. Brave merges projects_chrome_custom_vars after rbe_service-derived defaults. Chromium's official non-Google RBE guide documents a custom backend.star and the digest-pinned siso-chromium Linux image. BuildBuddy documents remote.buildbuddy.io as its managed REAPI endpoint, x-buildbuddy-api-key auth, and REAPI instance namespaces.
- **Prior learning reviewed:** SANDFOX M151 proves only a single remote compile action and is reference-only. It does not prove Siso M156 integration, cache reuse, APK creation, or BuildBuddy account behavior.
- **Options considered:** Rely on Brave's google.star/default defaults; adapt the existing BuildBuddy backend Star only; explicitly override all REAPI vars and use a host-scoped credential helper; change build systems.
- **Decision and rationale:** Proposed implementation should explicitly set the BuildBuddy endpoint, stable Sandium instance, backend Star path and executable credential-helper path through Brave's supported custom-var overlay. Use the upstream digest-pinned Chromium/Siso image as the first candidate, without Google's worker labels. Store only the API key in protected CircleCI secret storage. Keep siso_use_googlechrome_config=false for the first connection/action qualification because the preset is documented as Google-RBE-specific; qualify its broader remote rules separately for performance.
- **Trade-offs and risks:** Account entitlement, image pulls, instance acceptance, the exact pinned Siso helper path, remote action compatibility, and performance are unverified. The proposed namespace is not an authorization boundary. Large source handoff may be the dominant five-stage bottleneck; do not assume a complete source snapshot can fit the stage budget.
- **Validation criteria:** First run deterministic offline helper tests with fake credentials and URIs; then generate .sisoenv/backend.star using Chromium's pinned configure_siso.py in a temporary layout without network access. After explicit authorization, use pinned Siso auth-check (no compile) and then one measured, meaningful Chromium action. Only later consider a full APK build and the five-stage acceptance demonstrations.
- **Rollback:** Keep remote execution disabled by default; remove the Sandium-specific runtime configuration or revert its isolated source patch without changing SANDFOX.
- **Revisit when:** The pinned Siso/BuildBuddy connection and image pull have passed, or source/provider evidence requires a different backend config.
- **Related records:** [SANDIUM_REMOTE_BUILD_DESIGN.md](SANDIUM_REMOTE_BUILD_DESIGN.md), [SANDIUM_TEST_PLAN.md](SANDIUM_TEST_PLAN.md).
