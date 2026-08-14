# Backend (FastAPI)

## Setup
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env     # then fill in real values (Windows: copy, Mac/Linux: cp)
```

## Run
```
uvicorn app.main:app --reload
```
Visit http://localhost:8000/health -> should return {"status": "ok"}
Visit http://localhost:8000/docs -> interactive API docs

## Structure
Every folder under `app/modules/` is self-contained:
- `schemas.py` - input/output data contract
- `service.py` - actual logic (testable without HTTP)
- `router.py`  - thin HTTP layer

To enable a module, uncomment its import + include_router lines in `app/main.py`.
