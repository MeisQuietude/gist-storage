from math import ceil

from app.api.get_all_gists import get_all_gists
from config import NUMBER_GISTS_ON_PAGE


def count_pages() -> int:
    """
    Count pages
    :return: number of pages
    """
    gists = get_all_gists()
    return ceil(len(gists) / NUMBER_GISTS_ON_PAGE)
