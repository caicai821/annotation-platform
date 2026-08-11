from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    name: str
    type: str
    status: str
    created_at: datetime


class TaskCreate(BaseModel):
    dataset_id: int
    name: str = Field(min_length=1, max_length=128)
    type: str = Field(pattern="^(text|image)$")


class TaskUpdate(BaseModel):
    name: str | None = None
    status: str | None = Field(default=None, pattern="^(pending|in_progress|done)$")
