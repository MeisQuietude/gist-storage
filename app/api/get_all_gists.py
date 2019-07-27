from app.models.gist import Gist


def get_all_gists(are_public=True):
    """
    Get all public (by default) gists
    :param are_public: True or False
    :return: Gist Query
    """
    return Gist.query.filter(Gist.is_public == are_public).all()
