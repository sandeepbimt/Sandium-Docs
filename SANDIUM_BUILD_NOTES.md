# SANDIUM — Reproducible Build Notes

## Current status

No Sandium Android build has been run. Do not treat SANDFOX pins, commands, outputs or credentials as a Sandium baseline.

## Source pins

- Brave Core URL / exact commit:
- Brave Android URL / exact commit or tag:
- Chromium revision resolved by that Brave revision:
- Sandium patch-set commit:
- Dependency synchronization method:
- Pin date and rationale:
- Security/update strategy:

## Environment

- Runner/provider/image and architecture:
- OS:
- CPU / RAM / free disk:
- Git / Python / Node / package manager:
- JDK / Android SDK / NDK / build tools:
- GN / Ninja / Siso versions:
- BuildBuddy endpoint/instance identifier (never credentials):
- Remote execution availability, quota and pricing:

## Reproducible procedure

Only add commands verified against the selected source revision. For each, document working directory, purpose, expected output and diagnostics.

1. Preflight:
2. Source checkout and dependency sync:
3. Toolchain setup:
4. Build graph generation:
5. Build command/target:
6. APK path and integrity verification:
7. Install and smoke test:

## Cache and checkpoint contract

For each layer record purpose, identity key, stored paths, source/config compatibility checks, Siso state/journal behavior, required file metadata, archive size, pack/transfer/restore time, hit evidence, forward-progress evidence, invalidation, retention, cost and recovery.

Distinguish source/dependency reuse, remote action cache, runner-local cache, serialized checkpoint archive and same-workflow workspace. A cache-hit count alone is not proof of successful resume.

## Resource measurements

| Experiment / run | Checkout + deps | Peak disk | Peak RAM | Runtime | Archive size | Restore time | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Not measured | — | — | — | — | — | — | No Sandium build run |

## Artifact contract

Record source/config identity, workflow run, artifact path, size, SHA-256, archive integrity, signing/debug state and device install/smoke test. Never commit signing keys or secrets.
