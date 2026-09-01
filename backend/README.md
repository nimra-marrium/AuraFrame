# Backend (FastAPI)
## Setup

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then fill in real values
```

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env     # then fill in real values
```

## Run
```
uvicorn app.main:app --reload
```
Visit http://localhost:8000/health - should return {"status": "ok"}
Visit http://localhost:8000/docs - interactive API docs (FastAPI gives you this for free)

**Note:** the /docs "Try it out" UI has been unreliable specifically with the `authorization` header field on endpoints that require a Bearer token. If a request seems to silently ignore your token, use the Python test scripts (`test_create_project.py`, `test_full_pipeline.py`) instead - they use the `requests` library and work reliably.

## Structure
Every folder under `app/modules/` is a self-contained module:
- `schemas.py` - the input/output data contract
- `service.py` - the actual logic (testable without HTTP)
- `router.py`  - thin HTTP layer that calls service.py

To enable a module, uncomment its import + include_router lines in `app/main.py`.

See `../backend-modules-reference.md` (project root) for full detail on every module's responsibility, precondition/postcondition, and security pattern.