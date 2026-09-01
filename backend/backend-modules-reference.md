# AuraFrame Backend — Complete Module Reference

This document explains what every module does, its exact contract (input/output,
precondition/postcondition), which files matter, and how its security works.
Written as a "look here to remember what's happening" reference.

---

## How every module is structured (the pattern, once, so it's not repeated 11 times)

```
backend/app/modules/<module_name>/
├── __init__.py     empty - just marks this folder as a Python module
├── schemas.py      the data contract - what shape goes in, what shape comes out
├── service.py      the actual logic - pure-ish functions, DB/AI calls happen here
└── router.py       the HTTP layer - thin, translates HTTP <-> service.py
```

**Why split this way:** `schemas.py` can be imported by other modules without
pulling in any logic. `service.py` can be tested by calling its functions
directly, with no HTTP server running at all. `router.py` only exists to
translate an HTTP request into a function call and a function result back
into an HTTP response - it should never contain real logic itself.

**Two authentication patterns used across modules:**
- **RLS + user token** (`auth`, `project`, `boards`, `feedback`, `export`) -
  the router extracts the caller's `access_token` from the `Authorization:
  Bearer <token>` header, hands it to Supabase via
  `supabase.postgrest.auth(access_token)`, and Supabase's Row Level
  Security policies enforce "you can only touch your own data" at the
  database level.
- **No auth check in code** (`image`, all 5 AI agents) - these either use
  looser RLS policies (`with check (true)`) or are stateless pure
  functions with no ownership concept at all (the AI agents don't touch
  the database directly).

---

## Module 1 — Auth
**Files:** `backend/app/modules/auth/{schemas,service,router}.py`

**Responsibility:** sign up, log in, identify the requesting user via
Supabase Auth (email + password).

**Precondition:** email is valid format; password is 8+ characters
(enforced by Pydantic in `schemas.py` before `service.py` ever runs).

**Postcondition:** on signup, a user row exists in Supabase's internal
`auth.users` table; on login, caller receives a valid `access_token`
(a JWT) they can use as proof of identity on every other protected
endpoint.

**Endpoints:**
- `POST /auth/signup` → `{email, password}` → `{user_id, email, access_token}`
- `POST /auth/login` → `{email, password}` → `{user_id, email, access_token}`

**Key detail:** `service.py` wraps the Supabase call in `try/except`
because Supabase raises its own exception (`AuthApiError`) on failure
rather than returning `None` - if this isn't caught, it crashes as an
unhandled `500` instead of a clean `400`. (This was a real bug we fixed
mid-project.)

**Note:** email confirmation is currently OFF (toggled in Supabase →
Authentication → Providers → Email) so signup returns a working token
immediately, for faster testing. Turn this back ON before real deployment.

---

## Module 2 — Project
**Files:** `backend/app/modules/project/{schemas,service,router}.py`

**Responsibility:** create/read a project and its creative brief - the
first real "unit of work" a user creates.

**Precondition:** a valid, real `user_id` (from Auth) exists.

**Postcondition:** a row exists in the `projects` table, `status: draft`.

**Endpoints:**
- `POST /projects/` → `{user_id, name, brief_text, project_type?,
  target_audience?, desired_mood?}` → full `Project` record with `id`
- `GET /projects/{project_id}` → single project
- `GET /projects/user/{user_id}` → list of that user's projects

**Security - RLS pattern (the "real" one):**
```sql
create policy "Users can insert their own projects"
on projects for insert
with check (auth.uid() = user_id);
```
Router requires `Authorization: Bearer <token>` header; calls
`supabase.postgrest.auth(access_token)` before the DB call so Postgres
knows *who* is asking, and the policy checks that `auth.uid()` (the
token's identity) matches the `user_id` in the row being written.

---

## Module 3 — Image Upload
**Files:** `backend/app/modules/image/{schemas,service,router}.py`

**Responsibility:** accept an actual image file, store the bytes in
Supabase Storage, save a pointer (URL) + metadata in the `images` table.

**Precondition:** valid `project_id`; file is jpeg/png/webp/gif; under 8MB.

**Postcondition:** file exists in the `images` Storage bucket; a row
exists in the `images` table with `analysis: null` (not yet AI-analyzed).

**Endpoint:**
- `POST /images/` → multipart form (`project_id` + `file`) → `{id,
  project_id, url, analysis, created_at}`

**Key detail - different from every other module:** this one accepts
`multipart/form-data`, not JSON, because browsers can't send raw files
as JSON. `router.py` uses FastAPI's `UploadFile` + `Form(...)` instead
of a Pydantic body schema.

**Security:** looser than Project - storage bucket and `images` table
both use `with check (true)` policies (anyone can upload/read), not
scoped per-user. Acceptable simplification for an MVP; a "harden later"
item if you want to lock it down to project owners specifically.

---

## Module 4 — Brief Analyst Agent
**Files:** `backend/app/modules/brief_analyst/{schemas,service,router}.py`

**Responsibility:** turn raw brief text into structured creative tags
using Gemini.

**Precondition:** `brief_text` is non-empty.

**Postcondition:** none (pure function - no DB write happens here).

**Endpoint:**
- `POST /agents/brief/` → `{brief_text}` → `{objective, audience, tone[],
  keywords[], constraints[]}`

**How it works:** builds a prompt instructing Gemini to return ONLY raw
JSON matching the output shape, calls `gemini-2.5-flash`, strips any
accidental ```` ```json ```` fences from the response, parses it, and
validates it against `BriefAnalystOutput`.

---

## Module 5 — Visual Analyst Agent
**Files:** `backend/app/modules/visual_analyst/{schemas,service,router}.py`

**Responsibility:** analyze ONE image (colors, style, objects,
composition, lighting) using Gemini's multimodal (vision) capability.

**Precondition:** `image_url` is a reachable, real image.

**Postcondition:** none (pure function).

**Endpoint:**
- `POST /agents/visual/` → `{image_url}` → `{colors[], style, objects[],
  composition, lighting, keywords[]}`

**How it works:** fetches the image bytes itself via `httpx`, sends them
to Gemini as a `types.Part.from_bytes(...)` alongside the analysis
prompt. This is the one agent that actually "sees" an image, not just
text.

---

## Module 6 — Collective Analyst Agent
**Files:** `backend/app/modules/collective_analyst/{schemas,service,router}.py`

**Responsibility:** find recurring patterns ACROSS multiple Visual
Analyst outputs - the "your references consistently use..." feature.

**Precondition:** at least 2 analyses in the input array.

**Postcondition:** none (pure function).

**Endpoint:**
- `POST /agents/collective/` → `{analyses: [VisualAnalystOutput, ...]}`
  → `{recurring_colors[], recurring_motifs[], common_aesthetic,
  outliers[], overall_mood}`

**Notable dependency:** `schemas.py` imports `VisualAnalystOutput` from
Module 5 - this is the one deliberate exception to "modules don't touch
each other," since this agent's whole job is to consume Module 5's
output shape.

---

## Module 7 — Creative Director Agent
**Files:** `backend/app/modules/creative_director/{schemas,service,router}.py`

**Responsibility:** combine the Brief Analyst's output + the Collective
Analyst's output into one cohesive creative direction (palette,
typography, imagery direction, things to avoid).

**Precondition:** both inputs non-null, matching expected shapes.

**Postcondition:** none (pure function).

**Endpoint:**
- `POST /agents/direction/` → `{brief_analysis: BriefAnalystOutput,
  collective_analysis: CollectiveAnalystOutput}` → `{direction_name,
  palette[], typography{heading,body}, imagery_direction, avoid[]}`

**Notable dependency:** imports output shapes from both Module 4 and
Module 6, same pattern as above.

---

## Module 8 — Board Generator Agent
**Files:** `backend/app/modules/board_generator/{schemas,service,router}.py`

**Responsibility:** propose an initial canvas layout (x/y/w/h positions)
mixing image tiles, color swatches, and text, based on the Creative
Direction.

**Precondition:** direction JSON valid; at least 1 image id provided.

**Postcondition:** none (pure function).

**Endpoint:**
- `POST /agents/board/` → `{direction: CreativeDirectorOutput,
  image_ids: [string]}` → `{elements: [{type, ref/color/content, x, y,
  w, h}, ...]}`

**This is the last of the 5 AI agents** - after this, the pipeline output
matches exactly what Module 9 (Board storage) expects as input.

---

## Module 9 — Board storage
**Files:** `backend/app/modules/boards/{schemas,service,router}.py`

**Responsibility:** persist and update the board layout as the user
edits it on the canvas. One board per project (upsert logic: creates on
first save, updates after that).

**Precondition:** valid `project_id`; layout JSON well-formed.

**Postcondition:** `boards.layout_data` saved/updated in DB.

**Endpoints:**
- `PUT /boards/{project_id}` → `{elements: [...]}` → saved `Board` record
- `GET /boards/{project_id}` → current board

**Security - RLS via relationship (more advanced than Project's pattern):**
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
`boards` has no `user_id` column of its own - ownership is checked
*through* the parent `projects` row via a subquery. Same
`Authorization: Bearer <token>` pattern as Project.

---

## Module 10 — Export
**Files:** `backend/app/modules/export/{service,router}.py` (no
`schemas.py` - it's read-only, no user input to validate)

**Responsibility:** bundle a project's brief, images, and board layout
into a downloadable JSON file.

**Precondition:** the project exists.

**Postcondition:** none (read-only).

**Endpoint:**
- `GET /export/{project_id}` → downloadable `.json` file (sets
  `Content-Disposition: attachment` so the browser triggers a download
  instead of just displaying JSON)

**Note:** this is a JSON export, not a rendered image/PDF - real
image/PDF rendering would need an extra library (e.g. Pillow) and is a
good future upgrade, not a blocker.

**Security:** same `Bearer` pattern as Board/Project, since it reads
from `boards` (which requires the ownership check).

---

## Module 11 — Feedback
**Files:** `backend/app/modules/feedback/{schemas,service,router}.py`

**Responsibility:** capture 👍/👎 on any AI output (palette, direction,
board, etc.) for a project - the AI Evaluation feature from the original
spec.

**Precondition:** valid `project_id`; `rating` is `"up"` or `"down"`.

**Postcondition:** row saved in `feedback` table.

**Endpoints:**
- `POST /feedback/` → `{project_id, output_type, rating, comment?}` →
  saved `Feedback` record
- `GET /feedback/project/{project_id}` → list of feedback for a project

**Security:** same relationship-based RLS pattern as Board (checks
ownership through the parent `projects` row).

---

## Known quirks / things to remember

- **Swagger's `/docs` UI is unreliable with the `authorization` header
  field specifically** - it visually shows filled but sometimes doesn't
  actually send it (confirmed via the generated curl command missing
  `-H authorization`). When testing endpoints that need a Bearer token,
  prefer the Python test scripts (`test_create_project.py`,
  `test_full_pipeline.py` in `backend/`) over the Swagger UI.
- **PowerShell's `curl` is NOT real curl** - it's an alias for
  `Invoke-WebRequest` with different syntax. Use `curl.exe` to force real
  curl, or better, use the Python `requests`-based scripts.
- **RLS (Row Level Security)** blocks ALL access by default the moment
  it's enabled on a table - you must explicitly write policies for every
  operation (insert/select/update) or everything gets rejected, even
  from the legitimate owner.
- **Storage bucket RLS is separate from table RLS** - uploading a file
  successfully to Storage doesn't mean the matching database row insert
  will succeed; both have their own independent policies.
- **`service_role` key bypasses RLS entirely** - useful for backend-only
  trusted operations or as a temporary workaround, but loses the
  per-user security guarantee. Currently `database.py` uses the `anon`
  key + per-request `Bearer` token swap, which is the more correct
  pattern.