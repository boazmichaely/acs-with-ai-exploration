# Violations + AI enrichment (concept illustration)

Static demo of a violations table with an "Enrich with AI" flow: bulk selection, side drawer with AI summary (risk, score, one-line summary, prose), and an ACS-only policy/violation modal. Data is bundled in `mock-data.js`.

## Run the demo

Keep `violations-enrichment-mock.html` and `mock-data.js` in the same folder. Open the HTML file in a browser (double-click or File → Open).

## Templates

- **prompt-template.md** — Prompt sent to the LLM (system + user message). Defines the input and instructions for enrichment.
- **ai_analysis-schema.json** — Response template: the required JSON shape for the LLM reply (`ai_analysis` with one_sentence_summary, risk_level, prioritization_score, etc.). The UI and validation use this shape.

## Regenerate data and mock-data.js

From the **repo root**:

```bash
python3 scripts/sync-mock-data.py
```

Requires **sample-alerts/** (alert-01.json … alert-10.json) and **data/enrichments/** (01.json … 10.json). The script copies sample-alerts into data/alerts/, builds data/manifest.json, and writes mock-data.js. See **EMULATED-LLM.md** for how enrichments are produced without a real LLM.

## Contents

| Path | Role |
|------|------|
| **prompt-template.md** | Prompt template for the LLM. |
| **ai_analysis-schema.json** | Response template (JSON schema). |
| **violations-enrichment-mock.html** | Demo UI (table, bulk enrich, drawer, ACS modal). |
| **mock-data.js** | Bundled manifest + alerts + enrichments for the demo. |
| **data/** | manifest.json, alerts/*.json, enrichments/*.json (built/used by script). |
| **sample-alerts/** | Source alert payloads (alert-01.json … alert-10.json). |
| **scripts/sync-mock-data.py** | Rebuilds data/ and mock-data.js. |
| **examples/sample-enrichment-output.json** | One filled example conforming to the schema. |
| **EMULATED-LLM.md** | How enrichments are emulated. |

## Share

Zip `violations-enrichment-mock.html` and `mock-data.js`; the recipient can open the HTML in a browser.
