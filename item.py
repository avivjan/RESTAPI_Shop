from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        requested_item = cursor.execute(select_query, (name,)).fetchone()
        connection.close()
        if requested_item:
            return {"item": requested_item[0], "price": requested_item[1]}

    @jwt_required()
    def get(self, name: str):
        requested_item = Item.find_by_name(name)
        if requested_item:
            return requested_item
        return {"message": "Item not found"}, 404


    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item["name"], item["price"]))
        connection.commit()
        connection.close()
        return item, 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name=?"
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data.get("price")}
            items.append(item)
        else:
            item.update(data)
        return item
