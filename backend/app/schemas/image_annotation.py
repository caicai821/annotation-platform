"""图像标注 payload 结构（C + D 组所有，结构见 docs/api.md）。"""

from pydantic import BaseModel, Field


class Box(BaseModel):
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    label: str
    confidence: float = Field(default=1.0, ge=0, le=1)


class ImagePayload(BaseModel):
    labels: list[str]
    boxes: list[Box]
