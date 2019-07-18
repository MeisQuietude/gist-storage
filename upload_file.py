import json
import time

import requests


class DownloadException(BaseException):
    pass


class SizeException(BaseException):
    pass


def download_file_by_url(url: str, max_size: int = None, retry: int = 0):
    """
    Скачивает файл по ссылке
    :param url:
    :param ограничение на размер файла, смотрятся по заголовкам max_size:
    :param количество попыток получить 200 ответ от сервера retry:
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
    file_name = url.split('/')[-1]
    return json.dumps({'filename': file_name, 'content': response.content.decode('utf-8')})


def _wait_response(request_params: dict, retry: int) -> requests.Response:
    """
    Ждет 200 ответа от сервера
    :param request_params:
    :param retry:
    :return: :class:`Response <Response>` object
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
    Провяряет заголовки на допустимый размер контента
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


if __name__ == '__main__':
    uri = 'https://raw.githubusercontent.com/odoo/odoo/12.0/odoo/modules/graph.py'
    f = download_file_by_url(uri)
    print(f)
