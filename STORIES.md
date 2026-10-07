# TODO List Voice Note — Development Stories

## Epic 1 — Project Foundation

### STORY-001 — Create Repository Structure

**Goal**

Create the initial monorepo structure for backend and Android applications.

**Tasks**

- Create `backend/`
- Create `android/`
- Create `docs/`
- Create `data/`
- Create test structure
- Add `.gitignore`
- Add environment configuration
- Add README

**Acceptance Criteria**

- Backend starts successfully.
- Android project builds successfully.
- No secrets are committed.
- Repository structure follows `CLAUDE.md`.

---

### STORY-002 — FastAPI Application

**Goal**

Create the FastAPI application foundation.

**Tasks**

- Create FastAPI application.
- Add `/health`.
- Add application configuration.
- Add logging.
- Add CORS configuration for development.

**Acceptance Criteria**

```http
GET /health
```

returns:

```json
{
  "status": "ok"
}
```

---

# Epic 2 — TODO Domain

### STORY-003 — TODO Data Model

**Goal**

Create the canonical TODO domain model.

Fields:

```text
id
title
description
due_date
due_time
recurrence
status
created_at
updated_at
```

Statuses:

```text
pending
completed
cancelled
```

**Acceptance Criteria**

- Model uses Pydantic.
- Invalid data is rejected.
- Date/time types are explicit.
- Timezone handling is defined.

---

### STORY-004 — JSON Repository

**Goal**

Persist TODOs in JSON.

**Tasks**

- Create repository interface.
- Implement JSON repository.
- Implement read.
- Implement create.
- Implement update.
- Implement delete.
- Handle missing data file.
- Prevent data corruption during writes.

**Acceptance Criteria**

- Data survives backend restart.
- CRUD operations work.
- Invalid JSON is handled safely.
- Repository tests pass.

---

# Epic 3 — TODO API

### STORY-005 — Create TODO API

**Endpoint**

```http
POST /api/todos
```

**Acceptance Criteria**

A valid request creates a TODO and returns its ID.

Invalid requests return appropriate HTTP errors.

---

### STORY-006 — List TODOs

**Endpoint**

```http
GET /api/todos
```

Support basic filtering:

```text
status
date
```

---

### STORY-007 — Update TODO

**Endpoint**

```http
PATCH /api/todos/{todo_id}
```

Support updating:

- title
- description
- date
- time
- recurrence
- status

---

### STORY-008 — Delete TODO

**Endpoint**

```http
DELETE /api/todos/{todo_id}
```

Return an appropriate response when the TODO does not exist.

---

# Epic 4 — Gemini Integration

### STORY-009 — Gemini Client

**Goal**

Create an isolated Gemini integration.

**Requirements**

- API key from environment.
- Configurable model.
- Timeout handling.
- Retry policy.
- Structured response handling.
- Error logging without secrets.

---

### STORY-010 — Natural Language Command Schema

Create a strict AI output model.

Example:

```json
{
  "intent": "create_reminder",
  "title": "Call Rahul",
  "description": null,
  "due_date": "2026-10-08",
  "due_time": "10:00:00",
  "recurrence": null
}
```

Supported intents:

```text
create_todo
create_reminder
list_todos
complete_todo
delete_todo
update_todo
unknown
```

---

### STORY-011 — Command Interpretation

**Endpoint**

```http
POST /api/commands
```

Request:

```json
{
  "text": "Remind me to call Rahul tomorrow at 10 AM"
}
```

Expected behavior:

```text
text
 ↓
Gemini
 ↓
validated ParsedCommand
 ↓
TodoService
 ↓
JSON repository
```

**Acceptance Criteria**

- Natural-language input is parsed.
- Gemini output is validated.
- Invalid AI output does not create a TODO.
- Date/time uses `Asia/Kolkata`.
- Missing required information is detected.

---

# Epic 5 — Android Foundation

### STORY-012 — Android Application

Create the native Android application.

Requirements:

- Application launches.
- Basic UI exists.
- Permissions are declared correctly.
- Backend base URL is configurable.

---

### STORY-013 — Android API Client

Create the Android networking layer.

Responsibilities:

- Send voice commands.
- Retrieve TODOs.
- Create TODOs.
- Update TODOs.
- Delete TODOs.

API failures must be handled gracefully.

---

# Epic 6 — Reminder Engine

### STORY-014 — Local Reminder Scheduler

**Goal**

Schedule reminders on the Android device.

Input:

```text
TODO
+
due_date
+
due_time
```

Output:

```text
scheduled Android alarm
```

**Critical Requirement**

Once a reminder has been scheduled, it must not depend on Gemini or FastAPI being available at reminder time.

---

### STORY-015 — Notification

Create reminder notifications.

Notification must contain:

- TODO title
- Reminder time
- Optional description
- Open application action
- Complete action where supported

---

### STORY-016 — Reminder Persistence

Persist enough scheduling information locally so scheduled reminders can be restored after application/device restart.

---

# Epic 7 — Voice

### STORY-017 — Speech-to-Text

Implement voice command capture.

State machine:

```text
IDLE
 ↓
LISTENING
 ↓
COMMAND_CAPTURE
 ↓
PROCESSING
 ↓
SUCCESS / ERROR
 ↓
IDLE
```

---

### STORY-018 — Wake Word

Implement wake-word detection for:

> "Hey Vivo"

The wake-word engine should minimize:

- False positives
- Battery consumption
- Network dependency

Wake-word detection should preferably be local.

---

### STORY-019 — Voice Command Pipeline

Integrate:

```text
Wake Word
    ↓
Speech Capture
    ↓
STT
    ↓
FastAPI
    ↓
Gemini
    ↓
TODO
```

---

# Epic 8 — Background Execution

### STORY-020 — Foreground Voice Service

Implement Android foreground service for voice functionality where required by the target Android version.

Requirements:

- Correct foreground-service declaration.
- Correct notification.
- Microphone permission handling.
- Start/stop controls.
- Failure recovery.

---

### STORY-021 — Boot Startup

Start the required service after device reboot.

Use Android's supported boot mechanisms.

Acceptance criteria:

- Reboot device.
- Android starts.
- Application restores required background functionality.
- User can verify service state.

---

### STORY-022 — Battery Optimization Handling

Detect when battery optimization may prevent reliable background execution.

Provide user guidance rather than attempting unauthorized bypasses.

---

# Epic 9 — Voice TODO Operations

### STORY-023 — Voice Create TODO

Support:

> "Hey Vivo, add buy groceries to my TODO."

Expected:

```text
intent = create_todo
title = Buy groceries
```

---

### STORY-024 — Voice Reminder

Support:

> "Hey Vivo, remind me to call Rahul tomorrow at 10 AM."

---

### STORY-025 — Voice List

Support:

> "Hey Vivo, what are my tasks today?"

---

### STORY-026 — Voice Complete

Support:

> "Hey Vivo, mark call Rahul as complete."

---

### STORY-027 — Voice Delete

Support:

> "Hey Vivo, delete the grocery reminder."

---

### STORY-028 — Voice Update

Support:

> "Hey Vivo, move my Rahul reminder to 5 PM."

---

# Epic 10 — Recurrence

### STORY-029 — Daily Recurrence

Example:

> "Remind me every day at 9 AM to check the server."

---

### STORY-030 — Weekly Recurrence

Example:

> "Remind me every Monday at 9 AM."

---

### STORY-031 — Weekday Recurrence

Example:

> "Remind me every weekday at 8 AM."

---

### STORY-032 — Monthly Recurrence

Example:

> "Remind me on the 15th of every month."

---

# Epic 11 — Reliability

### STORY-033 — Backend Failure

If FastAPI is unavailable:

- Do not crash voice service.
- Show/announce failure.
- Retry where appropriate.
- Do not silently lose the command.

---

### STORY-034 — Gemini Failure

If Gemini is unavailable:

- Do not create a potentially incorrect TODO.
- Return controlled error.
- Allow retry.

---

### STORY-035 — Invalid AI Response

If Gemini returns invalid structured data:

```text
Gemini
 ↓
Validation failure
 ↓
Reject
 ↓
Retry / clarification
```

Never persist invalid AI output.

---

### STORY-036 — Duplicate Command Protection

Prevent accidental duplicate TODO creation caused by:

- Speech recognition retry.
- Network retry.
- User repeating command.
- Backend request retry.

Use request IDs/idempotency where appropriate.

---

# Epic 12 — Testing

### STORY-037 — Backend Unit Tests

Cover:

- Models
- Repository
- Services
- Gemini parser
- Date/time
- Recurrence

---

### STORY-038 — API Integration Tests

Test:

```text
POST /api/todos
GET /api/todos
PATCH /api/todos/{id}
DELETE /api/todos/{id}
POST /api/commands
```

---

### STORY-039 — Android Tests

Test:

- API client
- Voice state machine
- Scheduler
- Notification
- Boot receiver

---

### STORY-040 — End-to-End Test

Test:

```text
"Hey Vivo"
      ↓
voice capture
      ↓
STT
      ↓
FastAPI
      ↓
Gemini
      ↓
TODO
      ↓
Android scheduler
      ↓
notification
```

---

# Definition of Done

A story is DONE only when:

- Code is implemented.
- Relevant tests pass.
- Error cases are handled.
- Existing functionality is not broken.
- API/data contracts are documented.
- No credentials are exposed.
- The implementation follows `CLAUDE.md`.

---

# MVP Completion Criteria

The MVP is complete when the following scenario works:

> User says: "Hey Vivo, remind me to call Rahul tomorrow at 10 AM."

System behavior:

```text
1. Wake word detected
2. Voice command captured
3. Speech converted to text
4. Command sent to FastAPI
5. Gemini extracts intent/date/time
6. Backend validates result
7. TODO stored
8. Android receives reminder
9. Android schedules local alarm
10. Device displays notification at 10 AM
```

The reminder must remain functional even if FastAPI/Gemini is unavailable after scheduling.