# Jules helpers

Small CLI helpers for the Jules REST API. They read `JULES_API_KEY` from `.env` in the repo root.

## Quick usage

List sources:
```
python /home/USER/jules/jules-helpers/list_sources.py
```

List sessions:
```
python /home/USER/jules/jules-helpers/list_sessions.py
```

Get a session:
```
python /home/USER/jules/jules-helpers/get_session.py <session_id>
```

Delete a session:
```
python /home/USER/jules/jules-helpers/delete_session.py <session_id>
```

List activities for a session:
```
python /home/USER/jules/jules-helpers/list_activities.py <session_id>
```

Get an activity:
```
python /home/USER/jules/jules-helpers/get_activity.py <session_id> <activity_id>
```

Create a session:
```
python /home/USER/jules/jules-helpers/create_session.py \
  --prompt "Fix the build" \
  --source sources/github/OWNER/REPO \
  --starting-branch main \
  --title "Fix build" \
  --require-plan-approval
```

Send a message to a session:
```
python /home/USER/jules/jules-helpers/send_message.py <session_id> \
  --message "Please focus on the failing tests only."
```

Approve a plan:
```
python /home/USER/jules/jules-helpers/approve_plan.py <session_id>
```

List recurring sessions (approx schedules):
```
python /home/USER/jules/jules-helpers/list_schedules.py --repo OWNER/REPO
```
