from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    description: str | None = None
    created_at: datetime


class DatasetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    type: str = Field(pattern="^(text|image)$")
    description: str | None = None


class DataItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    content: str
    meta: dict | None = None
    created_at: datetime


class DataItemCreate(BaseModel):
    content: str
    meta: dict | None = None
