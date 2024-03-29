from collections import defaultdict, OrderedDict

from app.api.get_all_gists import get_all_gists


def get_language_statistic():
    """
    Collect statistic from snippets by language usage
    :return: sorted by language names dictionary with fractional values
    """
    count = defaultdict(int)  # dictionary {'language': default(0)}
    for gist in get_all_gists():
        for snippet in gist.snippets:
            count[snippet.language] += 1

    total_count = sum(count.values())  # count all snippets
    stats = OrderedDict(sorted(count.items(), key=lambda lang: lang[0].__repr__()))
    for k in stats.keys():
        # get a fractional values (for percent calculating)
        stats[k] = stats[k] / total_count

    return stats
