from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Dataset, Task, User
from ..response import ok
from ..schemas import TaskCreate, TaskOut, TaskUpdate
from ..security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total = db.query(Task).count()
    items = (
        db.query(Task).order_by(Task.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    )
    return ok(
        {
            "items": [TaskOut.model_validate(i) for i in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.post("")
def create_task(
    body: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    dataset = db.get(Dataset, body.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "数据集不存在"})
    if dataset.type != body.type:
        raise HTTPException(
            status_code=400,
            detail={"code": 40001, "message": f"任务类型必须与数据集类型一致（{dataset.type}）"},
        )
    task = Task(**body.model_dump(), created_by=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return ok(TaskOut.model_validate(task), "创建成功")


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "任务不存在"})
    return ok(TaskOut.model_validate(task))


@router.put("/{task_id}")
def update_task(
    task_id: int,
    body: TaskUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "任务不存在"})
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return ok(TaskOut.model_validate(task), "已更新")