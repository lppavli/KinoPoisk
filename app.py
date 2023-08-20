from elasticsearch import Elasticsearch
from flask import Flask
# from flasgger import Swagger

from api import movie
from db.db import init_db


def create_app(database:str = None):
    app = Flask(__name__)
    app.elasticsearch = Elasticsearch(
        hosts=["http://localhost:9200"],
        timeout=30
    )
    app.register_blueprint(movie.route)
    init_db(app, database)
    return app