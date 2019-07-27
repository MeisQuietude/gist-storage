from config import MAX_SIZE_UPLOAD_CONTENT_BY_URL
from ._get_file_by_url import get_file


def get_file_by_url(url):
    """
    Upload content by scrapping url
    :param url:
    :return: json.dumps({filename: filename, content: content})
    """
    return get_file(url, max_size=MAX_SIZE_UPLOAD_CONTENT_BY_URL)
