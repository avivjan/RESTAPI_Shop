import sqlite3
from models.user_model import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Please insert username")
    parser.add_argument("password", type=str, required=True, help="Please insert password")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"massage": "This username is already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"massage": "User created succesfully"}, 201

