import re

from config import SUPPORTED_LANGUAGES


def guess_language_by_shebang(line: str) -> int:
    pattern = re.compile(r"#!/(?:\S+/)+(\S+)")
    matched = pattern.match(line)
    if not matched: return 0

    language = matched.group(1).lower()
    for supp_language in SUPPORTED_LANGUAGES.keys():
        if language == supp_language:
            return list(SUPPORTED_LANGUAGES.keys()).index(language)
    return 0
