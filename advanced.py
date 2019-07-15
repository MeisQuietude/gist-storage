from math import ceil

from config import NUMBER_GISTS_ON_PAGE, MAX_NUMBER_LINES_PREVIEW, MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW


class AdvancedTool:
    @staticmethod
    def get_number_pages(all_gists):
        return ceil(len(all_gists) / NUMBER_GISTS_ON_PAGE)

    @staticmethod
    def get_preview_from_code(code: str):
        lines = code.split('\n')
        if len(lines) > MAX_NUMBER_LINES_PREVIEW:
            lines = lines[:MAX_NUMBER_LINES_PREVIEW]
            lines.append('...')
        return '\n'.join(map(
            lambda line:
            line if len(line) <= MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW
            else line[:MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW - 3] + '...',
            lines))
