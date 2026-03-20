#!/usr/bin/env python3
r"""Bundle sample alerts + enrichments into data/ and mock-data.js.

Does NOT call an external LLM. Expected workflow:

1. `data/enrichments/01.json` … `10.json` — each file is `{"ai_analysis": { ... }}`
   produced by emulating the prompt in `templates/prompt-template.md` (e.g. with each
   `sample-alerts/alert-NN.json`), or pasted from any LLM later.

2. Run this script to copy sample-alerts/ → data/alerts/, build manifest.json,
   and write mock-data.js.

Usage (from repo root):

  python3 scripts/sync-mock-data.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
SAMPLE = os.path.join(REPO_ROOT, "sample-alerts")
OUT = os.path.join(REPO_ROOT, "data")
DEMO_DIR = os.path.join(REPO_ROOT, "demo")


def sev_label(sev: str) -> tuple[str, str]:
    if "CRITICAL" in (sev or ""):
        return "CRITICAL", "red"
    if "HIGH" in (sev or ""):
        return "High", "orange"
    if "MEDIUM" in (sev or ""):
        return "Medium", "gold"
    if "LOW" in (sev or ""):
        return "Low", "blue"
    return "Unknown", "grey"


def lifecycle_display(ls: str | None) -> str:
    if not ls:
        return "—"
    return {"DEPLOY": "Deploy", "BUILD": "Build", "RUNTIME": "Runtime"}.get(ls, ls)


def main() -> int:
    if not os.path.isdir(SAMPLE):
        print(f"Error: sample-alerts not found at {SAMPLE}", file=sys.stderr)
        return 1

    os.makedirs(os.path.join(OUT, "alerts"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "enrichments"), exist_ok=True)
    manifest: dict = {"alerts": []}

    for i in range(1, 11):
        slug = f"{i:02d}"
        src = os.path.join(SAMPLE, f"alert-{slug}.json")
        enc_path = os.path.join(OUT, "enrichments", f"{slug}.json")
        if not os.path.isfile(enc_path):
            print(
                f"Error: missing {enc_path}\n"
                "Create it with emulated LLM output (see templates/prompt-template.md + sample-alerts).",
                file=sys.stderr,
            )
            return 1

        with open(enc_path, encoding="utf-8") as f:
            enrichment = json.load(f)
        if "ai_analysis" not in enrichment:
            print(f"Error: {enc_path} must contain top-level ai_analysis", file=sys.stderr)
            return 1

        with open(src, encoding="utf-8") as f:
            alert = json.load(f)
        shutil.copy(src, os.path.join(OUT, "alerts", f"{slug}.json"))

        pol = alert.get("policy") or {}
        dep = alert.get("deployment") or {}
        sev_name, sev_pf = sev_label(pol.get("severity", ""))
        v0 = (alert.get("violations") or [{}])[0]
        msg = v0.get("message") or ""
        prev = msg[:80] + ("…" if len(msg) > 80 else "")

        manifest["alerts"].append(
            {
                "slug": slug,
                "id": alert.get("id"),
                "policyName": pol.get("name"),
                "entity": dep.get("name") or "—",
                "clusterNs": f'{alert.get("clusterName")}/{alert.get("namespace")}',
                "severity": sev_name,
                "severityPf": sev_pf,
                "category": (pol.get("categories") or ["—"])[0],
                "lifecycle": lifecycle_display(alert.get("lifecycleStage")),
                "timeDisplay": "Mar 09, 2026, 4:16:16 PM EDT",
                "violationPreview": prev,
            }
        )

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    bundle = {
        "manifest": manifest,
        "alerts": {},
        "enrichments": {},
    }
    for i in range(1, 11):
        slug = f"{i:02d}"
        with open(os.path.join(OUT, "alerts", f"{slug}.json"), encoding="utf-8") as f:
            bundle["alerts"][slug] = json.load(f)
        with open(os.path.join(OUT, "enrichments", f"{slug}.json"), encoding="utf-8") as f:
            bundle["enrichments"][slug] = json.load(f)

    os.makedirs(DEMO_DIR, exist_ok=True)
    mock_js = os.path.join(DEMO_DIR, "mock-data.js")
    with open(mock_js, "w", encoding="utf-8") as f:
        f.write("window.__MOCK_DATA__ = ")
        f.write(json.dumps(bundle, separators=(",", ":")))
        f.write(";\n")

    print("Wrote", os.path.join(OUT, "manifest.json"))
    print("Wrote", mock_js)
    return 0


if __name__ == "__main__":
    sys.exit(main())
