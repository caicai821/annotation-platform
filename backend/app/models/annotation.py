from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Annotation(Base):
    """统一标注表：文本与图像共用，靠 type 区分，payload 存 JSON。"""

    __tablename__ = "annotations"
    __table_args__ = (UniqueConstraint("task_id", "item_id", "annotator_id", name="uq_annotation_task_item_annotator"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("data_items.id"), index=True)
    annotator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[str] = mapped_column(String(16))  # text / image
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(16), default="saved")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
