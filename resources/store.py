from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_byname(name)
        if store:
            return store.json(), 200
        return {"message":"A store with name {} not exists".format(name)}, 201

    @jwt_required()
    def post(self, name):
        if StoreModel.find_byname(name):
            return {"message":"A store with name {} already exists".format(name)}, 404

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error occured while saving store"}, 500
        return store.json(), 200

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_byname(name)
        if store:
            store.delete_from_db()

        return {"message":"Store Deleted"}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {"Stores":[store.json() for store in StoreModel.query.all()]}
