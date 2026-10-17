#!/usr/bin/env python3
"""Lightweight, offline validation of Sandium project documentation."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "SANDIUM_STARTER.md", "SANDIUM_STATUS.md", "SANDIUM_KNOWLEDGE.md",
    "SANDIUM_DECISIONS.md", "SANDIUM_FAILURE_LEARNINGS.md",
    "SANDIUM_EXPERIMENT_LOG.md", "SANDIUM_BUILD_NOTES.md",
    "SANDIUM_TEST_PLAN.md", "SANDIUM_CHAT_HANDOFF.md",
    "SANDIUM_CI_ARCHITECTURE.md", "SANDIUM_CLEAN_BASE_LEDGER.md",
]
errors = []
for name in REQUIRED:
    path = ROOT / name
    if not path.is_file():
        errors.append(f"Missing required document: {name}")
        continue
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        errors.append(f"Empty required document: {name}")
    if not text.endswith("\n"):
        errors.append(f"Missing final newline: {name}")

# Check local Markdown links in root-level project docs.
for name in REQUIRED:
    path = ROOT / name
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target_path = (path.parent / target.split("#", 1)[0]).resolve()
        if not target_path.exists():
            errors.append(f"Broken local link in {name}: {target}")

# Require the most important project-boundary and evidence rules to remain visible.
checks = {
    "SANDIUM_STARTER.md": ["SANDFOX", "Do not start a build"],
    "SANDIUM_KNOWLEDGE.md": ["SANDFOX", "forward progress"],
    "SANDIUM_STATUS.md": ["Single next action", "Current blocker"],
    "SANDIUM_CI_ARCHITECTURE.md": ["PROPOSED", "SANDFOX"],
}
for name, phrases in checks.items():
    path = ROOT / name
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase.lower() not in text.lower():
                errors.append(f"Required safeguard phrase missing from {name}: {phrase}")

if errors:
    print("SANDIUM_DOCS_VALIDATION=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)
print(f"SANDIUM_DOCS_VALIDATION=PASS documents={len(REQUIRED)}")
print("This check is documentation-only; it does not build or trigger browser CI.")
