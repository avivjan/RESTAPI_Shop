import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

from resoures.User_login import UserLogin
from resoures.user_register import UserRegister
from resoures.item_list import ItemsList
from resoures.item import Item
from resoures.store import Store
from resoures.store_list import StoreList
from resoures.user import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")   # If the envarioment var is not assigned use the local SQlite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "Hecktor"
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemsList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
