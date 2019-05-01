from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be empty")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': "An Item with name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)#**data = data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': "An Error occurred inserting the item"}, 500 #Internal server error

        return item.json(), 201




    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'item':name+' has been deleted'}, 200
        return {'item':name+' does not exist'}, 400

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) #**data = data['price'], data['store_id']
        else:
            item.price = data['price']
            item.store_id= data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #list(map(lambda x: x.json(), ItemModel.query.all())}