from app import app

from app.api.get_file_by_url import get_file_by_url

from .favicon import favicon
from .index import index
from .gist_create import create_gist
from .gist_create_post_form import gist_create_post_form
from .gist_description import gist_description
from .gist_discover import gist_discover


@app.route('/favicon.ico')
def favicon_route():
    return favicon(app.root_path)


@app.route('/')
def index_route():
    return index()


@app.route('/create')
def create_gist_route():
    return create_gist()


@app.route('/gist/<link>')
def gist_description_route(link):
    return gist_description(link)


@app.route('/discover/')
@app.route('/discover/<int:page>')
def gist_discover_route(page=1):
    return gist_discover(page)


@app.route('/post/gist', methods=['POST'])
def gist_create_post_form_route():
    return gist_create_post_form()


@app.route('/api/file/<path:url>')
def get_file_by_url_route(url):
    return get_file_by_url(url)
