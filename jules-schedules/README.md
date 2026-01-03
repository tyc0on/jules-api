# Jules schedule listing helper

This helper groups Jules sessions by title+prompt to approximate recurring scheduled tasks for a repo.

## Setup

- Ensure `.env` in the project root has `JULES_API_KEY`.
- Optional: set `JULES_REPO` to override the default `OWNER/REPO`.

## Run

```
python jules-schedules/list_repo_schedules.py
```

## Output

The script prints:
- the source resource name
- total sessions for the repo
- grouped entries (count, latest create time, title, prompt prefix)

It does not print or log the API key.
