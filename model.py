import datetime
import uuid

from app import db


class _Tools:
    @staticmethod
    def gen_id():
        """
        Generates random uuid
        :return: uuid.hex string, length = 32
        """
        return uuid.uuid4().hex

    @staticmethod
    def autoincrement(start=1, increment=1):
        i = start - increment
        while True:
            i += increment
            yield i

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
    id_ = db.Column(db.String(32), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean)
    link = db.Column(db.String(24), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, description, is_public=False):
        self.description = description
        self.is_public = is_public
        self.id_ = _Tools.gen_id()
        self.link = _Tools.make_link(self.id_, self.is_public)

    def __repr__(self):
        return f'Gist {self.id_}'


class Snippet(db.Model):
    id_ = db.Column(db.String(32), primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    code = db.Column(db.Text, nullable=False)
    gist_id = db.Column(db.String(32), db.ForeignKey('gist.id_'), nullable=False)
    gist = db.relationship('Gist', backref=db.backref('snippets', lazy=True))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id_'), default=1)
    language = db.relationship('Language')

    def __init__(self, gist_id, filename, language_id, code):
        self.id_ = _Tools.gen_id()
        self.gist_id = gist_id
        self.filename = filename
        self.language_id = language_id
        self.code = code

    def __repr__(self):
        return f'Snippet {self.id_}'


class Language(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    _autoincrement = _Tools.autoincrement(start=0)

    def __init__(self, name):
        self.id_ = next(Language._autoincrement)
        self.name = name

    def __repr__(self):
        return self.name if self.name else 'unknown'
