from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from userRegister import UserRegister
from itemList import ItemsList
from item import Item
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = "Hecktor"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemsList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
