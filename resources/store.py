from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'Message':'Store Not found'}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'Message': 'The store {} already exists'.format(name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {'message': "An Error occurred inserting the item"}, 500  # Internal server error
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'Message': name+' has been deleted'}, 200
        else:
            return {'Message': name + ' Cannot be found'}, 400

class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}


