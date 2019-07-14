import datetime
import uuid
from app import db


class DB_Tools:
    @staticmethod
    def gen_id():
        """
        Generates random uuid
        :return: uuid.hex string, length = 32
        """
        return uuid.uuid4().hex

    @staticmethod
    def make_link(id_: str, is_public: bool):
        """
        Generate link by id
        :param id_: uuid4().hex, length = 32
        :param is_public: is public gist or not
        :return url string
        """
        return id_[:8] if is_public else id_[8:]


class Gist(db.Model):
    id_ = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean)
    link = db.Column(db.String(80), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    snippets = db.relationship('Snippet', backref="gist", lazy="dynamic")

    # For __repr__
    columns = ('id_', 'description', 'is_public', 'link', 'created_at')
    values = (id_, description, is_public, link, created_at)

    def __init__(self, description, is_public=False):
        self.description = description
        self.is_public = is_public
        self.id_ = DB_Tools.gen_id()
        self.link = DB_Tools.make_link(self.id_, self.is_public)

    def __repr__(self):
        return f'Gist {self.id_}'


class Snippet(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(80), nullable=True)
    code = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    gist_id = db.Column(db.Integer, db.ForeignKey('gist.id_'), nullable=False)
    gist = db.relationship('Gist')

    # For __repr__
    columns = ('id_', 'gist_id', 'language', 'code')
    values = (id_, gist_id, language, code)

    def __init__(self, gist_id, language, code, order):
        self.id_ = DB_Tools.gen_id()
        self.gist_id = gist_id
        self.language = language
        self.code = code
        self.order = order

    def __repr__(self):
        return f'Snippet {self.id_}'
