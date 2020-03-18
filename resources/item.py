from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help="이 필드는 비워둘 수 없습니다."
    )
    parser.add_argument('store_cd',
        type = str,
        required = True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' aleady exists.".format(name)}, 400  # 400 응답: 잘못된 요청

        data = Item.parser.parse_args()

        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return{"message": "An error occurred inserting the item."}, 500

        return item.json(), 201 # 201:create

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            #item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            #item.store_id = data['store_id']  #item의 상점 변경은 하지 않는 걸로 하지...
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #람다식, 위와 동일함
