from datetime import date, time
from typing import Literal

from pydantic import BaseModel, Field


CommandIntent = Literal[
    "create_todo",
    "create_reminder",
    "list_todos",
    "complete_todo",
    "delete_todo",
    "update_todo",
    "unknown",
]


class VoiceCommandRequest(BaseModel):
    text: str = Field(min_length=1)
    source: str = "voice"


class ParsedCommand(BaseModel):
    intent: CommandIntent
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    due_time: time | None = None
    recurrence: str | None = None
