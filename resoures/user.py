from flask_restful import Resource

from models.user_model import UserModel

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found..."}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found..."}, 404
        user.delete()
        return {"message": "User deleted"}, 200
