import os
import re

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'jdbc:postgresql://localhost:5432/gists'
db = SQLAlchemy()


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('gist/create.html')

    assert request.method == 'POST'
    form: ImmutableMultiDict = request.form

    description: str = form.get('description', None).strip()
    if description is None:
        return render_template('gist/create.html', error="Gist's description can't be empty")

    filenames: list = form.getlist('filename', str)
    languages: list = []

    for name in filenames:
        # trying to get language name by file extension
        _, ext = os.path.splitext(name)
        lang = _get_supported_language_by_ext(ext)
        languages.append(lang)

    code_snippets: list = form.getlist('code', str)
    try:
        assert len(code_snippets) > 0
        assert len(code_snippets) == len(languages) == len(filenames)
    except AssertionError:
        return render_template('gist/create.html', error="Something get wrong...")

    for i in range(len(code_snippets)):
        # trying to get language name by shebang
        if languages[i] is not None: continue

        snippet = code_snippets[i]
        first_line = snippet.split('\n')[0]

        pattern = re.compile(r"#! ?[/\S]+ ?[python]")
        matched = pattern.match(first_line)

        if matched is None: continue
        languages[i] = "Python"

    languages = list(map(lambda l: l if l is not None else "Unknown language", languages))

    gists: dict = {}
    for i in range(len(filenames)):
        gists[filenames[i]] = {"language": languages[i],
                               "code_snippet": code_snippets[i]}

    return render_template('gist/description.html', description=description, gists=gists)


def _get_supported_language_by_ext(ext: str) -> str or None:
    """
    Supported languages: JS, Python, C++, PHP, Java
    """
    lang = None
    supported_exts = ('.js', '.py', '.cpp', '.myphp', '.java')
    supported_langs = ('JavaScript', 'Python', 'C++', 'PHP', 'Java')
    lang = dict(zip(supported_exts, supported_langs)).get(ext.lower(), None)
    return lang


@app.route('/discover')
def discover():
    return render_template('gist/list.html')


@app.route('/gist/<id>', methods=['GET', 'POST'])
def gist(id):
    """
    GET: looking for page of gist
    POST: create new one gist
    """
    if request.method == 'POST':
        pass
    else:
        return render_template('gist/description.html')


if __name__ == '__main__':
    app.run()
