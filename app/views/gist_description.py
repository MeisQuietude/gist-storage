from flask import render_template

from app.api.get_gist_by_id import get_gist


def gist_description(link):
    gist = get_gist(link)
    if gist is None:
        return render_template('gist/description.html', errors=["Gist not found"])
    return render_template('gist/description.html', gist=gist)


if __name__ == '__main__':
    print(get_gist('523532'))
