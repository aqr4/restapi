from app import app
from db import db

db.init_app(app)

@app.before_first_request # 위 config에서 설정한 DB를 생성합니다.  강의 109.  근데 안되는데 ?
def create_tables():
    db.create_all()
