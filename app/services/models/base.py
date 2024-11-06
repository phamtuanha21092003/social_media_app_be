from sqlalchemy import Select, func, select, exc
from db import db
from models import BaseModel
from typing import Type



class BaseModelService:
    model: Type[BaseModel] = None
    session = db.session


    def find_by_id(self, model_id: int):
        return db.session.scalars(select(self.model).where(self.model.id == model_id)).first()


    def create(self, is_flush: bool=True, is_commit: bool=True, **data):
        obj = self.model()

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)

        if is_flush:
            db.session.flush()

        if is_commit:
            db.session.commit()

        return obj


    def update(self, obj: Type[BaseModel], id: int|None=None, is_flush: bool=True, only: tuple=None, **data):
        if id: 
            obj = self.find_by_id(id)

        if obj:
            for k in data:
                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        if is_flush:
            self.session.flush()
        return obj


    def get_total(self, subquery: Select) -> int:
        total = self.session.execute(select(func.count()).select_from(subquery)).scalar()

        return total


    # kwargs is used to pass the filter condition
    def find(self, selectors=None, joiners: list=[], is_get_total: bool=False, is_get_query: bool=False, order_bys: list=[], **kwargs):
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

        if is_get_total:
            total = self.get_total(query)

        if len(order_bys) > 0:
            query = query.order_by(*order_bys)

        if not (limit is None or offset is None):
            query = query.limit(limit).offset(offset)

        if is_get_total:
            return self.session.scalars(query).all(), total

        return self.session.scalars(query).all()


    def first(self, selectors=None, joiners: list=[], **kwargs):
        if selectors is None:
            selectors = (self.model, )

        query = select(*selectors)

        for join in joiners:
            query = query.join(*join)

        for key, value in kwargs.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue

            query = query.filter(getattr(self.model, key) == value)

        return self.session.scalars(query).first()


    def delete(self, obj, is_flush=True):
        try:
            self.session.delete(obj)
            if is_flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e


    def where(self, query, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, list):
                query = query.where(getattr(self.model, key).in_(value))
                continue

            query = query.where(getattr(self.model, key) == value)

        return query
