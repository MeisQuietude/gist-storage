import json
import time

import requests


class DownloadException(BaseException):
    pass


class SizeException(BaseException):
    pass


def download_file_by_url(url: str, max_size: int = None, retry: int = 0):
    """
    Download file by link
    :param url:
    :param max_size: ограничение на размер файла, смотрятся по заголовкам max_size
    :param retry: количество попыток получить 200 ответ от сервера retry
    :return: dict{filename : content}
    """
    request_params = {
        'url': url,
        'stream': True,
        'allow_redirects': False,
    }
    response = _wait_response(request_params, retry)
    if response.status_code != 200:
        raise DownloadException(response.content)
    if max_size and not _check_size(url, max_size):
        return SizeException(url)
    filename = url.split('/')[-1]
    return json.dumps({'filename': filename, 'content': response.content.decode('utf-8')})


def _wait_response(request_params: dict, retry: int) -> requests.Response:
    """
    Wait 200 answer from server
    :param request_params:
    :param retry:
    :return: class:`Response <Response>` object
    :rtype: requests.Response[
    """
    response = requests.get(**request_params)
    while response.status_code != 200 and retry > 0:
        response = requests.get(**request_params)
        time.sleep(2)
        retry -= 1
    return response


def _check_size(url: str, max_size: int) -> bool:
    """
    Checks headers for allowed size of content
    :param url:
    :param max_size:
    :return:
    """
    h = requests.head(url)
    header = h.headers
    content_length = int(header.get('content-length', 0))
    if content_length and content_length > max_size:
        return False
    return True
