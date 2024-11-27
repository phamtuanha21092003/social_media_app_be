from app.services.models.base import BaseModelService
from models.comment import Comment
from sqlalchemy import select, text


class CommentService(BaseModelService):
    def __init__(self):
        self.model = Comment


    def get_count_comment_of_post(self, post_id):
        return self.get_total(select(Comment).where(Comment.post_id == post_id))


    def delete_comment_by_id(self, comment_id: int):
        query = text("DELETE FROM comment WHERE id = :comment_id")

        self.session.execute(query, {"comment_id": comment_id})

        self.session.flush()
