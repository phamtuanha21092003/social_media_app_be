from app.services.models.base import BaseModelService
from models.conversation import Conversation
from models.conversation_user import ConversationUser
from sqlalchemy import select, func, distinct, text


class ConversationService(BaseModelService):
    def __init__(self):
        self.model = Conversation


    def get_conversation_by_user_ids(self, creator_id: int, target_id: int):
        query = select(self.model)\
            .join(ConversationUser, self.model.id==ConversationUser.conversation_id)\
            .where(ConversationUser.account_user_id.in_([creator_id, target_id]))\
            .group_by(self.model.id)\
            .having(func.count(distinct(ConversationUser.account_user_id))==2)

        return self.session.scalars(query).first()


    def get_conversation_ids_and_total(self, user_id: int, limit: int, offset: int):
        # todo: add limit offset to this function
        query = text(
            """
                SELECT c.id AS conversation_id,
                       cm.content AS last_message,
                       cm.created,
                       CASE WHEN (cm.creator_id = :user_id) THEN cm.target_id ELSE cm.creator_id END AS user_id,
                       cm.creator_id,
                       cm.status
                FROM chat_conversation c
                JOIN chat_conversation_message cm
                  ON c.id = cm.conversation_id
                  AND cm.created = (
                      SELECT MAX(created)
                      FROM public.chat_conversation_message
                      WHERE conversation_id = c.id
                  )
                WHERE cm.creator_id = :user_id OR cm.target_id = :user_id
                ORDER BY cm.created DESC
            """
        )

        query_total = text(
            """
                SELECT COUNT(DISTINCT(ccm.conversation_id))
                FROM chat_conversation_message ccm
                WHERE ccm.creator_id = :user_id or ccm.target_id = :user_id
            """
        )

        conversations = self.session.execute(query, {"user_id": user_id, "limit": limit, "offset": offset}).all()

        total = self.session.execute(query_total, {"user_id": user_id}).scalar()

        return [
            {
                "id": _c[0],
                "content": _c[1] if _c[5] != "DELETED" else "The message has been deleted",
                'created': _c[2],
                'user_id': _c[3],
                'creator_id': _c[4],
                'status': _c[5]
            } for _c in conversations
        ], total
