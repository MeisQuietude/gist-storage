from config import COUNT_VIEW_PAGE_NUMBERS


def get_navigation_page_numbers(i, last_page, count=COUNT_VIEW_PAGE_NUMBERS):
    numbers = []
    if last_page <= 1:
        return numbers
    if i > count:
        numbers.append('...')
    numbers = [*numbers, *[page for page in range(i - count, i + count + 1) if 1 < page < last_page]]
    if last_page - i > count:
        numbers.append('...')
    return numbers
