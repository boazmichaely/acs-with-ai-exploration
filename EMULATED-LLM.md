# Emulated LLM enrichments (no API key)

The files under `data/enrichments/*.json` are **`ai_analysis` JSON** meant to match the contract in `../ai_analysis-schema.json` and `../prompt-template.md` (including **`one_sentence_summary`** for the UI hero line), the same way you would get from:

- A **Cursor / chat assistant** acting as the enrichment LLM (paste `sample-alerts/alert-NN.json` and ask for JSON only), or  
- A real OpenAI-compatible API later.

This repo **does not** require an LLM API to build the UI mock.

To **re-populate all rows** as if the prompt were run once per alert (assistant-authored `ai_analysis` from each `sample-alerts/alert-NN.json`), edit `data/enrichments/*.json` and run `sync-mock-data.py`—same deliverable shape as a batched LLM, just without HTTP.

## Regenerate `mock-data.js` after editing alerts or enrichments

```bash
cd prompt-exploration/ui-prototype
python3 scripts/sync-mock-data.py
```

`sync-mock-data.py` only **bundles** `../sample-alerts/` + `data/enrichments/` → `data/alerts/`, `manifest.json`, and `mock-data.js`. It does not call any network LLM.

## Adding a new alert row

1. Add `sample-alerts/alert-11.json` (and bump the loop in `sync-mock-data.py` from `1..10` to `1..11`), **or** replace an existing slot.
2. Create `data/enrichments/11.json` with `{ "ai_analysis": { ... } }` from an emulated or real LLM run.
3. Run `sync-mock-data.py` again.
