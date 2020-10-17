import sqlite3
import os

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        row = cursor.execute(query, (username, )).fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect(os.getcwd() + "/data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        row = cursor.execute(query, (_id, )).fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        return user


