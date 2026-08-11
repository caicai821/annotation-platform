from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnnotationSave(BaseModel):
    """统一标注保存接口的请求体。

    type 决定使用哪组的 payload 结构（见 text_annotation / image_annotation schema）。
    """

    type: str = Field(pattern="^(text|image)$")
    payload: dict


class AnnotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    item_id: int
    annotator_id: int
    type: str
    payload: dict
    status: str
    updated_at: datetime
