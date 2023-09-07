import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from fastapi.testclient import TestClient

from src.database import DATABASE_URL, Base
from src.main import app


@pytest.fixture(scope='session')
def engine():
    global engine  # noqa
    engine = create_engine(DATABASE_URL + '_test', future=True)
    if len(Base.metadata.sorted_tables) and not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='session')
def session(engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    session.begin()
    try:
        yield session
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()
        session.rollback()
        drop_database(engine.url)


@pytest.fixture(scope='session')
def client(session):
    app.dependency_overrides['get_session'] = session
    return TestClient(app)
