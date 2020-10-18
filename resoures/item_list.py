from flask_restful import Resource

from models.itemmodel import ItemModel


class ItemsList(Resource):
    def get(self):
        return {"items": [item.json for item in ItemModel.query.all()]}
               # list(map(item.json(), Item_model.query().all())) is the same