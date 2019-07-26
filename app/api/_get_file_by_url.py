import json
import time

import requests


class DownloadException(BaseException):
    pass


class SizeException(BaseException):
    pass


def get_file(url: str, max_size: int = None, retry: int = 0):
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

    filename = url.split('/')[-1]
    content = _process_content(response, max_size)

    return json.dumps({'filename': filename, 'content': content})


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


def _process_content(response: requests.Response, max_size: int) -> str:
    """
    Checks content for allowed size and return it
    :param response:
    :param max_size:
    :return: content string
    """
    content = ''
    for chunk in response.iter_content(1024, decode_unicode=True):
        content += chunk
        if len(content) > max_size:
            response.close()
            raise SizeException(f'File size is too large, {response.url}')

    return content
