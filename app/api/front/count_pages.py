from math import ceil

from app.models.gist import Gist
from config import NUMBER_GISTS_ON_PAGE


def count_pages() -> int:
    """
    Count pages
    :return: number of pages
    """
    gists = Gist.query.filter(Gist.is_public).all()
    return ceil(len(gists) / NUMBER_GISTS_ON_PAGE)
