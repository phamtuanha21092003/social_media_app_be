from app.services.models.base import BaseModelService
from models.post import Post
from sqlalchemy import Select


class PostService(BaseModelService):
    def __init__(self):
        self.model = Post


    def get_posts_by_keyword(self, keyword: str, limit: int, offset: int):
        query = Select(self.model).where(self.model.title.ilike(f'%{keyword}%'))

        total = self.get_total(query)

        return self.session.scalars(query.limit(limit).offset(offset)).all(), total
