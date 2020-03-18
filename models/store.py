from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    cd = db.Column(db.String(3))
    name = db.Column(db.String(50))

    items = db.relationship('ItemModel', lazy='dynamic') # 관계 알려줌
    #items = db.relationship('ItemModel') # 관계 알려줌

    def __init__(self, name, cd):
        self.cd = cd
        self.name = name

    def json(self):
        return {'cd': self.cd, 'name': self.name, 'items': [x.json() for x in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # select * from items where name=name limit 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
