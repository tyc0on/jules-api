## Jules API quick reference (scheduled tasks + sessions)

Use this when working with Jules scheduled tasks or sessions for a repo like `OWNER/REPO`.

- Base URL: `https://jules.googleapis.com/v1alpha`
- Auth: API key from `.env` (do not print it). Send header `x-goog-api-key: $JULES_API_KEY`
- Content type for JSON requests: `Content-Type: application/json`

### Find the repo source (required for sessions)
1) List sources:
   - `GET /v1alpha/sources`
2) Find the source whose GitHub repo matches `OWNER/REPO`.
3) Save the source resource name (format: `sources/{sourceId}`) for session queries.

### Find “scheduled tasks” (no explicit schedule endpoints in API docs)
The public API reference only documents Sessions, Activities, Sources, and Types. It does not list a dedicated schedules endpoint. Treat scheduled runs as sessions and locate them by source + title/prompt:
1) List sessions:
   - `GET /v1alpha/sessions?pageSize=50` (paginate with `pageToken` if needed)
2) Filter by `sourceContext.source == "sources/{sourceId}"`.
3) Look for recurring/scheduled runs by consistent `title` or `prompt` patterns.
4) If no matching sessions are found, confirm in the Jules UI and ask the user for a schedule identifier or URL; the schedule may not be exposed via the REST API.

### Update a scheduled task prompt (if only sessions are available)
When a scheduled task isn’t directly exposed, update by creating a new session with the corrected prompt (and confirm in UI for schedule edits). Use:
- `POST /v1alpha/sessions`
- Required fields: `prompt`, `sourceContext.source`, and `sourceContext.githubRepoContext.startingBranch`

Example (do not include the real key in logs):
```
curl -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources"
```

### Helper script (preferred for listing schedules)
Use the repo script at `jules-schedules/list_repo_schedules.py` to list sessions and group recurring prompts:
```
python jules-schedules/list_repo_schedules.py
```
Optional override:
```
JULES_REPO=OWNER/REPO \
python jules-schedules/list_repo_schedules.py
```

### Jules helper CLI (preferred for API work)
Helpers live in `jules-helpers/` and read `JULES_API_KEY` from `.env`.
```
python jules-helpers/list_sources.py
python jules-helpers/list_sessions.py
python jules-helpers/get_session.py <session_id>
python jules-helpers/delete_session.py <session_id>
python jules-helpers/list_activities.py <session_id>
python jules-helpers/get_activity.py <session_id> <activity_id>
python jules-helpers/create_session.py \
  --prompt "Fix the build" \
  --source sources/github/OWNER/REPO \
  --starting-branch main \
  --title "Fix build" \
  --require-plan-approval
python jules-helpers/send_message.py <session_id> \
  --message "Please focus on the failing tests only."
python jules-helpers/approve_plan.py <session_id>
python jules-helpers/list_schedules.py --repo OWNER/REPO
```
