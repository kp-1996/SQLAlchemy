import sqlite3
from flask import jsonify
from models.user import UserModel

class Database:
    def __init__(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
        cursor.execute(query)

        item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
        cursor.execute(item_table)

        connection.commit()
        connection.close()

    @classmethod
    def select_user(cls):
        return {"users":list(map(lambda x: x.json(), UserModel.query.all()))}
