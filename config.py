POSTGRES_DATABASE_URL: str = 'postgresql://root:toor@localhost:5432/gists'
SUPPORTED_LANGUAGES = {
    None: {},
    'javascript': {'.js'},
    'python': {'.py'},
    'c++': {'.cpp'},
    'php': {'.myphp'},
    'html': {'htm', 'html'}
}

# Options
MAX_NUMBER_LINES_PREVIEW = 10
MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW = 80

NUMBER_GISTS_ON_PAGE = 5
COUNT_VIEW_PAGE_NUMBERS = 3  # +- from current page
