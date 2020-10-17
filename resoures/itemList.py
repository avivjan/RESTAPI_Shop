from flask_restful import Resource, reqparse
import sqlite3
import os

class ItemsList(Resource):
    def get(self):

        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}
