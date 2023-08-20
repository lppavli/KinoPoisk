import os

from elasticsearch import Elasticsearch
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine

from db.models import db

load_dotenv()


def init_db(app: Flask, database:str = None):
    if not database:
        database = os.getenv('POSTGRES_DB')
    app.config["SECRET_KEY"] = "SECRET"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/{database}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()


def create_elasticsearch_connection():
    elasticsearch_url = 'http://elastic:9200'
    return Elasticsearch([elasticsearch_url])


def create_postgresql_connection(database: str = None):
    if not database:
        database = os.getenv('POSTGRES_DB')
    db_engine = create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/{database}"
    )

    return db_engine
