import unittest

import bson
import mongomock
import pymongo
import pytest

from StartupGeneratorAPI.model.words import WordsDB


def setup_documents():
    return [
        {
            "_id": bson.ObjectId("5ec85f1c173751c1857134b9"),
            "word": "Facebook",
            "set_index": 0,
        },
        {
            "_id": bson.ObjectId("5ec85f1c173751c1857134ba"),
            "word": "barbers",
            "set_index": 1,
        },
    ]


def setup_db():
    client = mongomock.MongoClient()
    for document in setup_documents():
        client.db["words"].insert_one(document)
    client.db["words"].create_index(
        [("word", pymongo.ASCENDING), ("set_index", pymongo.ASCENDING)], unique=True
    )
    return client.db


@pytest.fixture
def setup_words():
    db = setup_db()
    return WordsDB(db, db_name="db")


def test_get_all(setup_words):
    unittest.TestCase().assertCountEqual(
        list(map(lambda x: x["word"], setup_words.get_all())),
        list(map(lambda x: x["word"], setup_documents())),
    )


def test_get_random(setup_words):
    assert setup_words.get_random(0) == "Facebook"
    assert setup_words.get_random(1) == "barbers"


def test_add(setup_words):
    assert isinstance(setup_words.add("test", 0), bson.objectid.ObjectId)


def test_add_if_duplicate_should_return_none(setup_words):
    assert setup_words.add("Facebook", 0) is None


def test_delete(setup_words):
    assert setup_words.delete("Facebook", 0)


def test_delete_by_id(setup_words):
    assert setup_words.delete_by_id(bson.ObjectId("5ec85f1c173751c1857134b9"))
    assert not setup_words.delete_by_id(bson.ObjectId("5ec85f1c173751c1857134b9"))


def test_deleted_if_does_not_exist(setup_words):
    assert not setup_words.delete("Booper", 0)
