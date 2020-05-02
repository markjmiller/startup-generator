import os
from enum import Enum, auto


class AppVariables(Enum):
    mongo_reader_uri = auto()
    mongo_writer_uri = auto()
    admin_username = auto()
    admin_password = auto()
    flask_secret_key = auto()
    serve_static_from = auto()
    redirect_url = auto()
    redirect_path = auto()
    redirect_s3_bucket_name = auto()
    login_disabled = auto()
    aws_access_key = auto()
    aws_secret_key = auto()


def get_variable(variable: AppVariables, required=True):
    value = os.environ.get(variable.name)
    if required and not value:
        raise ValueError("Could not find environment variable: {}".format(variable))
    if value in ["True", "true"]:
        value = True
    elif value in ["False", "false"]:
        value = False
    return value
