from flask_restful import Resource
from models.storemodel import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message" : "A store named {} is already exists".format(name)}
        new_store = StoreModel(name)
        try:
            new_store.add()
        except:
            return {"message" : "An error occurred while adding store named: {}".format(name)},500
        return new_store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete()
            except:
                return {"message": "An error occurred while deleting store named: {}".format(name)},500
            return {"message": "Store deleted"}
        return {"message":"There is no store named {}".format(name)}