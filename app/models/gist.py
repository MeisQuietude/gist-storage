import datetime

from app import db
from app.models._tool import _Tool


class Gist(db.Model):
    id_ = db.Column(db.String(32), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean)
    link = db.Column(db.String(24), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, description, is_public=False):
        self.description = description
        self.is_public = is_public
        self.id_ = _Tool.gen_id()
        self.link = _Tool.make_link(self.id_, self.is_public)

    def __repr__(self):
        return f'Gist {self.id_}'
