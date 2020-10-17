import sqlite3
import os

class Item_model:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        requested_item = cursor.execute(select_query, (name, )).fetchone()
        connection.close()
        if requested_item:
            return cls(*requested_item)

    def insert(self):
        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (self.price, self.name))
        connection.commit()
        connection.close()
