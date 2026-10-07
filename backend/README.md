# Backend

FastAPI service for TODO List Voice Note.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests

```bash
pytest
```

## Endpoints

`GET /health`

```json
{"status":"ok"}
```
