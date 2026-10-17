#!/usr/bin/env python3
"""Evidence-only GitHub Actions recorder for Sandium. Never builds the browser."""
import json, os, subprocess, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "https://api.github.com"
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
STATE_PATH = ROOT / ".sandium" / "recorder-state.json"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
TICK = chr(96)

def api(path):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + TOKEN,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "sandium-evidence-recorder"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def append(path, heading, body):
    text = path.read_text(encoding="utf-8")
    if heading in text:
        return
    path.write_text(text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", encoding="utf-8")

def replace_generated(path, start, end, body):
    text = path.read_text(encoding="utf-8")
    a, b = text.find(start), text.find(end)
    block = start + "\n" + body.strip() + "\n" + end
    if a >= 0 and b >= a:
        text = text[:a] + block + text[b + len(end):]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")

def main():
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {"seen_run_ids": []}
    seen = {int(x) for x in state.get("seen_run_ids", [])}
    runs = api("/repos/" + REPO + "/actions/runs?per_page=100").get("workflow_runs", [])
    fresh = []
    for run in reversed(runs):
        rid, name = int(run["id"]), (run.get("name") or run.get("path") or "unknown-workflow")
        low_name = name.lower()
        if rid in seen or "recordkeeper" in low_name or "documentation validation" in low_name:
            continue
        if run.get("status") == "completed":
            fresh.append(run)
    for run in fresh:
        rid = int(run["id"])
        name, conclusion = run.get("name") or "unknown-workflow", run.get("conclusion") or "unknown"
        sha, branch = run.get("head_sha") or "UNKNOWN", run.get("head_branch") or "UNKNOWN"
        url, number = run.get("html_url") or "UNKNOWN", run.get("run_number", "UNKNOWN")
        jobs = api("/repos/" + REPO + "/actions/runs/" + str(rid) + "/jobs?per_page=100").get("jobs", [])
        job_summary = "; ".join(str(j.get("name", "job")) + ": " + str(j.get("conclusion") or j.get("status") or "UNKNOWN") for j in jobs) or "UNKNOWN"
        artifacts = api("/repos/" + REPO + "/actions/runs/" + str(rid) + "/artifacts?per_page=100").get("artifacts", [])
        artifact_summary = "; ".join(str(a.get("name", "artifact")) + " (expired=" + str(a.get("expired", "UNKNOWN")) + ", size=" + str(a.get("size_in_bytes", "UNKNOWN")) + " bytes)" for a in artifacts) or "No artifacts reported by GitHub."
        heading = "### GitHub Actions run " + str(rid)
        record = (
            "- **Recorded:** " + NOW + "\n"
            "- **Workflow/run:** " + name + " / run #" + str(number) + " (run ID " + TICK + str(rid) + TICK + ")\n"
            "- **Branch/commit:** " + TICK + branch + TICK + " / " + TICK + sha + TICK + "\n"
            "- **Conclusion:** **" + conclusion.upper() + "**; created " + str(run.get("created_at", "UNKNOWN")) + ", last updated " + str(run.get("updated_at", "UNKNOWN")) + "\n"
            "- **Jobs:** " + job_summary + "\n"
            "- **Artifacts:** " + artifact_summary + "\n"
            "- **Run evidence:** " + url + "\n"
            "- **Qualification:** Automatically recorded CI evidence only. This run does NOT by itself qualify as an accepted clean base. APK integrity, install/smoke tests, source/config pins and explicit acceptance evidence remain mandatory.\n")
        low_name = name.lower()
        # General workflow evidence belongs in the experiment log. Only build-related
        # workflows belong in build notes; only build/artifact candidates belong in the clean-base ledger.
        append(ROOT / "SANDIUM_EXPERIMENT_LOG.md", heading, record)
        build_related = any(term in low_name for term in ("build", "android", "apk", "checkpoint", "compile", "artifact", "clean-base"))
        if build_related:
            append(ROOT / "SANDIUM_BUILD_NOTES.md", heading, record)
        if build_related and artifacts:
            append(ROOT / "SANDIUM_CLEAN_BASE_LEDGER.md", heading,
                   record + "\n- **Automatic classification:** CANDIDATE ONLY; acceptance requires source/config pins, artifact integrity, install/smoke tests and required test evidence.\n")
        if conclusion != "success":
            append(ROOT / "SANDIUM_FAILURE_LEARNINGS.md", "### Automated CI outcome — run " + str(rid),
                   record + "\n**Diagnosis:** Not inferred automatically. Inspect linked job logs before assigning root cause.\n")
        seen.add(rid)
    state["seen_run_ids"] = sorted(seen)[-500:]
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    latest = next((r for r in runs if r.get("status") == "completed" and "recordkeeper" not in (r.get("name") or "").lower()), None)
    if latest:
        latest_block = (
            "- **Latest observed completed GitHub run:** " + str(latest.get("name", "UNKNOWN")) + " / run #" + str(latest.get("run_number", "UNKNOWN")) + " (" + str(latest.get("conclusion", "UNKNOWN")) + ") — " + str(latest.get("html_url", "UNKNOWN")) + "\n"
            "- **Commit:** " + TICK + str(latest.get("head_sha", "UNKNOWN")) + TICK + "; branch " + TICK + str(latest.get("head_branch", "UNKNOWN")) + TICK + "\n"
            "- **Boundary:** GitHub evidence is polled automatically. CircleCI is not covered until a Sandium-only integration is configured and tested. ChatGPT must still record decisions and findings GitHub cannot observe.\n")
    else:
        latest_block = "- No completed GitHub workflow run was available from the API.\\n"
    for path in [ROOT / "SANDIUM_STATUS.md", ROOT / "SANDIUM_CHAT_HANDOFF.md"]:
        replace_generated(path, "<!-- SANDIUM_AUTO_STATUS_START -->", "<!-- SANDIUM_AUTO_STATUS_END -->", latest_block)
    changed = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if changed:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
        subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
        paths = ["SANDIUM_CLEAN_BASE_LEDGER.md", "SANDIUM_EXPERIMENT_LOG.md", "SANDIUM_FAILURE_LEARNINGS.md", "SANDIUM_BUILD_NOTES.md", "SANDIUM_STATUS.md", "SANDIUM_CHAT_HANDOFF.md", ".sandium/recorder-state.json"]
        subprocess.run(["git", "add"] + paths, cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-m", "docs: record verified GitHub workflow evidence"], cwd=ROOT, check=True)
        subprocess.run(["git", "push"], cwd=ROOT, check=True)
        print("SANDIUM_RECORDER=COMMITTED")
    else:
        print("SANDIUM_RECORDER=NO_CHANGES")
    print("SANDIUM_RECORDER_NEW_RUNS=" + str(len(fresh)))
    return 0

if __name__ == "__main__":
    main()
