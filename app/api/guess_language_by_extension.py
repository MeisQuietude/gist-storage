from config import SUPPORTED_LANGUAGES


def guess_language_by_extension(ext: str) -> int:
    """
    Try to get language id by file extension
    :param ext: file extension (like '.ext')
    :return: language_id
    """
    ext = ext.lower()
    for supp_lang, supp_ext in SUPPORTED_LANGUAGES.items():
        if ext in supp_ext:
            return list(SUPPORTED_LANGUAGES.keys()).index(supp_lang)
    return 0
