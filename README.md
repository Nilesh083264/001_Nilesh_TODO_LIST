# TODO List Voice Note

Voice-first TODO and reminder application with a FastAPI backend and native Android client.

The MVP flow is:

```text
Wake word -> speech-to-text -> FastAPI command endpoint -> Gemini parsing -> TODO persistence -> Android local reminder
```

## Repository Structure

```text
backend/  FastAPI service, schemas, repositories, integrations, and tests
android/  Native Android application
data/     Repository-level data placeholder for MVP artifacts
docs/     Project documentation
```

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Run tests:

```bash
cd backend
pytest
```

## Android

The Android app is a native Kotlin shell under `android/`.

```bash
cd android
gradle :app:assembleDebug
```

Install Android SDK tooling and configure `local.properties` or `ANDROID_HOME` before building locally.

## Configuration

Copy `.env.example` files as needed and fill values locally. Do not commit real secrets.
