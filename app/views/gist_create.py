from flask import render_template


def create_gist():
    return render_template('gist/create.html')
