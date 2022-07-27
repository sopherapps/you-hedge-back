import json
import os

from flask import Flask

from services import website, auth, youtube

_SERVICE_FOLDER = os.path.dirname(__file__)
_ROOT_FOLDER = os.path.dirname(_SERVICE_FOLDER)


def create_app(config_filename: str = "config.json"):
    """Application factory for creating the Flask app"""
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=_ROOT_FOLDER,
        static_folder=os.path.join(_SERVICE_FOLDER, "website", "static"),
        template_folder=os.path.join(_SERVICE_FOLDER, "website", "templates"),
    )
    app.config.from_file(config_filename, load=json.load)

    app.register_blueprint(website.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(youtube.bp)

    return app
