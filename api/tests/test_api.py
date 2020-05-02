"""API tests

Requires the local mongodb instance to be running.
Ignored by tox.
"""

import logging
import re
from multiprocessing import Process

import bson
import pymongo
import pytest
import requests

from StartupGeneratorAPI.configuration import AppVariables, get_variable
from StartupGeneratorAPI.model.words import WordsDB

logger = logging.getLogger(__name__)

base_uri = "http://localhost:5000/"
mongo_uri = get_variable(AppVariables.mongo_writer_uri)


def start_server():
    from StartupGeneratorAPI.routes import main as run_debug_api

    run_debug_api(use_reloader=False)


def _reset_db():
    client = pymongo.MongoClient(mongo_uri)
    collection = client["app"]["words"]
    regx = re.compile(r"^__test__", re.IGNORECASE)
    result = collection.delete_many({"word": regx})
    logger.info("Cleaned up {} test documents.".format(result.deleted_count))
    return client


@pytest.fixture(autouse=True, scope="function")
def setup_db_func():
    client = _reset_db()

    def add_word(word: str, set_index: int):
        words = WordsDB(client["app"])
        return words.add(word, set_index)

    return add_word


@pytest.fixture(autouse=True, scope="module")
def start_api():
    server = Process(target=start_server)
    server.start()
    r = requests.get(base_uri, timeout=30)
    if r.status_code != 200:
        raise EnvironmentError("Could not start debug server.")
    yield
    server.terminate()
    server.join()
    _reset_db()


def test_get_suggestion():
    r = requests.get(base_uri + "suggestion")
    logger.info(r.text)

    assert r.status_code == 200


def test_add_word():
    word = WordsDB.word_schema("__test__NewWord", 0)

    r = requests.post(base_uri + "add", json=word)
    logger.info(r.text)

    assert r.status_code == 201


def test_add_word_duplicate(setup_db_func):
    word = WordsDB.word_schema("__test__NewWord", 0)
    setup_db_func(word["word"], word["set_index"])

    r = requests.post(base_uri + "add", json=word)
    logger.info(r.text)

    assert r.status_code == 400
    assert r.text == "Word already exists"


def test_delete_word(setup_db_func):
    word = WordsDB.word_schema("__test__DeleteWord", 0)
    setup_db_func(word["word"], word["set_index"])

    r = requests.delete(base_uri + "delete", json=word)
    logger.info(r.text)

    assert r.status_code == 204


def test_delete_word_does_not_exist():
    word = WordsDB.word_schema("__test__DoesNotExist", 0)

    r = requests.delete(base_uri + "delete", json=word)
    logger.info(r.text)

    assert r.status_code == 200
    assert r.text == "Word does not exist"


def test_delete_word_by_id(setup_db_func):
    word = WordsDB.word_schema("__test__DeleteWord", 0)
    db_id = setup_db_func(word["word"], word["set_index"])

    r = requests.delete(base_uri + "delete/{}".format(db_id))
    logger.info(r.text)

    assert r.status_code == 204


def test_delete_word_by_id_does_not_exist(setup_db_func):
    bad_id = bson.ObjectId("000000000000000000000000")
    r = requests.delete(base_uri + "delete/{}".format(bad_id))
    logger.info(r.text)

    assert r.status_code == 200
    assert r.text == "ID does not exist"


def test_delete_word_by_id_is_bad(setup_db_func):
    r = requests.delete(base_uri + "delete/0")
    logger.info(r.text)

    assert r.status_code == 200
    assert r.text == "ID is bad"
