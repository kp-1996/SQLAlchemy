from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field can not be empty"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_byname(name)
        if item:
            return item.json(), 201
        return {"message":"item not found"}, 400

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_byname(name)
        if item:
            item.delete_from_db()
            return {"meassage":"Item deleted", "item":item.json()}
        return {"message":"An item with name {} is not exists".format(name)}, 400

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_byname(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type = str,
        required = True,
        help = "This field can not be empty"
    )
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field can not be empty"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id"
    )
    # @jwt_required()
    def post(self):
        data = ItemList.parser.parse_args()
        item = ItemModel.find_byname(data['name'])
        if item:
            return {"message":"An item with name {} already exists".format(name)}
        item = ItemModel(**data)
        try:
            item.save_to_db()
        except:
            return {"message":" an error occured inserting the item"}, 500
        return item.json(), 201

    # @jwt_required()
    def get(self):
        return {"items":list(map(lambda x: x.json(), ItemModel.query.all()))} #[item.json() for item in ItemModel.query.all()]
