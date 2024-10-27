from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user


class Conversations(Resource):
    def get(self):
        pass


    @jwt_required()
    def post(self):
        user_id = current_user.id

