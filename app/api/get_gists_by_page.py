from sqlalchemy import desc

from config import NUMBER_GISTS_ON_PAGE
from app.models.gist import Gist


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
