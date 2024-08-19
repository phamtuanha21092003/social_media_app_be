from sqlalchemy import Select, func, select
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


    def get_total(self, subquery: Select) -> int:
        total = self.session.execute(select(func.count()).select_from(subquery)).scalar()

        return total


    # kwargs is used to pass the filter condition
    def find(self, selectors=None, joiners: list=[], is_get_total: bool=False, is_get_query: bool=False, **kwargs):
        if selectors is None:
            selectors = (self.model, )

        query = select(*selectors)

        for join in joiners:
            query = query.join(*join)

        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)

        for key, value in kwargs.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue

            query = query.filter(getattr(self.model, key) == value)

        if is_get_query:
            return query

        if limit and offset:
            query = query.limit(limit).offset(offset)

        if is_get_total:
            total = self.get_total(query)
            return self.session.scalars(query).all(), total

        return self.session.scalars(query).all()
