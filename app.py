from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('gist/create.html')


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
        pass


if __name__ == '__main__':
    app.run()
