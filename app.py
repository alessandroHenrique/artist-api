from flask import Flask
from flask_restful import Api
from .resources.artist import Artist
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    if not test_config:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    api.add_resource(Artist, '/artist')

    return app