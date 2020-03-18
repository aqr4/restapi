from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('cd',
        type = str,
        required = True,
        help="이 필드는 비워둘 수 없습니다."
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A stroe with name '{}' already exists.".format(name)}, 400

        data = Store.parser.parse_args()

        store = StoreModel(name, data['cd'])

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the stroe.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores:': [x.json() for x in StoreModel.query.all()]}
