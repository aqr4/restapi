from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    name = db.Column(db.String(50), primary_key=True)
    price = db.Column(db.Float(precision=2))

    store_cd = db.Column(db.String(3), db.ForeignKey('stores.cd')) # 외래키 설정
    store = db.relationship('StoreModel') # 관계 알려줌

    def __init__(self, name, price, store_cd):
        self.name = name
        self.price = price
        self.store_cd = store_cd

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_cd': self.store_cd}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # select * from items where name=name limit 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
