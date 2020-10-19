from flask_restful import Resource

from models.itemmodel import ItemModel


class ItemsList(Resource):
    def get(self):
        return {"items": [item.json for item in ItemModel.find_all()]}
               # list(map(item.json(), Item_model.find_all()) is the same