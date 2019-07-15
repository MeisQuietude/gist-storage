from math import ceil

from config import NUMBER_GISTS_ON_PAGE, MAX_NUMBER_LINES_PREVIEW, MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW, \
    COUNT_VIEW_PAGE_NUMBERS


class AdvancedTool:
    @staticmethod
    def get_last_page_number(all_gists):
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

    @staticmethod
    def get_page_numbers(i, last_page, count=COUNT_VIEW_PAGE_NUMBERS):
        numbers = []
        if i > count:
            numbers.append('...')
        numbers = [*numbers, *[page for page in range(i - count, i + count + 1) if 1 < page < last_page]]
        if last_page - i > count:
            numbers.append('...')
        return numbers
