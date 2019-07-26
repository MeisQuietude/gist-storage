import uuid


class _Tool:
    @staticmethod
    def gen_id():
        """
        Generates random uuid
        :return: uuid.hex string, length = 32
        """
        return uuid.uuid4().hex

    @staticmethod
    def autoincrement(start=1, increment=1):
        i = start - increment
        while True:
            i += increment
            yield i

    @staticmethod
    def make_link(id_: str, is_public: bool):
        """
        Generate link by id
        :param id_: uuid4().hex, length = 32
        :param is_public: is public gist or not
        :return url string
        """
        return id_[:8] if is_public else id_[8:]