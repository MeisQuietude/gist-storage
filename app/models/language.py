from app import db
from app.models._tool import _Tool


class Language(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    _autoincrement = _Tool.autoincrement(start=0)

    def __init__(self, name):
        self.id_ = next(Language._autoincrement)
        self.name = name

    def __repr__(self):
        return self.name if self.name else 'unknown'
