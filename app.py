from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resoures.userRegister import UserRegister
from resoures.itemList import ItemsList
from resoures.item import Item
from security import authenticate, identity


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Hecktor"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth Endpoint


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemsList, "/items")
api.add_resource(UserRegister, "/register")
db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    create_tables.run()
