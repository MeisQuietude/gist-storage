import os

from flask import request, render_template, redirect, url_for
from werkzeug.datastructures import ImmutableMultiDict

from app import db
from app.api.guess_language_by_extension import guess_language_by_extension
from app.api.guess_language_by_shebang import guess_language_by_shebang
from app.models.gist import Gist
from app.models.snippet import Snippet


def gist_create_post_form():
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
        languages[i] = guess_language_by_extension(ext)

        if languages[i]: continue

        # trying to get language name by shebang
        code_snippet = code_snippets[i]
        first_line = code_snippet.split('\n')[0]
        languages[i] = guess_language_by_shebang(first_line)

    gist = Gist(description, is_public)

    for i in range(len(filenames)):
        code_snippet = Snippet(gist.id_, filenames[i], languages[i], code_snippets[i])
        gist.snippets.append(code_snippet)

    db.session.add(gist)
    db.session.commit()

    return redirect(url_for('gist_description_route', link=gist.link))
