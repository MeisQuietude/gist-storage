import os

from flask import send_from_directory


def favicon(root):
    return send_from_directory(os.path.join(root, 'static', 'images'), 'favicon.ico')
