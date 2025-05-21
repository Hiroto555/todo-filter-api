from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from .models import StatusEnum


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending
    due_date: Optional[date] = None
    tags: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[date] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class TodoOut(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

