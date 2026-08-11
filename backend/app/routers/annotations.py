"""统一标注接口 [约定]，负责人维护。

文本组与图像组共用本路由，payload 结构校验分别委托给
schemas/text_annotation.py（A+B）与 schemas/image_annotation.py（C+D）。
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Annotation, DataItem, Task, User
from ..response import ok
from ..schemas import AnnotationOut, AnnotationSave
from ..schemas.image_annotation import ImagePayload
from ..schemas.text_annotation import TextPayload
from ..security import get_current_user

router = APIRouter(tags=["annotation"])

_PAYLOAD_SCHEMAS = {
    "text": TextPayload,
    "image": ImagePayload,
}


def _get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "任务不存在"})
    return task


def _validate_payload(annotation_type: str, payload: dict) -> dict:
    schema = _PAYLOAD_SCHEMAS.get(annotation_type)
    if schema is None:
        raise HTTPException(status_code=400, detail={"code": 40001, "message": "未知标注类型"})
    try:
        return schema.model_validate(payload).model_dump()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={"code": 40001, "message": f"payload 结构不符合 {annotation_type} 标注规范: {exc}"},
        )


@router.get("/tasks/{task_id}/items/{item_id}/annotation")
def get_annotation(
    task_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _get_task_or_404(db, task_id)
    if db.get(DataItem, item_id) is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "数据条目不存在"})
    annotation = (
        db.query(Annotation)
        .filter(
            Annotation.task_id == task_id,
            Annotation.item_id == item_id,
            Annotation.annotator_id == user.id,
        )
        .first()
    )
    if annotation is None:
        return ok(None)
    return ok(AnnotationOut.model_validate(annotation))


@router.put("/tasks/{task_id}/items/{item_id}/annotation")
def save_annotation(
    task_id: int,
    item_id: int,
    body: AnnotationSave,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = _get_task_or_404(db, task_id)
    if db.get(DataItem, item_id) is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "数据条目不存在"})
    if body.type != task.type:
        raise HTTPException(
            status_code=400,
            detail={"code": 40001, "message": f"任务类型为 {task.type}，标注类型必须一致"},
        )
    payload = _validate_payload(body.type, body.payload)

    annotation = (
        db.query(Annotation)
        .filter(
            Annotation.task_id == task_id,
            Annotation.item_id == item_id,
            Annotation.annotator_id == user.id,
        )
        .first()
    )
    if annotation is None:
        annotation = Annotation(
            task_id=task_id,
            item_id=item_id,
            annotator_id=user.id,
            type=body.type,
            payload=payload,
        )
        db.add(annotation)
    else:
        annotation.payload = payload
        annotation.type = body.type
    db.commit()
    db.refresh(annotation)
    return ok(AnnotationOut.model_validate(annotation), "保存成功")