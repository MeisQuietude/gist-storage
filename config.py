SUPPORTED_LANGUAGES = {
    None: {},
    'javascript': {'.js'},
    'python': {'.py'},
    'c++': {'.cpp'},
    'php': {'.myphp'},
    'html': {'.htm', '.html'}
}

# Options
MAX_NUMBER_LINES_PREVIEW = 10
MAX_NUMBER_SYMBOLS_IN_LINE_PREVIEW = 80

NUMBER_GISTS_ON_PAGE = 5
COUNT_VIEW_PAGE_NUMBERS = 3  # +- from current page

MAX_SIZE_UPLOAD_CONTENT_BY_URL = 1024 * 64  # 64kb


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DB_USER = 'gist'
    DB_PASS = 'gist'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = f'postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASS}@localhost:5432/gists'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
