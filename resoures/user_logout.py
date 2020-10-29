from flask_restful import Resource
from flask_jwt_extended import get_raw_jwt, jwt_required
from models.black_listed_jti_model import BlackListedJWIModel


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = BlackListedJWIModel(get_raw_jwt()["jti"])
        BlackListedJWIModel.add(jti)

        return {
            "message": "User logged out successfully"
        }, 200
