from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.itemmodel import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs a store id")

    @jwt_required
    def get(self, name: str):
        try:
            requested_item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred searching the item: {}".format(name)}, 500
        if requested_item:
            return requested_item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.add_or_update()
        except:
            return {"message": "An error occurred inserting the item: {}".format(item["name"])}, 500
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privillege is required"}, 401
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete()
            except:
                 return {"message": "An error occurred deleting the item: {}".format(name)}, 500
        else:
            return {"message": "An item with name {} does not exist".format(name)}

        return {"message": "Item deleted"},

    def put(self, name):
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred searching the result: {}".format(name)}, 500

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occurred putting result: {}".format(name)}, 500
        else:
            try:
                item.price = data["price"]
                item.store_id = data["store_id"]
            except:
                return {"message": "An error occurred putting result: {} ".format(name)}, 500
        item.add_or_update()
        return item.json(), 201

