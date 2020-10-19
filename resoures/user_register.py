from models.user_model import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Please insert username")
    parser.add_argument("password", type=str, required=True, help="Please insert password")


    def post(self):
        data = UserRegister.parser.parse_args()  # data is a dictionary

        if UserModel.find_by_username(data["username"]):
            return {"massage": "This username is already exists"}, 400

        user = UserModel(**data)
        user.add()
        return {"massage": "User created succesfully"}, 201

