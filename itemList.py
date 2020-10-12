from flask_restful import Resource, reqparse


class ItemsList(Resource):
    def get(self):
        return {"items": items}