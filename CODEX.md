# TODO List Voice Note — Claude Development Guide

## 1. Project Overview

**Project Name:** TODO List Voice Note

TODO List Voice Note is an Android voice-first TODO and reminder application.

The user should be able to say:

> "Hey Vivo, remind me to call Rahul tomorrow at 10 AM."

The system must detect the wake word, capture the voice command, understand the user's intent, create a structured TODO/reminder, persist it, and schedule a notification.

The application is intended to operate continuously in the background and automatically restart after device reboot.

---

# 2. Primary Architecture

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │ Android Client│
              │               │
              │ Wake Word     │
              │ STT           │
              │ Background    │
              │ Scheduler     │
              │ Notification  │
              └───────┬───────┘
                      │ HTTP
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              │    Backend    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Gemini AI   │
              │               │
              │ Intent        │
              │ Extraction    │
              │ Date/Time     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ JSON Storage  │
              │     MVP       │
              └───────────────┘
```

## 3. Architectural Ownership

### Android owns

- Wake-word detection
- Microphone interaction
- Speech-to-text integration
- Background execution
- Boot-time startup
- Local reminder scheduling
- Notifications
- Local task state required for reminder execution
- User-facing UI

### FastAPI owns

- API endpoints
- Request validation
- TODO business logic
- Gemini integration
- Structured command processing
- TODO persistence for the MVP
- Backend-side validation
- Error handling

### Gemini owns

Gemini is an interpretation layer, not the application's source of truth.

Gemini may perform:

- Intent detection
- Natural-language understanding
- Entity extraction
- Date/time interpretation
- Recurrence interpretation
- Command classification
- Natural-language response generation where required

Gemini must NOT directly control:

- Android services
- Reminder scheduling
- Database/storage writes
- Application lifecycle
- Device commands

The backend must validate Gemini's output before using it.

---

# 4. Technology Stack

## Backend

- Python 3.11+
- FastAPI
- Pydantic v2
- Gemini API
- JSON storage for MVP
- pytest
- httpx

## Android

Use native Android development.

Preferred:

- Kotlin
- Android SDK
- Foreground Service where required
- BroadcastReceiver for boot handling
- Android notification APIs
- AlarmManager / appropriate Android scheduling API
- Android SpeechRecognizer or selected STT implementation
- Local persistence where necessary

Do not assume unrestricted background execution.

Android versions impose background execution and microphone restrictions. The implementation must follow the target Android version's rules.

---

# 5. Core Functional Flow

```text
Device powered on
        │
        ▼
Android application starts
        │
        ▼
Background voice service starts
        │
        ▼
Wait for wake word
        │
        ▼
"Hey Vivo"
        │
        ▼
Capture command
        │
        ▼
Speech → Text
        │
        ▼
POST /api/commands
        │
        ▼
FastAPI
        │
        ▼
Gemini
        │
        ▼
Structured command
        │
        ▼
Validate
        │
        ▼
Create TODO
        │
        ▼
Persist
        │
        ▼
Schedule Android reminder
        │
        ▼
Notification
```

---

# 6. API Design Principles

All API contracts must use explicit Pydantic models.

Do not pass unstructured dictionaries between layers when a typed model can be used.

Example:

```python
class VoiceCommandRequest(BaseModel):
    text: str
    source: str = "voice"
```

Gemini output should also have a strict schema.

Example:

```python
class ParsedCommand(BaseModel):
    intent: Literal[
        "create_todo",
        "create_reminder",
        "list_todos",
        "complete_todo",
        "delete_todo",
        "update_todo",
        "unknown"
    ]

    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    due_time: time | None = None
    recurrence: str | None = None
```

Never trust AI output directly.

---

# 7. Date and Time Rules

Date/time interpretation must use an explicit timezone.

The default deployment timezone for the MVP is:

```text
Asia/Kolkata
```

Relative expressions must be resolved consistently:

- today
- tomorrow
- tonight
- this evening
- next Monday
- next week
- every Monday
- every day
- weekdays

The backend must never silently interpret an ambiguous date/time incorrectly.

If required information is missing, the application should request clarification.

Example:

> "Remind me to call Rahul."

Possible response:

> "What time should I remind you?"

---

# 8. Storage

MVP storage is JSON.

Recommended structure:

```text
data/
├── todos.json
└── settings.json
```

Example:

```json
{
  "todos": [
    {
      "id": "todo_001",
      "title": "Call Rahul",
      "description": null,
      "due_date": "2026-10-08",
      "due_time": "10:00:00",
      "recurrence": null,
      "status": "pending",
      "created_at": "2026-10-07T22:30:00+05:30",
      "updated_at": "2026-10-07T22:30:00+05:30"
    }
  ]
}
```

Storage access must be isolated behind a repository/service interface.

Do not scatter direct JSON file operations throughout the application.

---

# 9. Backend Project Structure

Preferred structure:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── commands.py
│   │   │   ├── todos.py
│   │   │   └── health.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   │   ├── command.py
│   │   └── todo.py
│   │
│   ├── services/
│   │   ├── command_service.py
│   │   ├── todo_service.py
│   │   ├── reminder_service.py
│   │   └── ai_service.py
│   │
│   ├── repositories/
│   │   └── todo_repository.py
│   │
│   └── integrations/
│       └── gemini.py
│
├── data/
├── tests/
├── requirements.txt
└── README.md
```

Keep responsibilities separated.

---

# 10. Android Architecture

Preferred high-level structure:

```text
android/
└── app/
    └── src/main/
        ├── java/.../
        │   ├── ui/
        │   ├── service/
        │   ├── voice/
        │   ├── network/
        │   ├── repository/
        │   ├── scheduler/
        │   ├── notification/
        │   └── receiver/
        │
        └── AndroidManifest.xml
```

Important components:

```text
VoiceService
    ↓
WakeWordDetector
    ↓
SpeechRecognizer
    ↓
ApiClient
    ↓
ReminderScheduler
    ↓
NotificationManager
```

---

# 11. Background Execution

The phrase "24x7" means the application should be designed for persistent operation, but Android does not guarantee unrestricted background execution.

Implementation must account for:

- Foreground service requirements
- Microphone foreground-service restrictions
- Battery optimization
- Doze mode
- App standby
- OEM background restrictions
- Boot receiver restrictions
- Notification permission
- Microphone permission

Do not claim that an Android application can bypass every OS restriction.

If a feature requires ADB, root, device-owner mode, or special OEM configuration, explicitly document that requirement.

---

# 12. ADB / Shell Capabilities

ADB shell commands are development/deployment capabilities, not the default application architecture.

Use official Android APIs whenever possible.

ADB may be used for:

- Installing the APK
- Granting development permissions where permitted
- Debugging
- Starting/stopping services during development
- Inspecting logs
- Testing boot behavior
- Device configuration

Never design the production application around unauthorized privilege escalation.

---

# 13. Security

Never hard-code:

- Gemini API keys
- API tokens
- passwords
- private credentials
- signing keys

Use environment/configuration mechanisms.

Example:

```text
GEMINI_API_KEY=
```

Never commit secrets to Git.

The backend must validate all client input.

---

# 14. Error Handling

Every external dependency must have explicit failure handling.

Examples:

```text
Speech recognition failed
        ↓
Retry / user feedback

FastAPI unavailable
        ↓
Queue locally or show failure

Gemini unavailable
        ↓
Retry / fallback / request later

Invalid Gemini response
        ↓
Reject response and retry

Reminder scheduling failed
        ↓
Persist task + report scheduling failure
```

Do not silently discard user commands.

---

# 15. Logging

Use structured application logging.

Logs should help diagnose:

- Wake-word detection
- Speech recognition
- API requests
- Gemini requests
- Gemini parsing
- TODO creation
- Scheduling
- Notification
- Service startup
- Boot startup
- Errors

Never log:

- API keys
- authentication tokens
- sensitive voice content unnecessarily

---

# 16. Testing Requirements

Every feature must have tests.

Backend tests:

- Pydantic validation
- Gemini response validation
- Command parsing
- TODO creation
- TODO update
- TODO deletion
- Recurrence parsing
- Date/time handling
- Repository behavior
- API endpoints

Android tests:

- Wake-word state machine
- Voice state transitions
- API request handling
- Reminder scheduling
- Notification behavior
- Boot startup
- Failure/retry behavior

---

# 17. Development Rules

1. Do not implement multiple unrelated features simultaneously.
2. Implement one story at a time.
3. Write tests with every backend feature.
4. Keep API contracts explicit.
5. Keep AI interpretation isolated.
6. Never trust AI output without validation.
7. Keep Android scheduling independent from Gemini.
8. Avoid premature database migration.
9. Do not introduce Redis, PostgreSQL, Kafka, or other infrastructure unless a requirement actually demands it.
10. Prefer simple, maintainable code over unnecessary abstraction.
11. Do not modify architecture without documenting the reason.
12. Do not claim a feature works without testing it.
13. Do not fabricate Android permissions or APIs.
14. Check Android-version-specific restrictions before implementing background behavior.
15. Keep the MVP operational before adding advanced functionality.

---

# 18. Definition of Done

A story is complete only when:

- Implementation exists.
- Tests exist where applicable.
- Error handling exists.
- API contracts are documented.
- No obvious security issue exists.
- The feature works with the existing architecture.
- Existing tests still pass.
- README/documentation is updated when necessary.

---

# 19. Development Priority

Implement in this order:

```text
1. Repository structure
2. TODO data model
3. JSON repository
4. TODO CRUD API
5. Gemini integration
6. Voice command parsing
7. Android project
8. Android ↔ FastAPI communication
9. Reminder scheduling
10. Notification
11. Wake-word detection
12. Background service
13. Boot auto-start
14. Recurring reminders
15. Advanced voice commands
```

Do not start with wake-word detection.

Build the deterministic backend first so the AI/voice layer has a stable API to communicate with.