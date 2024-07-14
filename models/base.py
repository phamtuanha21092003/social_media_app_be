from db import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)



class TimestampModel(db.Model):
    __abstract__ = True

    created: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
