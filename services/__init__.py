import json
import os
from logging import Logger

from flask import Flask
from flask_cors import CORS
from pydantic import ValidationError

from services import website, auth, youtube
from utils.cache import Cache
from utils.exc import APIException
from utils.logging import initialize_logger

_SERVICE_FOLDER = os.path.dirname(os.path.abspath(__file__))
_ROOT_FOLDER = os.path.dirname(_SERVICE_FOLDER)


def create_app(config_filename: str = "config.json", should_log_err_to_file: bool = True):
    """Application factory for creating the Flask app"""
    err_logger = initialize_logger(name="error", should_log_to_file=should_log_err_to_file)
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=_ROOT_FOLDER,
        static_folder=os.path.join(_SERVICE_FOLDER, "website", "static"),
        template_folder=os.path.join(_SERVICE_FOLDER, "website", "templates"),
    )
    app.config.from_file(config_filename, load=json.load)
    app.config.from_mapping({
        "ERROR_LOGGER": err_logger,
        "CACHE": Cache(ttl=app.config["CACHE_TTL_IN_SECONDS"]),
    })
    CORS(app)

    app.register_blueprint(website.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(youtube.bp)

    @app.errorhandler(APIException)
    def api_exception(e: APIException):
        lg: Logger = app.config.get("ERROR_LOGGER", None)
        lg.error(str(e))
        return app.response_class(e.bjson(), status=e.status_code)

    @app.errorhandler(ValidationError)
    def validation_error(e: ValidationError):
        lg: Logger = app.config.get("ERROR_LOGGER", None)
        lg.error(str(e))
        return app.response_class(e.json(), status=500)

    return app
