# MedEase Backend

## 1. Create `.env`

Copy `.env.example` to `.env` and fill in your CloseAI key.

## 2. Install dependencies

```powershell
python -m pip install -r backend\requirements-backend.txt
```

## 3. Run the backend

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```

Or:

```powershell
powershell -ExecutionPolicy Bypass -File backend\run_backend.ps1
```

## 4. Health check

Open:

```text
http://127.0.0.1:8000/api/health
```

## Notes

- The frontend keeps session history in `localStorage`.
- This backend only exposes `GET /api/health` and `POST /api/explain`.
- CloseAI is called through the OpenAI-compatible `/v1/chat/completions` interface.
- If `ready` is `false` on `/api/health`, your `.env` is missing `CLOSEAI_API_KEY`.
- Lightweight research logs are written to `backend/logs/explain-events.jsonl`.
- Logs do not store the raw input text by default; they store input hash, length, complexity outputs, semantic features, and UI actions.
- You can disable logging with `MEDEASE_LOGGING_ENABLED=false` in `.env`.

## Log aggregation for paper writing

Run:

```powershell
python scripts\summarize_medease_logs.py
```

This generates:

- `reports/medease_log_events.csv`
- `reports/medease_log_summary.md`

For paper-ready draft text and simple SVG figures, run:

```powershell
python scripts\generate_medease_paper_materials.py
```

This generates:

- `reports/medease_methods_results_draft.md`
- `reports/medease_methods_results_polished.md`
- `reports/medease_load_distribution.svg`
- `reports/medease_ui_actions.svg`
