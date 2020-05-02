import os

from flask import Flask

from StartupGeneratorAPI.configuration import AppVariables, get_variable


def create_app():
    static_dir = os.path.dirname(os.path.dirname(__file__)) + "/static"
    app = Flask(__name__, template_folder=static_dir)
    app.config["RESULT_STATIC_PATH"] = static_dir
    app.config["MONGO_URI"] = get_variable(AppVariables.mongo_reader_uri)
    app.secret_key = get_variable(AppVariables.flask_secret_key)
    return app
