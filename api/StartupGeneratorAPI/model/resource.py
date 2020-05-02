import abc
import pathlib
from enum import Enum, auto

import boto3
import botocore.exceptions
from flask import redirect, send_file
from flask_caching import Cache

from StartupGeneratorAPI.configuration import AppVariables, get_variable


class ResourceType(Enum):
    file = auto()
    s3 = auto()
    redirect = auto()


def resource_factory(config, resource_type: ResourceType):
    if resource_type.name == ResourceType.file.name:
        return FileResource(config)
    if resource_type.name == ResourceType.s3.name:
        return S3Resource()
    if resource_type.name == ResourceType.redirect.name:
        return RedirectResource()
    raise ValueError("Invalid resource type: {}".format(resource_type.name))


class Resource(object):
    @abc.abstractmethod
    def get(self, name: str, cache: Cache = None):
        pass


class FileResource(Resource):
    def __init__(self, config):
        path = get_variable(AppVariables.redirect_path, required=False)
        self._path = (
            pathlib.Path(path) if path else pathlib.Path(config["RESULT_STATIC_PATH"])
        )
        if not self._path.is_dir():
            raise FileNotFoundError("Directory not found: {}".format(self._path))

    def get(self, name: str, cache: Cache = None):
        path = self._path / name
        if not path.is_file():
            return 404, "Resource not found: {}".format(name)
        return send_file(str(path))


class S3Resource(Resource):
    def __init__(self):
        self._bucket_name = get_variable(AppVariables.redirect_s3_bucket_name)

        access_key = get_variable(AppVariables.aws_access_key)
        secret_key = get_variable(AppVariables.aws_secret_key)
        self._client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

    def get(self, name: str, cache: Cache = None):
        try:
            obj = self._client.get_object(Bucket=self._bucket_name, Key=name)
        except botocore.exceptions.ClientError:
            return "File not found", 404

        last_modified = obj["LastModified"]
        if not cache:
            return send_file(
                obj["Body"], attachment_filename=name, last_modified=last_modified
            )

        cached_obj = cache.get(name)
        if cached_obj:
            if last_modified > cached_obj["LastModified"]:
                return self._set_cache(cache, name, obj, last_modified)
            return cached_obj["contents"]
        return self._set_cache(cache, name, obj, last_modified)

    @staticmethod
    def _set_cache(cache, name, obj, last_modified):
        contents = obj["Body"].read().decode("utf-8")
        cache.set(name, S3Resource._cache_factory("name", contents, last_modified))
        return contents

    @staticmethod
    def _cache_factory(name: str, contents: str, last_modified):
        return {"name": name, "contents": contents, "LastModified": last_modified}


class RedirectResource(Resource):
    def __init__(self):
        url = get_variable(AppVariables.redirect_url, required=False)
        self._url = url if url else "http://localhost:4200"

    def get(self, name: str, cache: Cache = None):
        return redirect(self._url)
