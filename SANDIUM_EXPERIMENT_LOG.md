> **SOURCE BOUNDARY — 2026-10-25:** Current browser source is Bare Browser only. Read [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md) before interpreting this historical record. Older source-specific experiments, pins, cache identities and build assumptions are superseded; preserve them as history but do not reuse them as current technical guidance. The existing Sandium GitHub/CircleCI/BuildBuddy/Siso integration and credential assignments must be preserved. Do not clear caches or trigger builds during source migration.

---

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

No Sandium Android build has been run. A lightweight CircleCI preflight attempt failed before BuildBuddy access because SANDIUM_REAPI_ADDRESS was unset at that time; the attempt did not perform source sync or compile. EXP-SISO-001 records the offline adapter/configuration test. Documentation-only validation should also be recorded if it changes the automation design.

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


### EXP-AUTO-002 — Repair validator syntax regression

- **Status:** RUNNING (fix committed; validation pending)
- **Date:** 2026-10-17
- **Question:** Does the documentation validator still parse after adding the automation contract to its required-file list?
- **Hypothesis and falsification:** Correcting the malformed list newline restores Python syntax; falsified if the next workflow fails for syntax or document checks.
- **Baseline:** Failed documentation workflow run #18 at commit f1738ad11f04457ca636dddc8b76b7d692b35985.
- **Exact change / command:** Replaced the literal backslash-n in the REQUIRED list with a real newline; fix commit 63d0d723e5d8ee67e1725ab65bcf12dcb61f6223.
- **Environment:** GitHub Actions documentation-validation workflow; no browser build.
- **Expected / actual cost:** One lightweight documentation validation; actual runtime not yet available for the fix run.
- **Evidence:** [Run #18 failure](https://github.com/sandeepbimt/Sandium/actions/runs/38997172822); fix commit [63d0d72](https://github.com/sandeepbimt/Sandium/commit/63d0d723e5d8ee67e1725ab65bcf12dcb61f6223).
- **Observed result:** Fix committed; subsequent validation pending.
- **Conclusion:** HYPOTHESIS pending.
- **What it proves / unknowns:** A syntax error was found and corrected in source; successful validation is not yet proven.
- **Learning / prevention rule:** Never equate a successful file-write API response with syntactically valid source.
- **Related failure / decision IDs:** FAIL-AUTO-002; DEC-004.
- **Next action:** Inspect the next docs validation run and only mark this experiment PASS when its logs confirm success.

### GitHub Actions run 38996549308

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #2 (run ID `38996549308`)
- **Branch/commit:** `main` / `ac974c53858c9965165dce7689b8ae6429f0427f`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:51:33Z, last updated 2026-10-17T02:51:39Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996549308
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996551342

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #3 (run ID `38996551342`)
- **Branch/commit:** `main` / `3ee17471bd545b393cb58b03bb4eccf1a00f038a`
- **Conclusion:** **FAILURE**; created 2026-10-17T02:51:35Z, last updated 2026-10-17T02:51:46Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996551342
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996634478

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #5 (run ID `38996634478`)
- **Branch/commit:** `main` / `5597dad678e8341cd7fc91799417acdc75e03017`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:52:53Z, last updated 2026-10-17T02:53:01Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996634478
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996891617

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #7 (run ID `38996891617`)
- **Branch/commit:** `main` / `89f0fa987febb4fcd27f598943847e6663883483`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:56:57Z, last updated 2026-10-17T02:57:06Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996891617
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996898112

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #8 (run ID `38996898112`)
- **Branch/commit:** `main` / `a464d202149360218b26fbb621206d3b3a7fdc23`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:57:04Z, last updated 2026-10-17T02:57:12Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996898112
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996901624

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #9 (run ID `38996901624`)
- **Branch/commit:** `main` / `71b8317daaba95d46c8f71fde57a87808a9a36fe`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:57:08Z, last updated 2026-10-17T02:57:11Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996901624
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996904095

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #10 (run ID `38996904095`)
- **Branch/commit:** `main` / `f85975f3c7cc36a624f097ceb4aa0b47ba25ea8c`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:57:10Z, last updated 2026-10-17T02:57:20Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996904095
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38996908245

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #11 (run ID `38996908245`)
- **Branch/commit:** `main` / `912704977ebdbc728478e8de814a1b19fde4d254`
- **Conclusion:** **CANCELLED**; created 2026-10-17T02:57:14Z, last updated 2026-10-17T02:57:21Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38996908245
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997106132

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #14 (run ID `38997106132`)
- **Branch/commit:** `main` / `c81fc64edd86c2a517f94ff589adb6ec7beb43e7`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:00:29Z, last updated 2026-10-17T03:00:36Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997106132
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997114003

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #15 (run ID `38997114003`)
- **Branch/commit:** `main` / `7f4a7a2847b942a95fac73ba75ff66612d05e359`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:00:35Z, last updated 2026-10-17T03:00:43Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997114003
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997121121

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #16 (run ID `38997121121`)
- **Branch/commit:** `main` / `59ec69ce1f6770c010ada48cb5959f1e5f8f4502`
- **Conclusion:** **FAILURE**; created 2026-10-17T03:00:40Z, last updated 2026-10-17T03:00:49Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997121121
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997167340

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #17 (run ID `38997167340`)
- **Branch/commit:** `main` / `88f659eaf737aab4fd5be6f02efc567bb6eed80e`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:01:18Z, last updated 2026-10-17T03:01:25Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997167340
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997172822

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #18 (run ID `38997172822`)
- **Branch/commit:** `main` / `f1738ad11f04457ca636dddc8b76b7d692b35985`
- **Conclusion:** **FAILURE**; created 2026-10-17T03:01:24Z, last updated 2026-10-17T03:01:33Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997172822
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997371209

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #20 (run ID `38997371209`)
- **Branch/commit:** `main` / `727a0a14e443ded654995798192aa135703fd1bc`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:25Z, last updated 2026-10-17T03:04:34Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997371209
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997376898

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #21 (run ID `38997376898`)
- **Branch/commit:** `main` / `a02fd14d2fbf0b3caeb7532ba0f55edb0d34ed90`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:30Z, last updated 2026-10-17T03:04:40Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997376898
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997382508

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #22 (run ID `38997382508`)
- **Branch/commit:** `main` / `12ff7d6a2167abbd59eab768b625764f2a4a91a4`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:36Z, last updated 2026-10-17T03:04:42Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997382508
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997387604

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #23 (run ID `38997387604`)
- **Branch/commit:** `main` / `b65189eae6d10f968a6213eaf8ac5f78cb048b20`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:40Z, last updated 2026-10-17T03:04:50Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997387604
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997391561

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #24 (run ID `38997391561`)
- **Branch/commit:** `main` / `926b251d52556210b55428c42b52230b572187c1`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:44Z, last updated 2026-10-17T03:04:50Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997391561
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997403871

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #26 (run ID `38997403871`)
- **Branch/commit:** `main` / `3188da9d637a52567f97c886eb5213acb16ac1e7`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:04:56Z, last updated 2026-10-17T03:05:04Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997403871
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997410872

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #27 (run ID `38997410872`)
- **Branch/commit:** `main` / `b8c62adb667a629229b272508602c457c98169cc`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:05:02Z, last updated 2026-10-17T03:05:11Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997410872
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997416669

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #28 (run ID `38997416669`)
- **Branch/commit:** `main` / `91364328976ebdb4c6e053ae64c578b65db5ba62`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:05:06Z, last updated 2026-10-17T03:05:22Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997416669
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997422916

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #29 (run ID `38997422916`)
- **Branch/commit:** `main` / `51638897ddd054fdce73a224f8337950de7ac567`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:05:11Z, last updated 2026-10-17T03:05:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997422916
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997428514

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #30 (run ID `38997428514`)
- **Branch/commit:** `main` / `18f85893832f828207a7bdefa0b03b6be801928f`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:05:16Z, last updated 2026-10-17T03:05:27Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997428514
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997473230

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #33 (run ID `38997473230`)
- **Branch/commit:** `main` / `a7621945baa5cd667d304a18227c606b9c6549aa`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:05:57Z, last updated 2026-10-17T03:06:04Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997473230
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997525224

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #36 (run ID `38997525224`)
- **Branch/commit:** `main` / `1248c4a0b79a625b9ceae52f5e4b393497d569dc`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:06:45Z, last updated 2026-10-17T03:06:53Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997525224
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997529180

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #37 (run ID `38997529180`)
- **Branch/commit:** `main` / `0660951da07bf713d51ce5ee7d14a518514d3a53`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:06:48Z, last updated 2026-10-17T03:07:02Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997529180
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997545278

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #39 (run ID `38997545278`)
- **Branch/commit:** `main` / `91c7d6b37c771733760fb96c7d681a9ae17a9508`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:07:03Z, last updated 2026-10-17T03:07:12Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997545278
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 38997550324

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #40 (run ID `38997550324`)
- **Branch/commit:** `main` / `ade7b71bceed4408dab5ac9394fef0c04bd25108`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:07:08Z, last updated 2026-10-17T03:07:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/38997550324
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39000715223

- **Recorded:** 2026-10-17 07:45 UTC
- **Workflow/run:** Sandium documentation validation / run #54 (run ID `39000715223`)
- **Branch/commit:** `main` / `cc55a3fa779bb893b6a773f510bdb406a78b2734`
- **Conclusion:** **CANCELLED**; created 2026-10-17T03:56:56Z, last updated 2026-10-17T03:57:12Z
- **Jobs:** Validate Sandium documentation: success
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39000715223
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39028971739

- **Recorded:** 2026-10-17 11:46 UTC
- **Workflow/run:** Sandium documentation validation / run #58 (run ID `39028971739`)
- **Branch/commit:** `main` / `8b35c411813e2509f47bd6b53c7deb609664231b`
- **Conclusion:** **CANCELLED**; created 2026-10-17T11:30:41Z, last updated 2026-10-17T11:30:50Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39028971739
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39029189037

- **Recorded:** 2026-10-17 11:46 UTC
- **Workflow/run:** Sandium documentation validation / run #62 (run ID `39029189037`)
- **Branch/commit:** `main` / `180dbc9be96a3daf7e55a6bcd89dff968740b745`
- **Conclusion:** **CANCELLED**; created 2026-10-17T11:34:00Z, last updated 2026-10-17T11:34:08Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39029189037
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.


### EXP-SISO-001 — Offline Sandium BuildBuddy adapter/configure_siso validation

- **Status:** PASS — for source-only/offline scope; runtime integration remains unverified.
- **Date:** 2026-10-17
- **Question:** Can Sandium's runtime REAPI configuration generate the expected Siso config and backend file with safe, deterministic helper behavior without network access or a Chromium checkout?
- **Hypothesis and falsification:** The candidate settings can be generated through Brave's documented override names; the pinned Chromium configure_siso.py resolves the backend path and emits exact .sisoenv values. Falsified if offline helper tests, config generation, backend copy or identity checks fail.
- **Baseline:** Sandium master Brave Core 1.100.10, Chromium 156.0.8078.39, Siso c574896b272b40aac6e44c228ee0b471ea7e3d7d. Review branch includes the earlier two-commit Google-preset opt-in change.
- **Exact change / command:** Source adapter branch [review/sandium-buildbuddy-backend-2026-10-17](https://github.com/sandeepbimt/Sandium/tree/review/sandium-buildbuddy-backend-2026-10-17), final commit 806f565ea44e256344f05cafe1b2b80b577aecfc. Ran python3 -m unittest discover -s tests/ci -p test_*.py -v in a local temporary copy; ran the exact pinned configure_siso.py with the candidate endpoint, stable namespace, backend relative path and absolute helper path.
- **Environment:** Local temporary Linux workspace, standard Python libraries, fake credentials and fake URIs only. Exact upstream configure_siso.py blob SHA verified as cb0ce6aadd79bf1e0fa88f3da6b0b82ffee366e5. No Chromium sync, Siso executable, BuildBuddy request, CI run or compilation.
- **Expected / actual cost:** Fourteen unit tests completed in about six seconds; config generation completed locally without external resources. No CI minutes, BuildBuddy invocation or remote execution spend.
- **Evidence:** [Source branch](https://github.com/sandeepbimt/Sandium/tree/review/sandium-buildbuddy-backend-2026-10-17); [source patch commit](https://github.com/sandeepbimt/Sandium/commit/41d0ba23b368720db0cff98468e7f25969b9fc3d); [test assertion fix](https://github.com/sandeepbimt/Sandium/commit/806f565ea44e256344f05cafe1b2b80b577aecfc); local exact blob hash, test output, .sisoenv assertions and byte-identical backend copy were verified.
- **Observed result:** 14/14 tests passed. .env managed block was idempotent, preserved unrelated settings and contained no fake key. Pinned configure_siso.py emitted the expected SISO_REAPI_INSTANCE, SISO_REAPI_ADDRESS and SISO_CREDENTIAL_HELPER values and copied backend.star byte-for-byte.
- **Conclusion:** VERIFIED for offline generation and helper unit tests only; BuildBuddy/Siso runtime interoperability is INCONCLUSIVE.
- **What it proves / unknowns:** It proves the chosen custom-var names/values can be represented and the pinned upstream config generator resolves the candidate backend path in a matching workspace layout. It does not prove Brave's full .env-to-.gclient execution path, the credential-helper request URI emitted by pinned Siso, account auth, cache isolation, image pull, remote action/cache hits, five-stage reuse, or APK completion.
- **Learning / prevention rule:** Keep runtime secrets out of .env and source; validate the generated file with the pinned upstream generator before touching the network. A unit-test assertion that scans raw text must distinguish configured property syntax from prose comments.
- **Related failure / decision IDs:** FAIL-SISO-001; DEC-007.
- **Next action:** Obtain separate explicit approval for pinned Siso auth-check against BuildBuddy, with no Chromium sync or compile.


### EXP-SISO-002 — GitHub Actions Siso authentication workflow bootstrap

- **Date:** 2026-10-17
- **Status:** FAIL — setup failure before authentication; BuildBuddy authorization remains untested.
- **Workflow:** [Sandium Siso BuildBuddy Auth Check, run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682), branch `review/sandium-buildbuddy-backend-2026-10-17`, commit `dea3e5ee0b214098117d26c823fc32c080022f4d`.
- **Purpose/scope:** Check the pinned Siso connection to `remote.buildbuddy.io:443`, instance `sandium/android-arm64/ci`, without Chromium checkout, GN, compilation or APK build.
- **Attempt 1:** Failed before Siso install because the GitHub Actions repository secret `BUILDBUDDY_API_KEY` was missing. User subsequently confirmed adding the secret. Secret value was not disclosed.
- **Attempt 2:** Checkout passed; Siso install step failed in about two seconds with `Error: no such package: infra/tools/siso/linux-amd64`. Authentication step was skipped.
- **Interpretation:** This is a Siso package/bootstrap naming or installation-method error, not a BuildBuddy authentication failure. No auth response, REAPI request or BuildBuddy authorization result was obtained.
- **Cost/effects:** One short GitHub Actions runner attempt; no Chromium sync, GN generation, compilation, APK or SANDFOX action.
- **Next action:** Inspect the pinned Chromium/Brave source and official depot_tools/CIPD package metadata to identify the exact Siso installation method for revision `c574896b272b40aac6e44c228ee0b471ea7e3d7d`; make the smallest workflow correction and rerun only this isolated workflow. Do not guess package identifiers or widen scope.


### EXP-SISO-002 — Pinned Siso installation and BuildBuddy authentication (2026-10-17, update)

- **Workflow:** [Sandium Siso BuildBuddy Auth Check, run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682)
- **Sandium branch/commit shown in run:** `review/sandium-buildbuddy-backend-2026-10-17`, commit `fd7411a` (short SHA as displayed by GitHub).
- **Attempt 1:** Failed because repository secret `BUILDBUDDY_API_KEY` was missing. User added the secret; its value was not disclosed or recorded.
- **Attempt 2:** The initial CIPD identifier `infra/tools/siso/linux-amd64` failed with `no such package`; auth step did not execute.
- **Correction:** Workflow changed to use Chromium depot_tools CIPD package identifier `build/siso/linux-amd64` pinned with `git_revision:c574896b272b40aac6e44c228ee0b471ea7e3d7d`. Workflow commit title shown in GitHub: `fix: use Chromium Siso CIPD package name`.
- **Verified result:** Run #2 succeeded in 53 seconds total (job 50 seconds). Install step passed in 8 seconds. The authentication step log states it logged in by `ci/siso/buildbuddy-credential-helper.py`, invoked `use reapi "remote.buildbuddy.io:443" instance "sandium/android-arm64/ci"`, and printed `Siso authentication check succeeded.`
- **Scope confirmation:** The step explicitly says no Chromium checkout, GN, compile, or APK build was performed. No SANDFOX infrastructure was touched.
- **Interpretation:** The isolated Siso authentication check is now VERIFIED for this endpoint/instance and configured credential helper. This does not prove remote action execution, cache reads/writes, executor image compatibility, full build behavior, reuse, runtime, or APK production.
- **Warning:** GitHub summary showed one annotation warning; its content has not been inspected in the supplied evidence.
- **Next action:** Stop at this successful baseline; do not launch a build. Before any remote-execution/build experiment, review the feasibility/cost gates in the charter, remote-build design and test plan.


### EXP-SISO-003 — No-build plan/cost and wiring audit (2026-10-17)

- **Scope:** Public vendor documentation and read-only inspection of Sandium review-branch source. No workflow, CircleCI job, REAPI request or build was run.
- **Publicly documented:** BuildBuddy pricing currently lists Personal as free with up to 80 remote-build cores and 100 GB cache transfer; Team is pay-as-you-go beyond included transfer. BuildBuddy's self-hosted RBE configuration guide says self-hosted remote execution configuration requires Enterprise. These are distinct product/deployment contexts and do not establish this account's entitlement. Sources: [BuildBuddy pricing](https://www.buildbuddy.io/pricing/), [BuildBuddy RBE configuration](https://www.buildbuddy.io/docs/config-rbe/).
- **Publicly documented:** CircleCI Free includes 30,000 monthly credits for personal usage; public Linux open-source projects may qualify for up to 400,000 credits. Account/project eligibility and available resource classes/remaining credits are not known. Sources: [CircleCI credits](https://circleci.com/docs/guides/plans-pricing/credits/), [CircleCI pricing](https://circleci.com/pricing/).
- **Verified source audit:** Runtime env generator keeps remote execution disabled and Google-specific Siso preset disabled; helper is host/scheme/port-scoped; backend image is digest-pinned.
- **Remaining gap:** Actual account-level BuildBuddy plan/usage and CircleCI plan/credits are not accessible through the repository connector. The generated backend relative path has not been confirmed by observing Brave's full runtime resolution in the intended workspace. A successful auth-only check is not proof of cache namespace isolation or remote execution.
- **Decision:** No remote action or build. Keep Gate 0 and Gate 1 partial. Next action requires the user to inspect the BuildBuddy organization plan/usage and CircleCI plan/usage screens; report plan/remaining quota and allowed resource class only, never API keys or secrets.

### GitHub Actions run 39032505190

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #68 (run ID `39032505190`)
- **Branch/commit:** `main` / `e3b3a09935e0b7d39d7288c1ec2dd08cfb3db11d`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:26:09Z, last updated 2026-10-17T12:26:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39032505190
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033626055

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #71 (run ID `39033626055`)
- **Branch/commit:** `main` / `c7784b2bc604fb484fe129de96d74ec901bb459e`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:42:58Z, last updated 2026-10-17T12:43:05Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033626055
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033629250

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #72 (run ID `39033629250`)
- **Branch/commit:** `main` / `9db9c74252e4d2694e77f7d87dbc04ea694f8445`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:43:01Z, last updated 2026-10-17T12:43:06Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033629250
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033706213

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #75 (run ID `39033706213`)
- **Branch/commit:** `main` / `3fbb7e1617e99a8ab571f0d1f506a3fe48eb2bb2`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:44:10Z, last updated 2026-10-17T12:44:16Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033706213
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033711031

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #76 (run ID `39033711031`)
- **Branch/commit:** `main` / `a663baa5fb0c3a3d01e215f321c6553224e6ed6a`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:44:14Z, last updated 2026-10-17T12:44:18Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033711031
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033790861

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #78 (run ID `39033790861`)
- **Branch/commit:** `main` / `6ba5cabaa648733470d39e474f3207c0b0b042c5`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:45:23Z, last updated 2026-10-17T12:45:31Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033790861
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39033795069

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #79 (run ID `39033795069`)
- **Branch/commit:** `main` / `1dc66ee072aa0bda881bd1f096d725d467385ab3`
- **Conclusion:** **CANCELLED**; created 2026-10-17T12:45:27Z, last updated 2026-10-17T12:45:32Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39033795069
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39038484624

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #86 (run ID `39038484624`)
- **Branch/commit:** `main` / `3100605cc88cc5f0caaa135310ed596bd50458a5`
- **Conclusion:** **CANCELLED**; created 2026-10-17T13:54:21Z, last updated 2026-10-17T13:54:29Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39038484624
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039157670

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #89 (run ID `39039157670`)
- **Branch/commit:** `main` / `fb1fbc11a8c36184670c7236c8945cfd5f164d37`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:03:55Z, last updated 2026-10-17T14:04:03Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039157670
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039161345

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #90 (run ID `39039161345`)
- **Branch/commit:** `main` / `edd50c7a8368bc2831932d972d3939fa2fd7fe74`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:03:58Z, last updated 2026-10-17T14:04:01Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039161345
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039173776

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #92 (run ID `39039173776`)
- **Branch/commit:** `main` / `5b0843d25cc2607fc3ffd77d35a588af1fb88f37`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:04:09Z, last updated 2026-10-17T14:04:17Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039173776
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039242318

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #94 (run ID `39039242318`)
- **Branch/commit:** `main` / `299b693ce1281400f9f6ceb351c5c5e87f4e99fa`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:05:08Z, last updated 2026-10-17T14:05:14Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039242318
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039246772

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #95 (run ID `39039246772`)
- **Branch/commit:** `main` / `f394a5e5c0dbc2863ce6298e18aa7541224e97a5`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:05:11Z, last updated 2026-10-17T14:05:15Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039246772
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039389359

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #97 (run ID `39039389359`)
- **Branch/commit:** `main` / `ee05c25fc781821f334256e973dd696f30b26ed3`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:07:12Z, last updated 2026-10-17T14:07:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039389359
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039393309

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #98 (run ID `39039393309`)
- **Branch/commit:** `main` / `d14268d004fb19917706ef4b44aba009cf5ec16d`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:07:16Z, last updated 2026-10-17T14:07:21Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039393309
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039396641

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #99 (run ID `39039396641`)
- **Branch/commit:** `main` / `be18eb9030184635a08e62ca6e3569fa2fb7c4cd`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:07:19Z, last updated 2026-10-17T14:07:23Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039396641
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 39039426058

- **Recorded:** 2026-10-17 14:27 UTC
- **Workflow/run:** Sandium documentation validation / run #101 (run ID `39039426058`)
- **Branch/commit:** `main` / `e62ba4e793d804304cbcb456ca6d46b60f4410a3`
- **Conclusion:** **CANCELLED**; created 2026-10-17T14:07:45Z, last updated 2026-10-17T14:07:54Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/39039426058
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170636432

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #103 (run ID `40170636432`)
- **Branch/commit:** `main` / `8281852a461b70cc633dcfb8162a6af7e3c2373e`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:04Z, last updated 2026-10-25T06:52:09Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170636432
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170639008

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #104 (run ID `40170639008`)
- **Branch/commit:** `main` / `f34cace9439ee699e5c1d02def506a960e1b5799`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:06Z, last updated 2026-10-25T06:52:09Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170639008
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170641431

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #105 (run ID `40170641431`)
- **Branch/commit:** `main` / `a2a41a6cd524625ccc8d8c91a7c4897dc5d1271c`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:08Z, last updated 2026-10-25T06:52:14Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170641431
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170644365

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #106 (run ID `40170644365`)
- **Branch/commit:** `main` / `1c658b0147ba7a4d1566466bee4fc306ce0b25ff`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:11Z, last updated 2026-10-25T06:52:16Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170644365
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170647983

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #107 (run ID `40170647983`)
- **Branch/commit:** `main` / `574cc5cfee1a25822227c0bd8c8fbf4d18b3c46c`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:14Z, last updated 2026-10-25T06:57:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170647983
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170651103

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #108 (run ID `40170651103`)
- **Branch/commit:** `main` / `cc2f374d8cab265e63cccce511e912ce4244a876`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:18Z, last updated 2026-10-25T06:52:21Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170651103
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170653835

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #109 (run ID `40170653835`)
- **Branch/commit:** `main` / `6f3715e76ec776245d93307a1eee4d7226559a35`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:20Z, last updated 2026-10-25T06:52:24Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170653835
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170656508

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #110 (run ID `40170656508`)
- **Branch/commit:** `main` / `0ad48b0f82d075d9bf809702cffc9243520add13`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:23Z, last updated 2026-10-25T06:52:27Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170656508
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170659551

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #111 (run ID `40170659551`)
- **Branch/commit:** `main` / `4365f8bc9f1c09607e7df6f87a919cc35b353c03`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:26Z, last updated 2026-10-25T06:52:31Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170659551
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170663077

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #112 (run ID `40170663077`)
- **Branch/commit:** `main` / `964f35fa011f0a5236d1bf83b0d60c99e6000c47`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:52:30Z, last updated 2026-10-25T06:53:32Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170663077
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170725577

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #113 (run ID `40170725577`)
- **Branch/commit:** `main` / `ffd9de240d894d8d6a253e15e85e948e019629e1`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:53:31Z, last updated 2026-10-25T06:53:34Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170725577
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170728033

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #114 (run ID `40170728033`)
- **Branch/commit:** `main` / `d10f9cecfc42f45c156f38c2ca7ea82748ca00ec`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:53:33Z, last updated 2026-10-25T06:53:37Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170728033
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170731042

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #115 (run ID `40170731042`)
- **Branch/commit:** `main` / `7f85b807932f40189247b7c2217c871a000631e6`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:53:36Z, last updated 2026-10-25T06:53:41Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170731042
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170734492

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #116 (run ID `40170734492`)
- **Branch/commit:** `main` / `db3cb2229349d4b6fde5f003a87db2288e9b54c7`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:53:40Z, last updated 2026-10-25T06:54:13Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170734492
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170767805

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #117 (run ID `40170767805`)
- **Branch/commit:** `main` / `37bda238c507f7b3aaa150a167c4dab08a92346f`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:54:12Z, last updated 2026-10-25T06:54:16Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170767805
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170770879

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #118 (run ID `40170770879`)
- **Branch/commit:** `main` / `9a99e8e03ed4675ef4af42355ac7ef0db70d3358`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:54:15Z, last updated 2026-10-25T06:56:07Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170770879
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170885181

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #119 (run ID `40170885181`)
- **Branch/commit:** `main` / `85ba00d021cdb0745e8a2d6647b2a6252822bc85`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:56:06Z, last updated 2026-10-25T06:56:09Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170885181
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170887690

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #120 (run ID `40170887690`)
- **Branch/commit:** `main` / `be65b54abacf564c08787445df747a4f5cdaa545`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:56:08Z, last updated 2026-10-25T06:56:12Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170887690
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170890924

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #121 (run ID `40170890924`)
- **Branch/commit:** `main` / `26148e47bff7bbdd7963b5e6caafe61c1eb5a761`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:56:11Z, last updated 2026-10-25T06:56:16Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170890924
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170894672

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #122 (run ID `40170894672`)
- **Branch/commit:** `main` / `2a4a017ba8949621aad59d101c81d64fc0fbfc8a`
- **Conclusion:** **FAILURE**; created 2026-10-25T06:56:15Z, last updated 2026-10-25T06:57:26Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170894672
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170965978

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #123 (run ID `40170965978`)
- **Branch/commit:** `main` / `5e33c434b827f2c52fd39b19f7d8cbfd44eaced0`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:57:26Z, last updated 2026-10-25T06:57:33Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170965978
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170969970

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #124 (run ID `40170969970`)
- **Branch/commit:** `main` / `60fdff1eb8c7956cc8f25570312f846f2c95f2be`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:57:30Z, last updated 2026-10-25T06:57:37Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170969970
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170973903

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #125 (run ID `40170973903`)
- **Branch/commit:** `main` / `1f8e45dec48ec731b6ba9135a516eea71448314b`
- **Conclusion:** **FAILURE**; created 2026-10-25T06:57:34Z, last updated 2026-10-25T06:57:43Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170973903
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170991011

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #126 (run ID `40170991011`)
- **Branch/commit:** `main` / `7b3f1537bb2a5cf945dd83ed14469362c32d5aac`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:57:51Z, last updated 2026-10-25T06:57:59Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170991011
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170994816

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #127 (run ID `40170994816`)
- **Branch/commit:** `main` / `44c9f1bc2b9a3d99f808bfacd66464baf09fda3a`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:57:54Z, last updated 2026-10-25T06:57:59Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170994816
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40170997939

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #128 (run ID `40170997939`)
- **Branch/commit:** `main` / `6b33e080c980ab4fff6553b9ff2960c0367f3cce`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:57:58Z, last updated 2026-10-25T07:03:01Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40170997939
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171000456

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #129 (run ID `40171000456`)
- **Branch/commit:** `main` / `318d3e42af3b5e30213e2a6bfb34f0b85e694503`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:58:00Z, last updated 2026-10-25T06:58:06Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171000456
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171004521

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #130 (run ID `40171004521`)
- **Branch/commit:** `main` / `2b7ea854ef0b1760bab596602f477e7a153181c3`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:58:04Z, last updated 2026-10-25T06:58:08Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171004521
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171006980

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #131 (run ID `40171006980`)
- **Branch/commit:** `main` / `e7bc76caafe70c9cb2eadc5caa4a35295d609f5a`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:58:07Z, last updated 2026-10-25T06:58:29Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171006980
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171028358

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #132 (run ID `40171028358`)
- **Branch/commit:** `main` / `a9eb22b15471b9702ec18f3b06cdf028aa415a3d`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:58:28Z, last updated 2026-10-25T06:58:42Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171028358
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171041381

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #133 (run ID `40171041381`)
- **Branch/commit:** `main` / `0583ba16805aad1b71eb3f5727b7b4ee7214b539`
- **Conclusion:** **CANCELLED**; created 2026-10-25T06:58:41Z, last updated 2026-10-25T07:00:46Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171041381
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171176611

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #134 (run ID `40171176611`)
- **Branch/commit:** `main` / `2ce5af205c78551127f0d577a58b092187092ae2`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:00:45Z, last updated 2026-10-25T07:00:50Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171176611
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171180482

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #135 (run ID `40171180482`)
- **Branch/commit:** `main` / `1946694d5e84f0889a86d611d67594d8bf41416e`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:00:49Z, last updated 2026-10-25T07:02:15Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171180482
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171271961

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #136 (run ID `40171271961`)
- **Branch/commit:** `main` / `abe38c3af13201ec31569f807e5fec788250b429`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:02:14Z, last updated 2026-10-25T07:02:19Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171271961
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171275699

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #137 (run ID `40171275699`)
- **Branch/commit:** `main` / `e02003bfc333505b33ce832a98a33ba9703bba9f`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:02:18Z, last updated 2026-10-25T07:02:34Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171275699
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171291109

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #138 (run ID `40171291109`)
- **Branch/commit:** `main` / `67d8fed24651a64589b1df5ad923f7e1508981b5`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:02:33Z, last updated 2026-10-25T07:02:40Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171291109
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171296997

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #139 (run ID `40171296997`)
- **Branch/commit:** `main` / `d8332a42a9c49d97f2f7cc224e906ef5b705a3c9`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:02:39Z, last updated 2026-10-25T07:03:07Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171296997
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171332304

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #140 (run ID `40171332304`)
- **Branch/commit:** `main` / `b12b84d7457993e27e6c9618cedd79f33505499a`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:03:14Z, last updated 2026-10-25T07:03:19Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171332304
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171335493

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #141 (run ID `40171335493`)
- **Branch/commit:** `main` / `37df119911ed275bc244167a1d96c809c1a38ce4`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:03:17Z, last updated 2026-10-25T07:03:27Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171335493
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171828203

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #142 (run ID `40171828203`)
- **Branch/commit:** `main` / `4353f90c78d3696771a3ebaeea161919d2404642`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:11:10Z, last updated 2026-10-25T07:11:17Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171828203
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171835402

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #143 (run ID `40171835402`)
- **Branch/commit:** `main` / `de66ee9c5bdb5447eac39f1ecab7df7cbbfbd10c`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:11:17Z, last updated 2026-10-25T07:11:26Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171835402
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171840072

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #144 (run ID `40171840072`)
- **Branch/commit:** `main` / `cb48c44a93d73254558489a9595d2ba9877799c2`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:11:22Z, last updated 2026-10-25T07:11:32Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171840072
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171920692

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #145 (run ID `40171920692`)
- **Branch/commit:** `main` / `cfe4d09f27838819d02c49f65707f7dac797ea4a`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:12:40Z, last updated 2026-10-25T07:12:47Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171920692
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171924255

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #146 (run ID `40171924255`)
- **Branch/commit:** `main` / `acd485f8efec05f605083b9a6517585b9cf9379a`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:12:44Z, last updated 2026-10-25T07:12:54Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171924255
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171987120

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #147 (run ID `40171987120`)
- **Branch/commit:** `main` / `373d0ff56ffbd334a0b24c0d8aeaef4193ee7a8b`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:13:46Z, last updated 2026-10-25T07:13:53Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171987120
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171990366

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #148 (run ID `40171990366`)
- **Branch/commit:** `main` / `4e0be3ae7598a352c157e64673f59b4f6ae1a42f`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:13:50Z, last updated 2026-10-25T07:13:55Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171990366
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171994251

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #149 (run ID `40171994251`)
- **Branch/commit:** `main` / `fc21bdc9b8820fb36140622c3003a9ec22291522`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:13:54Z, last updated 2026-10-25T07:14:00Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171994251
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40171997919

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #150 (run ID `40171997919`)
- **Branch/commit:** `main` / `ff396b2c7f99dc97bebade172ffae728a83fdbfd`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:13:58Z, last updated 2026-10-25T07:14:05Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40171997919
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172002618

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #151 (run ID `40172002618`)
- **Branch/commit:** `main` / `8d90a580d04d4f1d0b9c32ab298087398a4781aa`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:14:02Z, last updated 2026-10-25T07:14:11Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172002618
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172040149

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #152 (run ID `40172040149`)
- **Branch/commit:** `main` / `e8ed01833a0094d92d9beae6c227078d0ddd5b2a`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:14:40Z, last updated 2026-10-25T07:14:48Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172040149
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172044171

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #153 (run ID `40172044171`)
- **Branch/commit:** `main` / `4f86ce7b52114465e160c1f0734bc42163e5c9dd`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:14:44Z, last updated 2026-10-25T07:14:49Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172044171
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172047385

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #154 (run ID `40172047385`)
- **Branch/commit:** `main` / `8ee40c63c81747136ebf2d87d76d9a8fa51370bb`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:14:48Z, last updated 2026-10-25T07:14:57Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172047385
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172163133

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #155 (run ID `40172163133`)
- **Branch/commit:** `main` / `d0b6ce6b7c0a893b5b51de96ba7b6d6b072eafab`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:16:38Z, last updated 2026-10-25T07:16:44Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172163133
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172166676

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #156 (run ID `40172166676`)
- **Branch/commit:** `main` / `efb1fac6d0ef0ef2135081c1d250ca0b7d7a353c`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:16:41Z, last updated 2026-10-25T07:16:51Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172166676
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172170788

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #157 (run ID `40172170788`)
- **Branch/commit:** `main` / `c9acc82c510b74e963c42b6c0b31ce21c4bbe3bf`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:16:45Z, last updated 2026-10-25T07:16:57Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172170788
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172183376

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #158 (run ID `40172183376`)
- **Branch/commit:** `main` / `10f450f0d2a5bc7bd17f8b7a650e0247c1ee5bfc`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:16:58Z, last updated 2026-10-25T07:17:05Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172183376
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172244709

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #159 (run ID `40172244709`)
- **Branch/commit:** `main` / `eb2f7a40e7e931eeac74009e5dd84069ccbed27f`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:17:59Z, last updated 2026-10-25T07:18:07Z
- **Jobs:** Validate Sandium documentation: cancelled
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172244709
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172248271

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #160 (run ID `40172248271`)
- **Branch/commit:** `main` / `ec0c916b211a6b1c8499db9d902af3b6c419f118`
- **Conclusion:** **CANCELLED**; created 2026-10-25T07:18:02Z, last updated 2026-10-25T07:18:07Z
- **Jobs:** UNKNOWN
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172248271
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172252212

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #161 (run ID `40172252212`)
- **Branch/commit:** `main` / `80922a4906cf60ceed76ab12f4e080cb0d2874c6`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:18:06Z, last updated 2026-10-25T07:18:15Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172252212
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40172374271

- **Recorded:** 2026-10-25 10:08 UTC
- **Workflow/run:** Sandium documentation validation / run #162 (run ID `40172374271`)
- **Branch/commit:** `main` / `64287b4dca40a892c0693ac03b9bb7da4f8c61c1`
- **Conclusion:** **FAILURE**; created 2026-10-25T07:20:08Z, last updated 2026-10-25T07:20:14Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40172374271
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

## EXP-BARE-SYNC-001 — Pin-first single gclient sync

- **Date:** 2026-10-25
- **Purpose:** Diagnose repeated stage-1 source setup stalls on the pinned Bare/Chromium Android build.
- **Branch under test:** `fix/bare-stage-handoff-review` (experimental; not a clean base).
- **Source pins:** Bare `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`; Chromium `1228231501697ff7a4a0150ea8ae6df37bb99331` / `156.0.8078.25`.
- **Preflight:** pass. Bare patch-series count 164; pinned source metadata and uBlock checksum validated without Chromium sync or compilation.
- **Attempt A outcome:** initial `fetch android` returned 0 after 8m23s, but it runs an internal `gclient sync` before returning. A later explicit sync to the pinned Chromium revision timed out at 20m with exit 124. It showed repeated `Still working on: src`. No GN/compile/APK resulted.
- **Additional observation:** a subsequent live screen showed a Git fetch retry warning for `third_party/clang-format/script` at `9f796802e5d633c96dbe97e0b6683d5e625949f9`. Since no underlying RPC/fatal error was captured in the screenshot, the transport root cause remains unknown.
- **Online finding:** depot_tools fetch source calls gclient config and then gclient sync; official Chromium docs say gclient materializes Git dependencies pinned through DEPS. Similar community logs show this retry message can occur with HTTP 400 shallow-info errors or connection-reset/early-EOF, but those are not proven for this run. References: https://github.com/columbia/depot_tools/blob/main/fetch.py ; https://github.com/chromium/chromium/blob/main/docs/dependencies.md ; https://groups.google.com/a/chromium.org/g/chromium-dev/c/pRDAs6tm-Zs ; https://groups.google.com/a/chromium.org/g/chromium-dev/c/UFZ7B19A1eM
- **Hypothesis tested next:** the prior pin step happened too late, because it came after fetch's internal dependency sync. The script was changed to run gclient config only, directly check out the pinned Chromium revision (bounded to 15 minutes plus a 60-second termination grace), and then perform a single bounded verbose sync. A Git command trace and separate config/fetch/sync logs are now collected. The five-stage workflow was also aligned to keep only small source-bound stage ledgers in CircleCI cache (no large output checkpoint archive); cross-stage compiled reuse is expected from the existing BuildBuddy/Siso remote cache. The final stage-5 gate now requires `BUILD_FINISHED=true`, `APK_ARCHIVE_VALID=true`, and `APK_SIGNATURE_VERIFIED=true`.
- **Code commits:** `8009f34419ca807f004a2176741f8c7a166c0bc1` (pin-first sync); `cd74848bf7e866772ce05e2a3dfa0afb48e85dd6` (initialize diagnostic logs); `a4e9f6469059bdb024201392987cfc524c357877` (static syntax checks before network work); `f0cb6c7cd055fb4c9b4686ab6c23bea70a1a7add` (bounded direct pin fetch); config artifact updates `0fd8cd5f107530a89dbfc9dee45e49c522a2926a`.
- **Current result:** fix committed; validation by a new CircleCI run is pending. This experiment is not a success; no APK has been produced.
- **Next action:** trigger the isolated five-stage workflow on the review branch and inspect whether `SANDIUM_CHROMIUM_DIRECT_PIN_PASS` appears and whether the single pinned gclient sync completes. If it fails, use the new Git trace and sync log to classify the exact transport/dependency error before making another change.

### GitHub Actions run 40216765034

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #163 (run ID `40216765034`)
- **Branch/commit:** `main` / `f4f09762b74639e63cf0b0cd085694103e95e1ea`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:30:07Z, last updated 2026-10-25T17:30:13Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40216765034
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40216822271

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #164 (run ID `40216822271`)
- **Branch/commit:** `main` / `98f0e6a41480e14b48b2934b851cc94f3c91dfca`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:30:45Z, last updated 2026-10-25T17:30:53Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40216822271
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40216847634

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #165 (run ID `40216847634`)
- **Branch/commit:** `main` / `aefecaab272574725d6dc23b4fc6d180e3e8195d`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:31:03Z, last updated 2026-10-25T17:31:11Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40216847634
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40216946859

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #166 (run ID `40216946859`)
- **Branch/commit:** `main` / `481371c5f167b01487d333b06d0969bea4cb7d72`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:32:16Z, last updated 2026-10-25T17:32:23Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40216946859
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40216980488

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #167 (run ID `40216980488`)
- **Branch/commit:** `main` / `5c88e4475cf94b7bf989f3c14cf4faea947a0920`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:32:41Z, last updated 2026-10-25T17:32:50Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40216980488
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40217037914

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #168 (run ID `40217037914`)
- **Branch/commit:** `main` / `253089abdad411f941384497ef585884c95a0868`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:33:24Z, last updated 2026-10-25T17:33:31Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40217037914
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40217392010

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #169 (run ID `40217392010`)
- **Branch/commit:** `main` / `3024e52953f39f0de3ea4b14a0d8498552052379`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:37:54Z, last updated 2026-10-25T17:38:01Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40217392010
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40217403942

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #170 (run ID `40217403942`)
- **Branch/commit:** `main` / `ecb071506932c667ed1900de8f628874df6a549e`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:38:03Z, last updated 2026-10-25T17:38:11Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40217403942
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40217417437

- **Recorded:** 2026-10-25 17:51 UTC
- **Workflow/run:** Sandium documentation validation / run #171 (run ID `40217417437`)
- **Branch/commit:** `main` / `5bdbf8bd4faf65bb41a1a8c259167ae1bfb63a23`
- **Conclusion:** **FAILURE**; created 2026-10-25T17:38:13Z, last updated 2026-10-25T17:38:20Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40217417437
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.

### GitHub Actions run 40219367969

- **Recorded:** 2026-10-25 20:48 UTC
- **Workflow/run:** Sandium documentation validation / run #172 (run ID `40219367969`)
- **Branch/commit:** `main` / `95297de4f3f7f048e717f4fb9c90e92be69e241b`
- **Conclusion:** **FAILURE**; created 2026-10-25T18:02:50Z, last updated 2026-10-25T18:02:57Z
- **Jobs:** Validate Sandium documentation: failure
- **Artifacts:** No artifacts reported by GitHub.
- **Run evidence:** https://github.com/sandeepbimt/Sandium-Docs/actions/runs/40219367969
- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.
