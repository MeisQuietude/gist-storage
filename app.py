from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('gist/create.html')

    assert request.method == 'POST'
    form: ImmutableMultiDict = request.form

    description: str = form.get('description', None)
    filenames: list = form.getlist('filename', str)
    code_snippets: list = form.getlist('code', str)

    gists: dict = dict(zip(filenames, code_snippets))

    return render_template('gist/description.html', description=description, gists=gists)


@app.route('/discover')
def discover():
    return render_template('gist/list.html')


@app.route('/gist/<id>', methods=['GET', 'POST'])
def gist(id):
    """
    GET: looking for page of gist
    POST: create new one gist
    """
    if request.method == 'POST':
        pass
    else:
        return render_template('gist/description.html')


if __name__ == '__main__':
    app.run()
