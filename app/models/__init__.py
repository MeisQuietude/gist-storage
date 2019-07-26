from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from app import app, db
from config import DevelopmentConfig, SUPPORTED_LANGUAGES
from app.models.language import Language


def create_itself():
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
        with app.app_context():
            db.create_all()
            db.session.commit()

        _fill_language_column()


def _fill_language_column():
    with app.app_context():
        for supported_language in SUPPORTED_LANGUAGES:
            db.session.add(Language(supported_language))
        db.session.commit()
