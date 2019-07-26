from collections import defaultdict, OrderedDict

from app.models.gist import Gist


def get_language_statistic():
    count = defaultdict(int)
    for gist in Gist.query.filter(Gist.is_public):
        for snippet in gist.snippets:
            count[snippet.language] += 1

    total_count = sum(count.values())
    stats = OrderedDict(sorted(count.items(), key=lambda lang: lang[0].__repr__()))
    for k in stats.keys():
        # get a percent values
        stats[k] = stats[k] / total_count

    return stats
