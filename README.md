# AuraFrame

An AI-powered creative workspace that turns scattered visual inspiration
and a plain-language brief into a structured creative direction and an
editable mood board.

## Structure

```
frontend/   Next.js app (the UI)
backend/    FastAPI app (the API + AI orchestration)
```

Each backend module under `backend/app/modules/` is self-contained:
input -> logic -> output, with no direct dependency on other modules.

## Getting started
See `frontend/README.md` and `backend/README.md` for setup instructions.

## Status
Skeleton stage - modules are scaffolded but not yet implemented.
Build order: Auth -> Project -> Brief Analyst Agent -> Image Upload ->
Visual Analyst -> Collective Analyst -> Creative Director -> Board
Generator -> Board storage/editing -> Export -> Feedback.
