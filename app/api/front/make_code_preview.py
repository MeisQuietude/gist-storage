from config import MAX_NUMBER_LINES_PREVIEW, MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW


def make_code_preview(code: str):
    lines = code.split('\n')
    if len(lines) > MAX_NUMBER_LINES_PREVIEW:
        lines = lines[:MAX_NUMBER_LINES_PREVIEW]
        lines.append('...')
    return '\n'.join(map(
        lambda line:
        line if len(line) <= MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW
        else line[:MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW - 3] + '...',
        lines))
