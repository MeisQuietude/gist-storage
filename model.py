from app import db


class DB_Tools:
    @staticmethod
    def gen_id():
        # TODO
        return 0

    @staticmethod
    def make_link():
        # TODO
        return "no"


class Gist(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    is_private = db.Column(db.Boolean)
    link = db.Column(db.String(80), unique=True)
    snippets = db.relationship('Snippet', backref="gist", lazy="dynamic")

    # For __repr__
    columns = ('id_', 'description', 'is_private', 'link')
    values = (id_, description, is_private, link)

    def __init__(self, description, is_private):
        self.description = description
        self.is_private = is_private
        self.id_ = DB_Tools.gen_id()
        self.link = DB_Tools.make_link()

    def __repr__(self):
        return f'Gist {self.id_}'


class Snippet(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.Integer, db.ForeignKey('gist.id_'), nullable=False)
    language = db.Column(db.String(80), nullable=True)
    code = db.Column(db.Text)

    # For __repr__
    columns = ('id_', 'gist_id', 'language', 'code')
    values = (id_, gist_id, language, code)

    def __init__(self, gist_id, language, code):
        self.id_ = DB_Tools.gen_id()
        self.gist_id = gist_id
        self.language = language
        self.code = code

    def __repr__(self):
        return f'Snippet {self.id_}'
