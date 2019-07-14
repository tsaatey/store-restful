
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Create an item APi
class Item(Resource):
    parser = reqparse.RequestParser()

    # Set the item price in the json
    parser.add_argument(
        'price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )

    parser.add_argument(
        'store_id',
        type = int,
        required = True,
        help = "Every item need a store Id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        response = self.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {"message": f"Item with name {name} already exists"}, 400
        try:
            item = ItemModel(name, response['price'], response['store_id'])
            item.save_to_db()
        except:
            return {'message': 'Item could not be saved!'}, 500

        return {'message': 'success', 'result': item.json()}, 201

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)

        if not item:
            return {"message": f"Item name {name} cannot be found"}, 404
        else:
            item.delete_from_db()

        return {'message': '{} has been deleted!'.format(name)}, 200

    @jwt_required()
    def put(self, name):
        response = self.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **response)
        else:
            item.price = response['price']

        item.save_to_db()

        return {'message': 'Update successful', 'result': item.json()}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        """
            Using a lambda function

            return {'items': list(map(lambda x: x.json, ItemModel.query.all()))}
        """

        return {'items': [item.json() for item in ItemModel.query.all()]}
