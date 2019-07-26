from math import ceil

from config import NUMBER_GISTS_ON_PAGE


def count_pages(all_gists):
    return ceil(len(all_gists) / NUMBER_GISTS_ON_PAGE)
