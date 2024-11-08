from app.services.models.base import BaseModelService
from models.conversation import Conversation
from models.conversation_user import ConversationUser
from sqlalchemy import select, func, distinct


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
