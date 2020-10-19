from flask_restful import Resource

from models.storemodel import StoreModel

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}