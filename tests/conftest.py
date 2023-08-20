import sys
import os
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from app import create_app
from db.db import create_postgresql_connection, create_elasticsearch_connection
from db.db import init_db


@pytest.fixture
def app():
    app = create_app(database='test_db')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def elasticsearch_connection():
    connection = create_elasticsearch_connection()
    yield connection


@pytest.fixture
def test_db(app):
    # init_db(app, database='test_db')
    test_db_engine = create_postgresql_connection(database='test_db')
    app.db_engine = test_db_engine
    yield test_db_engine
    test_db_engine.dispose()
