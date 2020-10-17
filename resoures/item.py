from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required
import os

from models.item_model import Item_model

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self, name: str):
        try:
            requested_item = Item_model.find_by_name(name)
        except:
            return {"message": "An error occurred searching the item: {}".format(name)}, 500
        if requested_item:
            return requested_item.json()
        return {"message": "Item not found"}, 404


    def post(self, name):
        if Item_model.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = Item_model(name, data["price"])
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item: {}".format(item["name"])}, 500
        return item.json(), 201

    def delete(self, name):
        try:
            connection = sqlite3.connect(os.getcwd() + "/data.db")
            cursor = connection.cursor()

            delete_query = "DELETE FROM items WHERE name=?"
            cursor.execute(delete_query, (name,))
            connection.commit()
            connection.close()
        except:
            return {"message": "An error occurred deleting the item: {}".format(name)}, 500

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        new_item = Item_model(name, data.get("price"))

        try:
            result = Item_model.find_by_name(name)
        except:
            return {"message": "An error occurred searching the result: {}".format(name)}, 500

        if result is None:
            try:
                new_item.insert()
            except:
                return {"message": "An error occurred putting result: {}".format(name)}, 500
        else:
            try:
                new_item.update()
            except:
                return {"message": "An error occurred putting result: {} ".format(name)}, 500
        return new_item.json()

