from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from resources.artist import Artist
from resources.dynamo import Dynamo
from decouple import config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    api = Api(app)

    if not test_config:
        app.config.from_mapping(
            SECRET_KEY=config("SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    api.add_resource(Artist, '/artist')
    api.add_resource(Dynamo, '/create-table')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)
