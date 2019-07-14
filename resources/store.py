from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with same name {name} already exists!'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': 'Delete failed as store name does not exist'}, 404

        store.delete_from_db()

        return {'message': f'Store with name {name} has been deleted successfully'}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
