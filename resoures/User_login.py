from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user_model import UserModel

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="You must enter an username")
    parser.add_argument("password", required=True, help="You must enter a password")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and user.password == data["password"]:

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "Your login details is not correct"}, 401


