# Violations + AI enrichment (UI mock)

Static demo of a violations table with an "Enrich with AI" flow: bulk selection, side drawer with AI summary (risk, score, one-line summary, prose), and an ACS-only policy/violation modal. Data is bundled in `mock-data.js`.

## Run

Keep `violations-enrichment-mock.html` and `mock-data.js` in the same folder. Open the HTML file in a browser (double-click or File → Open).

## Contents

- **violations-enrichment-mock.html** — Table (10 rows), checkboxes, "Enrich with AI" bulk action, AI summary drawer, policy-link → ACS-only modal. PatternFly 5 (CDN).
- **mock-data.js** — Inline bundle (manifest + alerts + enrichments).
- **data/** — Same content as JSON (for reference or regeneration).
- **scripts/sync-mock-data.py** — Rebuilds `data/` and `mock-data.js` from source alerts + enrichments (see `EMULATED-LLM.md` if you need to regenerate).

## Share

Zip `violations-enrichment-mock.html` and `mock-data.js`; recipient can open the HTML locally.
