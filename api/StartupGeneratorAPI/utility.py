import pathlib

import pymongo

from StartupGeneratorAPI.model.words import WordsDB, WordsTextFile


def add_words_to_db_from_text(
    file_path: pathlib.Path, set_index: int, db_client: pymongo.MongoClient
):
    loader = WordsTextFile(file_path)
    words = WordsDB(db_client.get_default_database())
    for word in loader.words:
        words.add(word, set_index)
