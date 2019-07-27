from flask import url_for, render_template
from werkzeug.utils import redirect

from app.api.front.count_pages import count_pages
from app.api.front.get_navigation_page_numbers import get_navigation_page_numbers
from app.api.front.make_code_preview import make_code_preview
from app.api.get_gists_by_page import get_gists_by_page
from app.api.get_language_statistic import get_language_statistic


def gist_discover(page):
    _last_page = count_pages()
    info = {
        "current_page": page,
        "last_page": _last_page,
        "navigation_page_numbers": get_navigation_page_numbers(page, _last_page),
        "preview": make_code_preview,
        "language_statistic": get_language_statistic()
    }
    if page > _last_page:
        # if user try go to page > last allowed page
        return redirect(url_for('gist_discover_route', page=_last_page))

    gists = get_gists_by_page(page)
    return render_template('gist/list.html', info=info, gists=gists)
