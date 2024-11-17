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
        query = text(
            """
                SELECT DISTINCT ON (ccm.conversation_id)
                    ccm.conversation_id,
                    ccm.content,
                    ccm.created,
                    CASE WHEN (ccm.creator_id = :user_id) THEN ccm.target_id ELSE ccm.creator_id END AS user_id,
                    ccm.creator_id,
                    ccm.status
                FROM chat_conversation_message ccm
                WHERE ccm.creator_id = :user_id or ccm.target_id = :user_id
                ORDER BY ccm.conversation_id, ccm.created desc
                LIMIT :limit
                OFFSET :offset
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
