import os
from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://guest:1111@192.168.3.110/soogeup_api?charset=utf8'
# 환경변수 DATABASE_URL 이 없으면 디폴트(SQLite3-data.db) 사용
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aqr4'
api = Api(app)

jwt = JWT(app, authenticate, identity)   # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    @app.before_first_request # 위 config에서 설정한 DB를 생성합니다.  강의 109.  근데 안되는데 ?
    def create_tables():
        db.create_all()

    app.run(host='192.168.1.101', port=5000, debug=True)
