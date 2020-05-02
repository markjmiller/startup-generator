import json
from pathlib import Path

import bson
import flask_login
from flask import flash, redirect, render_template, request, send_file, url_for
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager, login_required
from flask_pymongo import PyMongo

from StartupGeneratorAPI.application import create_app
from StartupGeneratorAPI.configuration import AppVariables, get_variable
from StartupGeneratorAPI.model.resource import ResourceType, resource_factory
from StartupGeneratorAPI.model.user import User
from StartupGeneratorAPI.model.words import WordsDB
from StartupGeneratorAPI.validation import validate_word_request

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

db_client = PyMongo(app)
admin_db_client = PyMongo(app, uri=get_variable(AppVariables.mongo_writer_uri))

cache = Cache(config={"CACHE_TYPE": "simple"})
cache.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def base():
    return "Startup Idea Generator API"


@app.route("/favicon")
def get_favicon():
    favicon_path = Path(app.config["RESULT_STATIC_PATH"]) / "favicon.ico"
    return send_file(favicon_path)


@app.route("/<path:filename>")
@login_required
def static_path(filename):
    resource_type = get_variable(AppVariables.serve_static_from)
    resource = resource_factory(app.config, ResourceType[resource_type])
    return resource.get(filename)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login", unauthorized=True))


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("admin"))

    if request.method == "POST":
        user = User.authenticate(
            request.form.get("username", None), request.form.get("password", None)
        )

        if not user:
            return render_template("login.html", message="Invalid login")

        flask_login.login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("admin"))

    status_code = 200
    if request.args.get("unauthorized"):
        status_code = 401
    return render_template("login.html"), status_code


@app.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
def admin():
    resource_type = get_variable(AppVariables.serve_static_from)
    resource = resource_factory(app.config, ResourceType[resource_type])
    return resource.get("index.html", cache)


@app.route("/suggestion", methods=["GET"])
def get_suggestion():
    words = WordsDB(db_client.db)
    suggestion = {"word_1": words.get_random(0), "word_2": words.get_random(1)}
    app.logger.debug("Created word pair: {}".format(json.dumps(suggestion)))
    return suggestion


@app.route("/all_words", methods=["GET"])
@login_required
def get_all_words():
    return {"words": list(WordsDB(admin_db_client.db).get_all())}


@app.route("/add", methods=["POST"])
@login_required
@validate_word_request(request)
def add_word():
    words = WordsDB(admin_db_client.db)
    inserted_id = words.add(request.json["word"], request.json["set_index"])
    if inserted_id is None:
        return "Word already exists", 400
    return {"_id": str(inserted_id)}, 201


@app.route("/delete", methods=["DELETE"])
@login_required
@validate_word_request(request)
def delete_word():
    words = WordsDB(admin_db_client.db)
    deleted = words.delete(request.json["word"], int(request.json["set_index"]))
    if not deleted:
        return "Word does not exist", 200
    return "", 204


@app.route("/delete/<_id>", methods=["DELETE"])
@login_required
def delete_word_by_id(_id):
    words = WordsDB(admin_db_client.db)
    try:
        db_id = bson.ObjectId(_id)
    except bson.errors.InvalidId:
        return "ID is bad", 200
    deleted = words.delete_by_id(db_id)
    if not deleted:
        return "ID does not exist", 200
    return "", 204


def main(**kwargs):
    app.config["LOGIN_DISABLED"] = get_variable(
        AppVariables.login_disabled, required=False
    )
    app.run(debug=True, **kwargs)


if __name__ == "__main__":
    main()
