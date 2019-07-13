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
    description = db.Column(db.String(255))
    is_private = db.Column(db.Boolean)
    link = db.Column(db.String(80))

    # For __repr__
    columns = ('id_', 'description', 'is_private', 'link')
    values = (id_, description, is_private, link)

    def __init__(self, description, is_private):
        self.description = description
        self.is_private = is_private
        self.id_ = DB_Tools.gen_id()
        self.link = DB_Tools.make_link()

    def __repr__(self):
        """
        :return: dict {"column_name": column_value}
        """
        return {k: v for k, v in zip(self.columns, self.values)}


class Snippet(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.Integer)
    language = db.Column(db.String(80))
    code = db.Column(db.String)

    # For __repr__
    columns = ('id_', 'gist_id', 'language', 'code')
    values = (id_, gist_id, language, code)

    def __init__(self, gist_id, language, code):
        self.id_ = DB_Tools.gen_id()
        self.gist_id = gist_id
        self.language = language
        self.code = code

    def __repr__(self):
        """
        :return: dict {"column_name": column_value}
        """
        return {k: v for k, v in zip(self.columns, self.values)}
