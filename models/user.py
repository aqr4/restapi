from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # 여기 id 없으면 오류남, id는 파이썬 내장 메소드임
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))

    def __init__(self, email, password):  # 여기는 ID 없어도 됨 (SQLAlchemy가 self.id 자동 제공)
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):     # find_by_email, find_by_id 같이 혼용해서 사용해도 정상 작동함
        return cls.query.filter_by(email=email).first()  # select * from users where email=email limit 1

    @classmethod
    def find_by_id(cls, _id):     # find_by_email, find_by_id 같이 혼용해서 사용해도 정상 작동함
        return cls.query.filter_by(id=_id).first()  # select * from users where email=email limit 1
