# SANDIUM — Bare + CircleCI + BuildBuddy + Siso Remote Build Design

**Status:** Source adapter in progress; all build workflows remain gated  
**Authority:** [SANDIUM_SOURCE_OF_TRUTH.md](SANDIUM_SOURCE_OF_TRUTH.md)  
**Active migration branch:** [`migration/bare-source-adapter`](https://github.com/sandeepbimt/Sandium/tree/migration/bare-source-adapter)

## Source identity

- Bare repository: https://github.com/BareBrowser/bare-browser
- Reviewed Bare commit: `a5a7ef74f3b77d45720b8c502cbacc30f2f3dbd5`
- Chromium commit: `1228231501697ff7a4a0150ea8ae6df37bb99331`
- Chromium version: `156.0.8078.25`
- Bare is an ordered patch series over Chromium Desktop Android, not a complete Chromium source checkout.
- Source preparation must fetch the pinned Bare commit, verify its Chromium pin, check out that exact Chromium revision, apply the ordered patches, and supply the separately versioned/checksummed uBlock Origin CRX input.

## Preserve existing integration

Do not create or reconnect any project, account, context, webhook or credential. Reuse the existing Sandium GitHub repository, CircleCI project/integration, BuildBuddy endpoint/instance, protected `BUILDBUDDY_API_KEY` assignment, Siso integration and cache configuration.

The existing recorded endpoint/instance are `remote.buildbuddy.io:443` and `sandium/android-arm64/ci`. The existing GitHub Actions authentication check passed in [run 39037465682](https://github.com/sandeepbimt/Sandium/actions/runs/39037465682). That result proves only the isolated authentication check; it does not prove CircleCI secret visibility, remote action execution, useful cache hits or APK production.

If an existing secret or setting is inaccessible, report its name and stop. Do not rotate, recreate or reassign it. Never print a credential.

## Architecture

- **CircleCI:** retain the existing project and orchestration service. The five-stage workflow is a target design and is not yet wired in the migration branch; current config only exposes the opt-in source preflight and a fail-closed build stub.
- **Bare:** the pinned patch series and build/version instructions.
- **Chromium/depot_tools:** checkout and dependency graph at the exact revision declared by the pinned Bare snapshot.
- **Siso:** use the Siso version and configuration contract from that exact Chromium revision. Do not hardcode a Siso version from an older source workflow.
- **BuildBuddy:** keep the existing REAPI service, endpoint, instance and authentication assignment. Adapt the generated Chromium-native Siso/REAPI configuration to the pinned Chromium revision.
- **Remote execution:** enable only after the generated config is verified and a meaningful action proves it. A successful auth check is not proof of remote execution.
- **Cache:** preserve the existing cache service and all existing cache objects. Use a new Bare-specific key namespace for new build state; never clear old cache data or restore incompatible entries. Avoid uploading the full Chromium source/output tree to CircleCI Free storage; use the BuildBuddy/Siso remote action cache for compiled-action reuse and small source-bound stage ledgers for continuity.

## Source adapter requirements

1. Resolve Bare commit and Chromium commit from the pinned source; fail closed on any mismatch.
2. Compute and record the ordered patch count and digest.
3. Verify the Chromium checkout is exactly the pinned commit and clean before applying patches.
4. Apply patches in deterministic filename order with the documented patch-series mechanism; stop on any conflict or already-applied ambiguity.
5. Supply the expected uBlock Origin CRX as a separately versioned/checksummed input.
6. Generate Chromium-native `.gclient` REAPI variables and the credential-helper configuration using existing settings. Inspect generated `.sisoenv` and runtime flags before any remote action.
7. Ensure the build arguments explicitly select the intended Siso/remote-execution path and do not accidentally select a Google-only remote-execution preset.
8. Keep source checkout, hooks, GN generation, local-only actions, compilation, packaging and verification as separate measured phases.
9. Record Bare SHA, Chromium SHA/version, patch digest, extension digest, toolchain/Siso revision, target ABI, GN args, backend config digest, artifact identity and cache evidence.

## Current adapter artifacts

- Source pin and GN args: `ci/bare/source-pin.txt`, `ci/bare/gn_args.gn`.
- Pre-build cache identity: `ci/bare/write_cache_identity.py`.
- Source/build identity and APK verification: `ci/bare/build_identity.py`.
- Identity-checked checkpoint pack/verify/restore: `ci/bare/checkpoint.py`.
- Artifact naming and checksum: `ci/bare/package_artifact.sh`.
- Guarded source bootstrap: `ci/bare/bootstrap_chromium.sh`; it was not executed.

## Cache/checkpoint policy

- Preserve existing cache objects and settings; do not clear them.
- Existing source checkout and local output checkpoints are not presumed compatible with the Bare source identity.
- Reuse content-addressed remote action results only when action inputs and toolchain identity match; prove useful hits with Siso counters/logs.
- Use stable identity keys containing Bare commit, Chromium commit, patch digest, target, toolchain/Siso revision, GN args and backend-config digest.
- Do not key by only branch, run ID or timestamp.
- Reject incomplete, stale, corrupt or mismatched checkpoints. A cache hit, archive restore or green job alone is not proof of useful reuse.

## No-build gates

The migration branch's full-build workflow fails closed. Keep `run_sandium_bare_source_ready=false` until the five stages are wired to the Bare adapters, new source-identity key namespace, small stage ledgers and artifact verifier, and actual remote execution/cache behavior is separately proven.

Before a build is considered:
- validate YAML and shell syntax;
- verify Bare and Chromium pins and patch digest;
- inspect the actual generated Siso configuration without compiling;
- prove the existing secret references and endpoint/instance are unchanged;
- establish storage, runtime and cost from existing account configuration;
- obtain explicit approval for one controlled build.

No Chromium sync, GN generation, compilation, APK packaging or CircleCI pipeline was run as part of this design update.


## Source-only feasibility review — 2026-10-27

### Source bootstrap correction

The active migration branch had drifted from the previous written status: `bootstrap_chromium.sh` still ran `fetch --nohooks android`, which may start a dependency sync before the workflow enforces its pinned Chromium revision. Commit [`952eb6f`](https://github.com/sandeepbimt/Sandium/commit/952eb6f0b3b6eea206b250b954d7f44a2b4d02db) replaces that sequence with `.gclient` configuration, direct fetch of the exact pinned Chromium commit, pin verification before and after a bounded/logged dependency sync, and no build operation. No source sync was run while making this change. No-build workflow [40443430796](https://github.com/sandeepbimt/Sandium/actions/runs/40443430796) passed.

### Persistence feasibility verdict: BLOCKED / NOT PROVEN

Bare's official [README](https://github.com/BareBrowser/bare-browser) and [BUILDING.md](https://github.com/BareBrowser/bare-browser/blob/main/BUILDING.md) describe a roughly 50 GB Chromium checkout, at least 100 GB free disk, 32 GB allocated VM memory, and a build that takes hours. The current CircleCI config on the migration branch uses a small Python Docker executor for source preflight and a fail-closed stub for the full build; no suitable build resource class or durable source store is configured/proven there.

CircleCI's [cache guide](https://circleci.com/docs/guides/optimize/caching/) says cache entries are immutable for a given key and large caches have restore/expansion costs. Its [persist-data guide](https://circleci.com/docs/guides/optimize/persist-data/) describes caches as reuse across jobs/workflows, but the included Free storage allowance and this account's overage/credit eligibility do not prove that a 50 GB source tree or large output checkpoints can be stored affordably. A cache miss also lets a job proceed by doing the work again; a successful restore step is not proof that useful build work was reused.

BuildBuddy/Siso remote action cache can reuse outputs only for compatible action keys. It does not, by itself, prove that a later CircleCI job has the local Chromium source checkout, dependencies, generated GN graph and toolchain state needed to continue. A five-job workflow that uploads the whole source/output tree is not accepted; a five-job workflow that re-syncs/re-generates from scratch at every stage is not accepted either.

### Stage-ledger contract update — source-only, 2026-10-27

Schema 2 has been implemented in the active Bare adapter. Current source commits include [`7307a08`](https://github.com/sandeepbimt/Sandium/commit/7307a08495facb2d5e2fd1be302d9d74157184b3), [`05aa490`](https://github.com/sandeepbimt/Sandium/commit/05aa490da9d02ec97b30565f27224f5c0a096538), [`a344207`](https://github.com/sandeepbimt/Sandium/commit/a344207e970e43562397067d14a9c01c87190be8), and [`440aaa9`](https://github.com/sandeepbimt/Sandium/commit/440aaa98980e498d5bea551d0097a51fac68f31f).

- **Stage 1:** requires successful source/dependency preparation evidence; no Siso counters are fabricated.
- **Stage 2:** requires effective GN arguments and a generated `build.ninja` graph.
- **Stage 3:** requires actual uncached remote Siso action execution.
- **Stage 4:** requires both a remote-cache hit and additional uncached remote action execution in the same invocation. A cache hit alone is not forward progress.
- **Stage 5:** validates the prior source/GN identity chain and directly reruns APK structure/content and `apksigner` verification, checking the manifest's size/hash.

The stable identity excludes only the not-yet-generated GN fingerprint; the fingerprint is established at Stage 2 and must remain unchanged thereafter. Siso progress counters are invocation-local and are not summed across stages. These source changes are not wired to build jobs, and the no-build test result must be confirmed before describing the implementation as test-passing.

### Persistence feasibility reassessment — 2026-10-27

**Verified public constraints:**

- Bare's [official README](https://github.com/BareBrowser/bare-browser) states that the Chromium checkout is about 50 GB, recommends about 100 GB free disk and at least 32 GB allocated to the Docker VM; full builds take hours.
- CircleCI's [current pricing page](https://circleci.com/pricing/) lists the Free plan with 30,000 monthly credits, 1 GB included network transfer and 2 GB-months of storage. The [Free-plan credit guide](https://circleci.com/docs/guides/plans-pricing/credits/) confirms that excess network/storage usage draws from the monthly credit allotment.
- CircleCI [cache guidance](https://circleci.com/docs/guides/optimize/caching/) says caches are immutable by key, a cache miss continues with work instead of restoring, and large cache restores can cost more time than regenerating data. CircleCI [persistence guidance](https://circleci.com/docs/guides/optimize/persist-data/) describes workspaces as data passed to downstream jobs through a workflow, not a durable cross-workflow source tree.
- BuildBuddy/Siso remote action cache can reuse compatible action results. It does not independently provide the later job with the local Chromium checkout, DEPS dependencies, generated GN graph, toolchain, and output directory.

**Assessment:** a raw 50 GB source checkout is 25 times the Free storage allotment and 50 times the included network-transfer allotment, before GN/build outputs or any transfer retries. Compression could reduce transferred bytes, but there is no measured archive size, restore duration, or account-level credit budget for this exact source/build state. Nor is there evidence that the current account provides a persistent runner disk with Bare's required capacity. It would be unjustified to assume that a full source/output archive can be handed between stages within the user's current entitlements. It is equally unjustified to declare the architecture categorically impossible without account-level usage and runner details.

**Conclusion:** the five-stage approach is **not demonstrated feasible under the known constraints**. Do not wire it based on a small-ledger handoff alone, and do not replace it with a cold Chromium sync in each stage. Keep `run_sandium_bare_source_ready=false`.

### Required next action

Inspect the existing CircleCI project/account's actual storage/network-credit usage and available runner/resource classes, then establish whether one existing workspace can retain at least the required source plus build state with sufficient disk, RAM, and runtime across the proposed jobs. Do this as a read-only feasibility check; do not trigger a build, change credentials, clear caches, or create a new infrastructure project. If current entitlements cannot support that state, explicitly re-scope the stage strategy instead of pretending it can.


## Read-only CircleCI feasibility assessment — 2026-10-27

### Publicly verified plan limits

- CircleCI's current [pricing page](https://circleci.com/pricing/) and [credit documentation](https://circleci.com/docs/guides/plans-pricing/credits/) list Free as **30,000 credits/month**, **1 GB included network transfer** and **2 GB-months included storage**. Excess storage/network usage consumes credits; when personal Free credits reach zero, builds are blocked until the monthly refill.
- The public [resource class documentation](https://circleci.com/docs/guides/execute/resource-class-overview/) lists a Linux VM `xlarge` class with 8 vCPU, 32 GB RAM and 150 GB disk in the resource tables. Resource-class access is plan-dependent. The current Sandium migration config uses `cimg/python:3.12` in a Docker executor and does not request this VM class; it is only a source-preflight job, not a Chromium builder.
- CircleCI [workspaces](https://circleci.com/docs/guides/orchestrate/workspaces/) are per-workflow, additive-only data transfer between jobs, stored off-executor and unpacked into downstream jobs. Default/max retention is 15 days. They do not create a durable shared checkout for a later, newly triggered workflow.
- CircleCI's [persistence guide](https://circleci.com/docs/guides/optimize/persist-data/) confirms workspaces, caches and artifacts use stored data; usage can be inspected in the web UI under Plan → Usage, with storage and network detail on the Network/Storage views.

### Size comparison against Bare's published requirement

Bare's [official build documentation](https://github.com/BareBrowser/bare-browser/blob/main/BUILDING.md) says the Chromium checkout is roughly 50 GB, recommends at least 100 GB free disk, and 32 GB allocated VM memory.

Using the uncompressed source size as a planning baseline:
- 50 GB is **25×** the 2 GB-month included storage amount.
- 50 GB is **50×** the 1 GB included network-transfer amount.

These ratios are not a prediction of billable usage for a compressed archive: actual transfer depends on compression, cache deduplication and how CircleCI meters the object. They do show that persisting the raw source tree through CircleCI-managed storage cannot be assumed free. Build outputs and repeated workspace restores would add more.

### What could work in principle, and what is not proven

A single CircleCI Linux VM job could, in principle, have a resource class whose published disk/RAM fit Bare's stated baseline. That does **not** establish that the user's current Free organization can select that class, that it has enough remaining monthly credits, or that the current runtime limits allow a Chromium build. The current CircleCI account's plan, remaining credits, usage, job-level resource-class access, configured runtime cap, storage/network usage and retention settings were not accessible through the connected tools. No account values are inferred.

A multi-job five-stage workflow can use a workspace to transfer state within one workflow, but it must upload and later download/unpack the source/build tree. That transfer is large, and the workspace does not persist across newly triggered workflows. A small ledger alone does not transfer the actual source checkout or generated build graph. BuildBuddy/Siso action cache is useful for compatible action outputs, but does not substitute for the local source, dependencies, GN graph and toolchain needed by later jobs.

### Assessment

**Current verdict: not demonstrated feasible within the user's actual account constraints.** The public Free limits show that a raw 50 GB handoff would greatly exceed included storage/network allotments; public resource-class tables show a possible RAM/disk class but do not prove entitlement. Because the account-level usage and class access could not be read, this is a conditional assessment, not a categorical claim that CircleCI cannot do the build.

### Exact read-only checks still required in the CircleCI UI

1. Open **Organization → Plan / Usage** and record the plan name, remaining credits for this month, monthly credit allowance, and any usage caps.
2. Open **Usage → Network / Storage** and inspect storage volume, storage activity, and network transfer for the Sandium project; note whether excess use is already drawing credits.
3. Open the existing Sandium project settings/configuration and verify which executor/resource classes are actually available to this project, whether a Linux VM `xlarge` class is selectable, and the effective job timeout/runtime limit.
4. Review the existing workspace/cache retention controls and the actual cache/workspace usage. Do not clear, recreate, or overwrite any existing cache.

Record the results without changing settings. Do not launch a build as a way to discover limits.

### Decision and next action

Do not wire the five-stage pipeline yet. First obtain those account-specific values and calculate the expected cost/transfer for the chosen state-transfer mechanism. If the existing plan cannot support a durable workspace and adequate builder resources, re-scope the workflow rather than introducing repeated cold syncs or assuming a large archive will be affordable. Keep `run_sandium_bare_source_ready=false`.
