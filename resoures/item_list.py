from flask_restful import Resource
from flask_jwt_extended import jwt_optional,get_jwt_identity

from models.itemmodel import ItemModel


class ItemsList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items},200
        else:
            return {
                 "items": [item["name"] for item in items],
                 "message": "Login for more info..."
            }, 200
