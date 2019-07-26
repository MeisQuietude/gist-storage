from app.models.gist import Gist


def get_gist(id_) -> Gist or None:
    """
    :param id_: id_ (len:32), public link (len:8), private link (len:24)
    :return: object (type 'Gist') or None
    """
    try:
        assert id_ is not None

        id_length = len(id_)
        if id_length == 32:
            # Full id\link ( developer case )
            result = Gist.query.filter(Gist.id_ == id_).first()
        elif id_length == 24:
            # Private link
            result = Gist.query.filter(Gist.id_.endswith(id_)).first()
        elif id_length == 8:
            # Public link
            result = Gist.query.filter(Gist.id_.startswith(id_)).first()
        else:
            raise AssertionError
        return result
    except AssertionError:
        return None
