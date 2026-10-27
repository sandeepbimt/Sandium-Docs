# Sandium Chat Continuity — 2026-10-27
**Purpose:** Continue the exact Stage 1 → Stage 2 compiled-output reuse and task-accounting investigation in a new ChatGPT chat without losing evidence or repeating prior mistakes.

**Project repositories**
- Build/control repository: https://github.com/sandeepbimt/Sandium
- Documentation repository: https://github.com/sandeepbimt/Sandium-Docs
- Active build branch: `build/bare-apk-once-20261025`
- CircleCI pipeline: `sandium-buildbuddy-siso-preflight`
- Target: `Sandium-debug-arm64.apk` (Android ARM64 debug APK)
- Current latest known code commit in the branch: `0847bd8f546ea53feae85b5bf9c77e67625979b3` — `test(ci): run compiled output reuse preflight regression`
- The live CircleCI screenshot header showed the workflow associated with commit `0847bd8`. Do not assume the live run's final state until its logs are retrieved.

> ## Mandatory next action
> **Continue from the exact current evidence below. Do not launch, rerun, cancel, or trigger another build.** The current five-stage CircleCI workflow was still running Stage 2 in the latest screenshot. First obtain its final logs/artifacts after it finishes, or inspect the current live step if it is still running. Establish actual compiled-output reuse and reconcile Stage 1/Stage 2 graph totals before changing source or spending more credits.
>
> Do not declare reuse successful because a large archive was found/extracted. Do not “fix” a mismatch by simply weakening the ledger or forcing the denominator to match. Keep actual compile reuse and progress-accounting correctness as separate questions.

## 1. User intent and constraints
- User is frustrated by repeated costly builds, cache restores that do not produce useful reuse, and prior tally errors.
- Wants a concrete, evidence-based diagnosis and code fix, not generic suggestions or a speculative new build.
- CircleCI credits are limited. No parallel builds or blind experiments.
- Keep heavyweight Chromium/Android compilation separate from lightweight tests.
- Do not claim that a run started, completed, passed, created an APK, or reused outputs unless logs/artifacts prove it.
- Do not touch old SANDFOX CircleCI/BuildBuddy/Siso infrastructure; this is the separate Sandium project.
- User explicitly asked to move the investigation to a **new chat** and provide a continuity MD. This file is that handoff. The assistant cannot create/open a new ChatGPT conversation on the user's behalf; the user should open a new chat and attach/paste this file, asking to continue from its “Mandatory next action.”
- Preserve the existing last-known-good checkpoint and do not delete remote caches.

## 2. Exact current live-run state from screenshots
Screenshots were shared by the user on 2026-10-27 around 5:07–5:43 PM local time (India). Latest view of Stage 2 showed it **still running**.

### Stage 1 screenshot — authoritative reference supplied by user
The screenshot showed the end of the Stage 1 step “Build one bounded incremental window of the pinned Bare APK” at approximately **43m 51s**. The log's exact reported fields included:

- `SANDIUM_STAGE_LEDGER=PASS stage=1`
- `SANDIUM_STAGE_EVIDENCE=REMOTE_EXECUTION_OR_CACHE_WITH_PROGRESS`
- `SANDIUM_BUILD_IDENTITY_SHA256=1c9148f66f75e0a53656ed382f60957e40edda715214f647a571bccc4b8f8f8f`
- `SISO_REMOTE_EXECUTED_ACTIONS=1`
- `SISO_REMOTE_ACTION_CACHE_HITS=45308`
- `SANDIUM_STAGE_COMPLETED_ACTIONS=55304`
- `SANDIUM_PROGRESS_ACCOUNTING_MODE=NON_ADDITIVE_WATERMARK`
- `SANDIUM_PROGRESS_IS_UNIQUE_CUMULATIVE_ACTION_COUNT=false`
- `SANDIUM_PROGRESS_WATERMARK=55304`
- `SANDIUM_MAX_COMPLETED_ACTIONS=55304`
- `SANDIUM_CUMULATIVE_COMPLETED_ACTIONS=55304`
- `SANDIUM_ESTIMATED_REMAINING_ACTIONS=53764`
- `SANDIUM_TOTAL_ACTION_COUNT=109068`
- `SANDIUM_APK_READY=false`
- `SANDIUM_STATE_HANDOFF_PACK=PASS`
- `SANDIUM_STATE_HANDOFF_FILES=.siso_fs_state,.siso_fs_state.journal,.siso_fs_state.0,.ninja_log,.ninja_deps,.siso_config,.siso_deps,.siso_filegroups`
- `SANDIUM_STATE_HANDOFF_ARCHIVE_BYTES=59270657`
- `SANDIUM_STATE_HANDOFF_BUILD_IDENTITY_SHA256=1c9148f66f75e0a53656ed382f60957e40edda715214f647a571bccc4b8f8f8f`
- `SANDIUM_OUTPUT_CHECKPOINT_PREFLIGHT=PASS`
- `SANDIUM_OUTPUT_CHECKPOINT_STAGE=1`
- `SANDIUM_OUTPUT_CHECKPOINT_KIND=completed-stage`
- `SANDIUM_OUTPUT_CHECKPOINT_BYTES=12667276992`
- `SANDIUM_OUTPUT_CHECKPOINT_BUILD_IDENTITY_SHA256=1c9148f66f75e0a53656ed382f60957e40edda715214f647a571bccc4b8f8f8f`
- `SANDIUM_OUTPUT_CHECKPOINT_COMPILED_OBJECT_FILES=39373`
- `SANDIUM_OUTPUT_CHECKPOINT_COMPILED_OBJECT_BYTES=3440344250`
- `SANDIUM_OUTPUT_CHECKPOINT_ACTION_SAMPLE_FILES=24`

**Crucial Stage 1 limitation:** the same screenshot explicitly showed:
- `SANDIUM_COMPILED_OUTPUT_REUSE_EVIDENCE=LOCAL_OUTPUT_REUSE_NOT_PROVEN`
- `SANDIUM_COMPILED_OUTPUT_REUSE_VERIFIED_SAMPLES=0`
- `SANDIUM_COMPILED_OUTPUT_REUSE_MINIMUM_SAMPLES=3`

Therefore Stage 1 did a large amount of work and saved a substantial checkpoint, but did **not** prove that it reused local outputs from an earlier checkpoint. This does not by itself prove the checkpoint is unusable by Stage 2; Stage 2 must test restored outputs.

### Stage 2 screenshot — latest observed running build
The screenshot at approximately 5:43 PM showed:
- Job: `sandium-bare-stage-2`
- Build step: “Build one bounded incremental window of the pinned Bare APK”
- Elapsed in that step: about **29m 11s** (another prior screenshot showed 21m 20s; use the latest one).
- Visible Siso progress: approximately `[49008/69088]`, with numerous C++ and generated-action lines.
- Earlier Stage 2 setup steps were green:
  - Restore Stage 1 APK/status metadata
  - Reuse a verified APK before restoring multi-gigabyte build output
  - Restore full compiled outputs from this workflow's Stage 1 (1.8 GiB archive, extracted in about 29 seconds)
  - Restore pinned Chromium/Bare source and dependency cache (a 17 GiB cache was found; restore step completed in 2m53s)
  - Fail closed if a continuation stage lost its source cache
  - Validate/prepare pinned Chromium source without configuring GN
- Stage 2 had not yet shown a final ledger, final Siso metrics, checkpoint save, or verified APK in the screenshots.

The displayed Stage 2 denominator (~69,088) is materially lower than Stage 1's recorded `SANDIUM_TOTAL_ACTION_COUNT=109068`. Difference is roughly 36.7%, not small drift. This is a **high-risk potential graph-total mismatch**, but it is not yet a confirmed final failure because the screenshot is mid-build and the authoritative final parsed total/ledger have not been retrieved. Do not treat an in-progress Siso display as the final ledger value.

## 3. Key questions to answer next
1. Did Stage 2 actually restore Stage 1's full compiled output tree into the exact expected output path?
2. Did source restoration and GN/configuration preserve the restored objects and generated graph?
3. Did the Stage 2 reuse preflight run and pass? Retrieve its actual sample-level output.
4. Does Stage 2 show real local compiled-output reuse, with at least the required 3 verified samples, or only a checkpoint restore?
5. How many Stage 2 actions were genuinely executed locally/remotely, cached, skipped/no-exec, or rebuilt? Read the actual Siso metrics JSONL and summary; don't infer from the progress counter.
6. What final action count does Stage 2 pass to the ledger? Does it equal Stage 1's 109,068 or does the ledger fail with `Build graph action count changed: prior=... current=...`?
7. Is the Stage 2 checkpoint cumulative and correctly identity-bound? Is it only published on success?
8. Was `Sandium-debug-arm64.apk` created and fully verified (manifest, SHA-256, ZIP integrity, signature)? Current screenshots show `APK_READY=false` at the end of Stage 1, not an APK.

## 4. Relevant source implementation already inspected
Repository: `sandeepbimt/Sandium`, branch `build/bare-apk-once-20261025`.

- `ci/bare/run_stage.sh` (observed blob SHA `bcd45ecc87a6860345ed9f05b773ff18fc0adbb7`)
  - Runs lightweight static checks and regression tests.
  - For stages >1, requires a previous ledger and validates cached APK fast path.
  - Normalizes regular source files to epoch `946684800`.
  - Configures GN, requires `use_siso=true`, `use_reclient=false`, `use_remoteexec=true`.
  - Normalizes generated-file timestamps before cache identity/output checkpoint handling.
  - Restores a full output checkpoint; later stages require it.
  - Emits `SANDIUM_COMPILED_OUTPUT_REUSE=FULL_CHECKPOINT_RESTORED_NOT_YET_PROVEN` immediately after archive restore. This is intentionally not proof of reuse.
- `ci/bare/stage_ledger.py` (observed blob SHA `d3cb3d3ba84091c8188b1434ee0de8459a3f419d`)
  - Requires exact source/toolchain/GN/Siso build identity across stages.
  - Requires Stage 2 state handoff to be from Stage 1 in the same CircleCI workflow.
  - Requires full compiled-output restore and verified local reuse before continuing.
  - Requires prior graph total to equal current total in its strict ledger path.
  - Uses non-additive progress watermarks; stage-local counts overlap with prior-stage counts and must not be blindly summed.
- `ci/bare/output_checkpoint.py` (observed blob SHA `8deaeb9d0529255771777458843938637dd87fbe`)
  - Full checkpoint is the compiled output tree at `src/out/android_Debug_arm64`, saved beside source tree to avoid making `out/` look like a partial checkout.
  - Archive restoration and identity checks alone are not proof of Siso consuming the outputs.
- `ci/bare/state_handoff.py` (observed blob SHA `c1f30da7c19e6748f91c9c3407c49dc14ff8b723`)
  - Handles Siso filesystem state and related files such as `.siso_fs_state`, journals, `.ninja_log`, `.ninja_deps`, Siso config/deps/filegroup state.
- `ci/bare/normalize_progress_total.py`
  - Allows at most 1% denominator drift only if full build identity exactly matches; a ~36.7% difference is far outside this allowance and should not be papered over.
- `ci/bare/test_stage_ledger.py`
  - Tests non-additive watermark accounting and legacy additive-ledger repair.
  - Includes test that graph total must remain stable across stages.
- `ci/bare/test_compiled_output_reuse_preflight.py`
  - Added to lightweight validation workflow in commit `0847bd8f546ea53feae85b5bf9c77e67625979b3`.
  - This fixed a previous false positive where the reuse parser mistook the echoed Siso `ninja -n` invocation and its target arguments for scheduled compile actions. It does not by itself prove the live Stage 2 reuse works.

## 5. Prior history and learning that must not be lost
- Previous ledger bug: code added a prior baseline to the current Siso/Ninja progress even though these counts overlap. It failed with:
  `Cumulative completed-action estimate exceeds graph total: baseline=103735 current_stage=55453 total=109040`.
  A non-additive watermark fix was introduced. Do not reintroduce additive progress.
- Earlier stage attempt ran roughly 40m37s and timed out (`AUTONINJA_EXIT_CODE=124`) after tens of thousands of actions. Do not infer action totals from line counts.
- Prior output checkpoint failures included:
  - 16-byte archive (metadata-only, not useful compiled output).
  - Missing Siso state file at handoff.
  - Manifest-preflight false positive from repeated GN/build.ninja regeneration.
  - REAPI output-path rejection due to `-fcrash-diagnostics-dir=../clang-crashreports`.
- A large archive (1.5–1.8 GiB compressed) is better than a 16-byte archive, but it still does not prove compatible, usable output reuse.
- A cache archive being downloaded/extracted is not the same as Siso skipping already-built outputs.
- Local compiled-output reuse and remote action-cache hits are separate signals. Remote cache-hit count may be high even if local output reuse is poor; interpret Siso metrics carefully.
- Previous live screenshot showed Stage 2 performing many C++/generated actions after restore. This raises concern for repeated work but does not prove it without final metrics/sample checks.
- User strongly suspects Stage 2 is repeating Stage 1 work and that a task-count mismatch may cause a later failure. Treat this as a credible hypothesis to test, not as an already confirmed failure.

## 6. Required evidence retrieval sequence
Do not start another build. Use current run evidence first:
1. Open the CircleCI Stage 2 job and wait for final state if still running.
2. Download/retrieve these artifacts/logs if available:
   - `stage-2-driver.log`
   - `stage-2-siso.log`
   - `stage-2-metrics.jsonl`
   - `stage-2-reuse-preflight.log` (or exact filename referenced by driver)
   - `sandium-state-handoff-report.json`
   - `ci-handoff/stage-2/ledger.json` and `status.txt`
   - checkpoint-quality report and artifact manifest/APK, if present
3. Record the exact final values for:
   - `SANDIUM_COMPILED_OUTPUT_REUSE_EVIDENCE`
   - verified sample count / required sample count
   - build identity hashes and checkpoint identity
   - source checkpoint stage/workflow
   - `SANDIUM_STAGE_COMPLETED_ACTIONS`
   - `SANDIUM_TOTAL_ACTION_COUNT` and `SANDIUM_GRAPH_TOTAL_VARIANCE` if any
   - Siso local/remote/cache/skip/noexec counters, actual remote execution proof, remote cache hits
   - final ledger result and exit code
   - checkpoint bytes and object inventory after Stage 2
   - APK path, bytes, SHA-256, archive/signature verification, `artifact_verified`
4. Compare Stage 1 baseline above against Stage 2's actual output.
5. If CircleCI connector/API isn't available, ask the user for the final Stage 2 log/artifact rather than guessing. Don't claim access to CircleCI beyond screenshots/logs the user has provided.

## 7. Decision tree after evidence
- **If Stage 2 reuse preflight fails:** inspect exact sample-level output, paths, mtimes, build.ninja/GN hashes, output inventory and source/toolchain/GN identity. Determine why restored object files are considered dirty.
- **If reuse passes but graph total differs materially:** determine why graph totals differ after GN/source restoration; inspect final `build.ninja` identity, generated files, Siso dry-run total, normalized total output and ledger arguments. Do not just weaken the >1% guard.
- **If reuse passes and totals match:** verify forward progress and the final cumulative checkpoint. Do not infer APK success until the APK/manifest/signature/hash checks pass.
- **If the stage times out or fails:** preserve the last known-good checkpoint, capture final logs and ledger, identify exact failing gate, and only then make a targeted code change plus regression test.
- Any fix should be followed by lightweight validation first. A new full build requires explicit authorization after reviewing the current run's evidence.

## 8. Last known source fix and lightweight validation
- Commit: `0847bd8f546ea53feae85b5bf9c77e67625979b3`
- Message: `test(ci): run compiled output reuse preflight regression`
- Branch: `build/bare-apk-once-20261025`
- Changed file: `.github/workflows/validate-bare-stage-pipeline.yml`, adding `python3 ci/bare/test_compiled_output_reuse_preflight.py` to lightweight offline validation.
- GitHub Actions run reported success: https://github.com/sandeepbimt/Sandium/actions/runs/40490570355
- This is only a source-level/lightweight validation result. It is **not** proof of live CircleCI Stage 2 reuse or APK creation.
- A prior parser correction fixed the false-positive from Siso dry-run invocation echo; see commits `b09e2229`, `0dd94eb9`, `ffb4b457`, `9f308043`, and `0847bd8f` in the branch history. Latest known head was `0847bd8f` when inspected; verify live run's exact commit before concluding.

## 9. User communication rules for continuation
- Start with evidence-based status, clearly separating **confirmed**, **inferred/risk**, and **not yet known**.
- Keep the response direct and concise, but include exact numbers and exact log fields.
- Do not ask the user to repeat information already in this file.
- Do not tell the user to launch another build while the current run's evidence remains uninspected.
- Never describe an archive restore as proof of reuse.
- Never add stage action counters together unless a verified, disjoint-delta definition supports it.
- Never “solve” a tally error by relaxing validation without explaining the underlying graph/identity difference.
- Never claim an APK exists until it has been verified.
- The single next action is: **inspect the final/current Stage 2 evidence, then diagnose the actual reuse and denominator issue.**
