import os
import datetime

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

from resoures.user_login import UserLogin
from resoures.user_register import UserRegister
from resoures.token_refresh import TokenRefresh
from resoures.item_list import ItemsList
from resoures.item import Item
from resoures.store import Store
from resoures.store_list import StoreList
from resoures.user import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")   # If the envarioment var is not assigned use the local SQlite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=5)
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
api.add_resource(TokenRefresh, "/refresh")

db.init_app(app)


# This wiil be called before executing the first request.
@app.before_first_request
def create_tables():
    db.create_all()


# This wiil be called every time a token is created, the data that returns here will add to the token as a claim.
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


# This will be called if client send an expired token.
@jwt.expired_token_loader
def expired_token_callback():
    return {
        "description": "This token has expired",
        "error": "token_expired"
    },401

# This will be called if client send an invalid token.
@jwt.invalid_token_loader
def invalid_token_callback(error)
    return {
        "description": "Signiture verification failed",
        "error": "invalid_token"
    }, 401


# This will be called if client dont send a token at all.
@jwt.unauthorized_loader
def missing_token_callback():
    return {
               "description": "Request does not contain an access token",
               "error": "authorization_required"
           }, 401

# This will be called if this method required a fresh token and client send a non-fresh token.
@jwt.needs_fresh_token_loader
def token_not_fresh_token():
    return {
               "description": "The token is not fresh",
               "error": "fresh_token_required"
           }, 401

# This will be called if client send a revoked token.
@jwt.revoked_token_loader
def revoked_token_callback():
    return {
               "description": "This token has been revoked",
               "error": "token_revoked"
           }, 401




if __name__ == "__main__":
    app.run(port=5000, debug=True)

