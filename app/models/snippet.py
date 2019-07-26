from app import db
from app.models._tool import _Tool


class Snippet(db.Model):
    id_ = db.Column(db.String(32), primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    code = db.Column(db.Text, nullable=False)
    gist_id = db.Column(db.String(32), db.ForeignKey('gist.id_'), nullable=False)
    gist = db.relationship('Gist', backref=db.backref('snippets', lazy=True))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id_'), default=1)
    language = db.relationship('Language')

    def __init__(self, gist_id, filename, language_id, code):
        self.id_ = _Tool.gen_id()
        self.gist_id = gist_id
        self.filename = filename
        self.language_id = language_id
        self.code = code

    def __repr__(self):
        return f'Snippet {self.id_}'
