from sqlalchemy import select
from db import db
from models import BaseModel
from typing import Type



class BaseModelService:
    model: Type[BaseModel] = None
    session = db.session

    def find_by_id(self, model_id: int):
        return db.session.scalars(select(self.model).where(self.model.id == model_id)).first()


    def create(self, is_flush: bool = True, is_commit: bool = True, **data):
        obj = self.model()

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)

        if is_flush:
            db.session.flush()

        if is_commit:
            db.session.commit()

        return obj

