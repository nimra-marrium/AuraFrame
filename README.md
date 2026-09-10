<div align="center">

# AuraFrame

**An AI-powered creative workspace that transforms unstructured visual inspiration into structured creative direction and editable mood boards.**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-3.5--flash--lite-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Overview

Creative professionals start projects with scattered inspiration — Pinterest boards, screenshots, half-written notes, competitor references. AuraFrame turns that fragmented input into a structured creative system: a written brief goes in, a computer-vision + multimodal-LLM pipeline analyzes it alongside any reference images, and the output is a complete creative direction — palette, typography, imagery guidance — rendered onto an editable mood board.

This is not a chatbot wrapper. It's a multi-agent orchestration pipeline with independently testable stages, backed by a relational database with row-level security, and a real file-storage layer.

## Architecture

```
User Brief ──┐
             ├──▶ Brief Analyst Agent ───┐
Reference    │                          │
Images ──────┼──▶ Visual Analyst Agent ─┼──▶ Collective Analyst Agent
             │    (per image)           │    (cross-image patterns)
             │                          │
             └──────────────────────────┼──▶ Creative Director Agent
                                         │    (direction + palette + type)
                                         │
                                         └──▶ Board Generator Agent
                                              (canvas layout JSON)
                                                    │
                                                    ▼
                                          User-editable Mood Board
                                                    │
                                          Feedback Loop (👍/👎 per output)
```

Five independent AI agents, each a pure function — JSON in, JSON out — chained through a controlled pipeline rather than a single opaque prompt. Every agent is testable in isolation with hand-written mock input, with no dependency on the database or any other agent running.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL (Supabase), Row Level Security |
| Auth | Supabase Auth (JWT-based) |
| File storage | Supabase Storage |
| AI / LLM | Google Gemini 3.5 Flash Lite (multimodal — text + vision) |
| Frontend | Next.js, React, TypeScript, Tailwind CSS *(in progress)* |

## Backend module map

| Module | Responsibility |
|---|---|
| Auth | Signup / login via Supabase Auth, JWT session handling |
| Project | Create/read a project and its creative brief |
| Image Upload | Multipart file upload → Supabase Storage + DB pointer |
| Brief Analyst Agent | Brief text → structured objective/audience/tone/keywords |
| Visual Analyst Agent | Single image → colors, style, objects, composition, lighting |
| Collective Analyst Agent | N images → recurring patterns, outliers, overall mood |
| Creative Director Agent | Brief + visual patterns → palette, typography, direction |
| Board Generator Agent | Direction → canvas layout (x/y/w/h element positions) |
| Board Storage | Persist/update user-edited board layout |
| Export | Bundle project into a downloadable file |
| Feedback | Capture 👍/👎 per AI output for evaluation |

Full detail — preconditions, postconditions, security patterns — in [`backend-modules-reference.md`](./backend-modules-reference.md).

## Security model

Every user-owned resource is protected by PostgreSQL Row Level Security, not just application-level checks. Requests carry the caller's Supabase JWT; policies verify ownership at the database layer — including relationship-based checks (e.g. a board's ownership is verified through its parent project's `user_id`, since `boards` has no direct `user_id` column of its own).

```sql
create policy "Users can insert boards for their own projects"
on boards for insert
with check (
  exists (
    select 1 from projects
    where projects.id = boards.project_id
    and projects.user_id = auth.uid()
  )
);
```

## Status

- ✅ Backend — 11/11 modules complete, tested end-to-end
- ⬜ Frontend — in progress
- ⬜ Deployment

## Getting started

See [`backend/README.md`](./backend/README.md) for backend setup (macOS/Linux + Windows instructions included).

## Roadmap

- [ ] Frontend: creative brief intake, image upload UI, AI analysis panels
- [ ] Interactive mood board canvas
- [ ] Image embeddings for visual similarity search (pgvector)
- [ ] Background job queue for AI agent calls (async, non-blocking)
- [ ] Deployment (Vercel + Render)

---

<div align="center">
<sub>Built as a portfolio project demonstrating full-stack AI product engineering: multi-agent orchestration, multimodal AI integration, relational database security, and product-oriented system design.</sub>
</div>