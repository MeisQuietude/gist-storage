from ._get_file_by_url import get_file
from config import MAX_SIZE_UPLOAD_CONTENT_BY_URL


def get_file_by_url(url):
    return get_file(url, max_size=MAX_SIZE_UPLOAD_CONTENT_BY_URL)
