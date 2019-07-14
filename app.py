import os
import re

from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from werkzeug.datastructures import ImmutableMultiDict

from config import POSTGRES_DATABASE_URL, APP_DEBUG

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_DATABASE_URL
    db.init_app(app)

    engine = create_engine(POSTGRES_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app


from model import Gist, Snippet

app = create_app()


@app.route('/', methods=['GET'])
def index():
    return render_template('gist/create.html')


@app.route('/post/gist', methods=['POST'])
def post_gist():
    form: ImmutableMultiDict = request.form

    description: str = form.get('description', '').strip()
    if not description:
        return render_template('gist/create.html', error="Gist's description can't be empty")
    is_public: bool = bool(int(form.get('public', 0)))

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

        pattern = re.compile(r"#! ?[/\S]+ ?[python]")  # shebang for python (it's only one supported and use shebang)
        matched = pattern.match(first_line)

        if matched is None: continue
        languages[i] = "Python"

    gist = Gist(description, is_public)

    for i in range(len(filenames)):
        snippet = Snippet(gist.id_, filenames[i], languages[i], code_snippets[i], i)
        gist.snippets.append(snippet)

    db.session.add(gist)
    db.session.commit()

    return redirect(url_for('gist_description', link=gist.link))


@app.route('/gist/<link>')
def gist_description(link):
    gist = get_gist_api(link)
    if gist is None:
        return render_template('gist/description.html', error={"error": "gist not exists"})
    return render_template('gist/description.html', gist=gist)


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


# @app.route('/api/gist/<id_>')
def get_gist_api(id_=None) -> Gist or None:
    """
    :param id_: id_ (len:32), public link (len:8), private link (len:24)
    :return: object (type 'Gist') or None
    """
    try:
        assert id_ is not None

        id_length = len(id_)
        if id_length == 32:
            # Full id\link ( developer case )
            result = Gist.query.filter(Gist.id_ == id_).first()
        elif id_length == 24:
            # Private link
            result = Gist.query.filter(Gist.id_.endswith(id_)).first()
        elif id_length == 8:
            # Public link
            result = Gist.query.filter(Gist.id_.startswith(id_)).first()
        else:
            result = None

        assert result is not None

        return result

    except AssertionError:
        return None


def get_all_gists_api():
    """
    :return: Gists or None
    """
    gists = Gist.query.filter(Gist.is_public)
    return gists


if __name__ == '__main__':
    app.run()
