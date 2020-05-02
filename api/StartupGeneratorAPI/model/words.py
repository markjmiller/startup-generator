import pathlib
import random
import re

import bson
from pymongo.errors import DuplicateKeyError


class WordsDB(object):
    def __init__(self, db, db_name="app"):
        assert db.name == db_name
        self._words = db["words"]

    def get_all(self):
        return map(
            lambda document: self.document_schema(document), self._words.find({})
        )

    def get_random(self, set_index: int):
        documents = self._words.aggregate(
            [{"$match": {"set_index": set_index}}, {"$sample": {"size": 1}}]
        )
        for document in documents:
            return document["word"]

    def add(self, word: str, set_index: int):
        try:
            result = self._words.insert_one(self.word_schema(word, set_index))
        except DuplicateKeyError:
            return None
        return result.inserted_id

    def delete(self, word: str, set_index: int) -> bool:
        result = self._words.delete_one(self.word_schema(word, set_index))
        return result.deleted_count > 0

    def delete_by_id(self, _id: bson.ObjectId) -> bool:
        result = self._words.delete_one({"_id": _id})
        return result.deleted_count > 0

    @staticmethod
    def word_schema(word, set_index):
        return {"word": word, "set_index": set_index}

    @staticmethod
    def document_schema(document):
        return {
            "_id": str(document["_id"]),
            **WordsDB.word_schema(document["word"], document["set_index"]),
        }


class WordsTextFile(object):
    def __init__(self, file_path: pathlib.Path):

        if file_path is None:
            raise ValueError("file_path is None")

        self._words = []
        self._file_path = file_path

        self._load()

    def _load(self):
        with open(str(self._file_path), "r") as file:
            for line in file:
                line = line.rstrip()
                if not line:
                    continue
                word_match = re.search(r"^[\w\-\s]+$", line)
                if word_match:
                    self._words.append(word_match.group(0))
                else:
                    raise ValueError("Bad value: {}".format(line))

        if not len(self._words):
            raise ValueError("No words were found.")

    @property
    def words(self):
        for word in self._words:
            yield word

    @property
    def random(self):
        return random.choice(self._words)
