# AuraFrame

An AI-powered creative workspace that turns scattered visual inspiration
and a plain-language brief into a structured creative direction and an
editable mood board.

## Structure

```
frontend/   Next.js app (the UI) - not yet built
backend/    FastAPI app (the API + AI orchestration) - COMPLETE
```

## Status

✅ **Backend: 100% complete** - all 11 modules built and verified working
end-to-end, including real Supabase Row Level Security, Gemini-powered
multimodal AI agents, and file storage.

⬜ **Frontend: not started** - next phase.

⬜ **Deployment: not started** - happens after frontend is complete.

## Backend module map

See `backend-modules-reference.md` for full detail on every module -
responsibilities, preconditions/postconditions, file locations, and
security patterns. Quick summary:

| # | Module | What it does |
|---|--------|---------------|
| 1 | Auth | Signup/login via Supabase Auth |
| 2 | Project | Create/read a project + brief |
| 3 | Image Upload | Store reference images |
| 4 | Brief Analyst Agent | Brief text → structured tags (Gemini) |
| 5 | Visual Analyst Agent | One image → visual analysis (Gemini vision) |
| 6 | Collective Analyst Agent | Multiple analyses → shared patterns |
| 7 | Creative Director Agent | Brief + patterns → creative direction |
| 8 | Board Generator Agent | Direction → initial canvas layout |
| 9 | Board storage | Save/load user-edited board layout |
| 10 | Export | Bundle project into downloadable JSON |
| 11 | Feedback | 👍/👎 on any AI output |

## Tech stack

**Backend:** Python, FastAPI, Supabase (Postgres + Auth + Storage),
Google Gemini (`gemini-2.5-flash`, multimodal).

**Frontend (planned):** Next.js, React, TypeScript, Tailwind CSS.

**Architecture:** every backend module is self-contained -
`schemas.py` (data contract) + `service.py` (logic) + `router.py`
(HTTP layer) - so any one module can be built, tested, and understood
in isolation, without the others running.

## Getting started

See `frontend/README.md` and `backend/README.md` for setup instructions
for each half of the project.

**Backend quick start:**
```
cd backend
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
pip install -r requirements.txt
cp .env.example .env           # then fill in real Supabase + Gemini keys
uvicorn app.main:app --reload
```
Visit `http://localhost:8000/docs` for interactive API docs.

**Testing note:** the Swagger `/docs` UI has proven unreliable with the
`authorization` header field specifically. For endpoints requiring a
Bearer token, use the Python test scripts in `backend/`
(`test_create_project.py`, `test_full_pipeline.py`) instead - these use
the `requests` library and work reliably.

## Build order (for reference / if extending)

Auth → Project → Brief Analyst Agent → Image Upload → Visual Analyst →
Collective Analyst → Creative Director → Board Generator → Board
storage → Export → Feedback → **[current point]** → Frontend → Deployment