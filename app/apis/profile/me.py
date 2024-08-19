from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService



class Me(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    def get(self):
        
        return {'message': 'Hello, World!'}