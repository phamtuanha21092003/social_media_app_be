from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class Emoji(BaseModel):
    __tablename__ = "emoji"

    url: Mapped[str] = mapped_column(nullable=False)

