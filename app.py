import os
import re
from collections import defaultdict, OrderedDict

from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, desc
from sqlalchemy_utils import database_exists, create_database
from werkzeug.datastructures import ImmutableMultiDict

from advanced import AdvancedTool
from config import POSTGRES_DATABASE_URL, NUMBER_GISTS_ON_PAGE, SUPPORTED_LANGUAGES
from upload_file import download_file_by_url

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    engine = create_engine(POSTGRES_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        with app.app_context():
            db.create_all()
            for supported_language in SUPPORTED_LANGUAGES:
                db.session.add(Language(supported_language))
            db.session.commit()

    return app


from model import Gist, Snippet, Language

app = create_app()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico')


@app.route('/')
def index():
    return render_template('gist/create.html')


@app.route('/gist/<link>')
def gist_description(link):
    gist = get_gist_api(link)
    if gist is None or not Gist.query.filter(Gist.link == link).limit(1).all():
        return render_template('gist/description.html', errors=["Gist not found"])
    return render_template('gist/description.html', gist=gist)


@app.route('/discover/')
@app.route('/discover/<int:page>')
def discover(page=1):
    _last_page = AdvancedTool.get_last_page_number(get_gists_by_page(0))
    info = {
        "current_page": page,
        "last_page": _last_page,
        "page_numbers": AdvancedTool.get_page_numbers(page, _last_page),
        "get_preview": AdvancedTool.get_preview_from_code,
        "language_statistic": _get_snippet_statistic_by_languages()
    }
    if page > _last_page:
        page = _last_page
        return redirect(url_for('discover', page=page))

    gists = get_gists_by_page(page)
    return render_template('gist/list.html', info=info, gists=gists)


@app.route('/post/gist', methods=['POST'])
def post_gist():
    errors = []

    form: ImmutableMultiDict = request.form
    description: str = form.get('description', '').strip()
    is_public: bool = bool(int(form.get('public', 0)))
    filenames: list = form.getlist('filename', str)
    code_snippets: list = form.getlist('code', str)

    if not description or len(description) > 255:
        errors.append(f'Length of description should be between 1 and {255}')
    if not filenames or not all(0 < len(name) <= 80 for name in filenames):
        errors.append(f'Length of filenames should be between 1 and {80}')
    if not code_snippets or not all(code_snippets):
        errors.append(f'Length of code should not be empty')

    if errors:
        return render_template('gist/create.html', errors=errors)

    languages: list = [0] * len(filenames)
    for i in range(len(languages)):
        # trying to get language name by file extension
        _, ext = os.path.splitext(filenames[i])
        languages[i] = _get_supported_language_by_ext(ext)

        if languages[i]: continue

        # trying to get language name by shebang
        code_snippet = code_snippets[i]
        first_line = code_snippet.split('\n')[0]
        languages[i] = _get_supported_language_by_shebang(first_line)

    gist = Gist(description, is_public)

    for i in range(len(filenames)):
        code_snippet = Snippet(gist.id_, filenames[i], languages[i], code_snippets[i])
        gist.snippets.append(code_snippet)

    db.session.add(gist)
    db.session.commit()

    return redirect(url_for('gist_description', link=gist.link))


def _get_supported_language_by_ext(ext: str) -> int:
    ext = ext.lower()
    for supp_lang, supp_ext in SUPPORTED_LANGUAGES.items():
        if ext in supp_ext:
            return list(SUPPORTED_LANGUAGES.keys()).index(supp_lang)
    return 0


def _get_supported_language_by_shebang(line: str) -> int:
    pattern = re.compile(r"#!/(?:\S+/)+(\S+)")
    matched = pattern.match(line)
    if not matched: return 0

    language = matched.group(1).lower()
    for supp_language in SUPPORTED_LANGUAGES.keys():
        if language == supp_language:
            return list(SUPPORTED_LANGUAGES.keys()).index(language)
    return 0


def _get_snippet_statistic_by_languages():
    count = defaultdict(int)
    for gist in Gist.query.filter(Gist.is_public):
        for snippet in gist.snippets:
            count[snippet.language] += 1

    total_count = sum(count.values())
    stats = OrderedDict(sorted(count.items(), key=lambda lang: lang[0].__repr__()))
    for k in stats.keys():
        # get a percent values
        stats[k] = stats[k] / total_count

    return stats


@app.route('/api/file/<path:url>')
def get_file_by_url_api(url):
    return download_file_by_url(url)


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
            raise AssertionError
        return result
    except AssertionError:
        return None


def get_gists_by_page(i: int = 0, number_gist_on_page: int = NUMBER_GISTS_ON_PAGE):
    """
    :param i: number of page: 1 to N (0 for all)
    :param number_gist_on_page: maximum gists by page
    :return: list or None
    """
    if i < 0: i = 0
    gists = None
    if i == 0:
        gists = Gist.query.filter(Gist.is_public).order_by(desc(Gist.created_at)).all()
    else:
        i = i - 1
        start = i * number_gist_on_page
        end = start + number_gist_on_page
        gists = Gist.query.filter(Gist.is_public).order_by(desc(Gist.created_at)).slice(start, end).all()
    return gists


if __name__ == '__main__':
    app.run()
