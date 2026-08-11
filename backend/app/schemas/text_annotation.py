"""文本标注 payload 结构（A + B 组所有，结构见 docs/api.md）。"""

from pydantic import BaseModel, Field, model_validator


class Entity(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    label: str

    @model_validator(mode="after")
    def check_range(self):
        if self.end <= self.start:
            raise ValueError("end 必须大于 start")
        return self


class TextPayload(BaseModel):
    labels: list[str]
    entities: list[Entity]
