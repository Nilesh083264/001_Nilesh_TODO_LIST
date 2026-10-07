from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel, Field


TodoStatus = Literal["pending", "completed", "cancelled"]


class Todo(BaseModel):
    id: str
    title: str = Field(min_length=1)
    description: str | None = None
    due_date: date | None = None
    due_time: time | None = None
    recurrence: str | None = None
    status: TodoStatus = "pending"
    created_at: datetime
    updated_at: datetime
