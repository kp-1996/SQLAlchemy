from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT
from security import authenticate, identity
from database import Database
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Prasad"
api = Api(app)
# database_op = Database()

jwt = JWT(app, authenticate, identity)

class Adduser(Resource):
    def get(self):
        return Database.select_user()

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Adduser, '/getuser')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8080, debug = True)
