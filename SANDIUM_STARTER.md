## SANDIUM — Android Browser Project Charter

**Product:** SANDIUM Browser  
**Platform:** Android  
**Initial codebase:** Official Brave Android source  
**Status:** Independent project; planning and source investigation first.

## Mission

Build a polished, fast, privacy-conscious Android browser based initially on regular Brave. Understand the existing architecture before removing features or rebuilding components.

Long-term goals: fast launch and browsing; strong ad/tracker blocking; excellent dark-page rendering; reliable PWA installation and standalone behavior; privacy and stability; maintainable upstream changes.

## Mandatory project separation

Sandium is a new, independent project, not a continuation or rename of SANDFOX.

- All Sandium source, development, CI workflows, builds, artifacts, logs, checkpoints and project documentation must live in the Sandium repository or infrastructure separately configured for Sandium.
- SANDFOX may be inspected for lessons and reference only. Do not trigger or depend on its builds, workflows, credentials, caches, checkpoints, artifacts or source checkout.
- Do not modify existing SANDFOX CircleCI, BuildBuddy or Siso configuration or infrastructure.
- Independently review and implement any adopted idea; never assume old cache/checkpoint behavior works for Sandium.

## Engineering method: DIRTFT

UNDERSTAND → MINIMAL CHANGE → TEST → LEARN → PRESERVE → PROCEED.

For each failure: inspect actual logs; classify the failure; record what is and is not proved; make the smallest justified fix; inspect the full diff; run one targeted validation; preserve the lesson. Never make speculative commits or launch overlapping expensive builds. Optimize information gained per test.

## Resource constraints

- No paid GitHub upgrade is planned.
- Do not assume full Chromium checkout/build fits a CI budget without evidence.
- Before any expensive run, document source pins, dependencies, storage, memory, bandwidth, cache persistence, remote execution needs, expected runtime, cost, success criteria and diagnostics.
- Do not claim resumability or cross-run reuse until logs prove it.

## Initial technical direction

Official entry points:
- Brave Core: https://github.com/brave/brave-core
- Brave browser repository: https://github.com/brave/brave-browser
- Brave Siso documentation: https://github.com/brave/brave-core/blob/master/docs/siso_customization.md

These are investigation starting points, not proof of build feasibility. Select a revision based on reproducibility, security support, build feasibility and a clear update strategy. Do not start a build until the source-level feasibility audit is complete and reviewed.

Establish which repositories provide Android app and core code, how Chromium is synchronized, exact toolchain/SDK/NDK/JDK requirements, official Android build flow, output APK and verification method, cache/remote execution behavior, resource needs and a reproducible path under constraints.

## Scope order

1. Source/build feasibility.
2. Reproducible baseline APK.
3. Install and launch on a real Android device.
4. Basic navigation and compatibility.
5. Measure cold/warm launch and page loading.
6. Verify built-in blocking.
7. Investigate extension/uBlock compatibility.
8. Verify PWA behavior.
9. Investigate dark-page integration.
10. Measure performance and memory.
11. Make carefully scoped UI/privacy changes.
12. Brand the working product as SANDIUM.

Every stage needs explicit pass criteria and retained evidence.

## Baseline measurements

Once an APK exists, record device model, Android version, build revision, test conditions and method. Measure cold/warm launch, cold/warm navigation, first launch and process-death recovery, memory, blocking, PWA install/launch/navigation/back-forward/reload/external links, and dark rendering across native-dark, image/video, SVG, canvas, code and embedded content.

## Documentation system

Maintain SANDIUM_STATUS.md, SANDIUM_KNOWLEDGE.md, SANDIUM_DECISIONS.md, SANDIUM_FAILURE_LEARNINGS.md, SANDIUM_EXPERIMENT_LOG.md, SANDIUM_BUILD_NOTES.md, SANDIUM_TEST_PLAN.md, SANDIUM_CHAT_HANDOFF.md and SANDIUM_CI_ARCHITECTURE.md. Repository records are authoritative; chat history is supplementary. Never store secrets. Preserve history and label verified facts, hypotheses, rejected approaches and superseded decisions separately.

## Definition of progress

Progress means reducing uncertainty with reliable evidence, producing a reproducible baseline, preserving learning and moving toward a stable Android browser without wasting resources or entangling SANDFOX.
