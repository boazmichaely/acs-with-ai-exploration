# Violations + AI enrichment (concept illustration)

Static demo of a violations table with an "Enrich with AI" flow: bulk selection, side drawer with AI summary (risk, score, one-line summary, prose), and an ACS-only policy/violation modal. Data is bundled in **demo/mock-data.js**.

## Run the demo

Open **demo/violations-enrichment-mock.html** in a browser (double-click or File → Open). Keep **mock-data.js** in the same folder (demo/); the script writes it there.

## Templates

Templates live in **templates/**:

- **templates/prompt-template.md** — Prompt sent to the LLM (system + user message). Defines the input and instructions for enrichment.
- **templates/ai_analysis-schema.json** — Response template: the required JSON shape for the LLM reply (`ai_analysis` with one_sentence_summary, risk_level, prioritization_score, etc.). The UI and validation use this shape.

## Regenerate data and mock-data.js

From the **repo root**:

```bash
python3 scripts/sync-mock-data.py
```

Requires **sample-alerts/** (alert-01.json … alert-10.json) and **data/enrichments/** (01.json … 10.json). The script copies sample-alerts into data/alerts/, builds data/manifest.json, and writes **demo/mock-data.js**. See **EMULATED-LLM.md** for how enrichments are produced without a real LLM.

## Contents

| Path | Role |
|------|------|
| **templates/** | prompt-template.md, ai_analysis-schema.json. |
| **demo/** | violations-enrichment-mock.html, mock-data.js (runnable demo). |
| **data/** | manifest.json, alerts/*.json, enrichments/*.json (built/used by script). |
| **sample-alerts/** | Source alert payloads (alert-01.json … alert-10.json). |
| **scripts/sync-mock-data.py** | Rebuilds data/ and demo/mock-data.js. |
| **examples/sample-enrichment-output.json** | One filled example conforming to the schema. |
| **EMULATED-LLM.md** | How enrichments are emulated. |

## Share

Zip **demo/violations-enrichment-mock.html** and **demo/mock-data.js**; the recipient can open the HTML in a browser.
