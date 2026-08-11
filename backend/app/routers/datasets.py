from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DataItem, Dataset, User
from ..response import ok
from ..schemas import DataItemCreate, DataItemOut, DatasetCreate, DatasetOut
from ..security import get_current_user

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("")
def list_datasets(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total = db.query(Dataset).count()
    items = (
        db.query(Dataset)
        .order_by(Dataset.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return ok(
        {
            "items": [DatasetOut.model_validate(i) for i in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.post("")
def create_dataset(
    body: DatasetCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    dataset = Dataset(**body.model_dump(), created_by=user.id)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return ok(DatasetOut.model_validate(dataset), "创建成功")


@router.get("/{dataset_id}/items")
def list_items(
    dataset_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    dataset = db.get(Dataset, dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "数据集不存在"})
    total = db.query(DataItem).filter(DataItem.dataset_id == dataset_id).count()
    items = (
        db.query(DataItem)
        .filter(DataItem.dataset_id == dataset_id)
        .order_by(DataItem.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return ok(
        {
            "items": [DataItemOut.model_validate(i) for i in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.post("/{dataset_id}/items")
def create_item(
    dataset_id: int,
    body: DataItemCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    dataset = db.get(Dataset, dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail={"code": 40401, "message": "数据集不存在"})
    item = DataItem(dataset_id=dataset_id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return ok(DataItemOut.model_validate(item), "添加成功")