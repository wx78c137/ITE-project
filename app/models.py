from app import db

class Result(db.Document):
    seq = db.IntField()
    result = db.StringField()
