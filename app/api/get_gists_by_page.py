from sqlalchemy import desc

from config import NUMBER_GISTS_ON_PAGE
from app.models.gist import Gist


def get_gists_by_page(i: int = 1, number_gist_on_page: int = NUMBER_GISTS_ON_PAGE) -> list:
    """
    :param i: number of page: 1 to N
    :param number_gist_on_page: maximum gists by page
    :return: list or None
    """

    if i < 0: i = 1

    i = i - 1
    start = i * number_gist_on_page
    end = start + number_gist_on_page
    gists = Gist.query.filter(Gist.is_public).order_by(desc(Gist.created_at)).slice(start, end).all()

    return gists
