from flask_restful import Resource

from models.item_model import Item_model


class ItemsList(Resource):
    def get(self):
        return {"items": [item.json for item in Item_model.query().all()]}
               # list(map(item.json(), Item_model.query().all())) is the same