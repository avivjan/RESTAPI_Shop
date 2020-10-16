from flask_restful import Resource, reqparse
import sqlite3


class ItemsList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}
