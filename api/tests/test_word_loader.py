import pathlib

import pytest

from StartupGeneratorAPI.model.words import WordsTextFile


@pytest.fixture
def setup_data_paths():
    data_folder = pathlib.Path(__file__).parent / "data"
    return {
        "word_set_1": data_folder / "word_set_1.txt",
        "word_set_2": data_folder / "word_set_2.txt",
        "empty": data_folder / "empty.txt",
        "bad": data_folder / "bad.txt",
    }


def test_text_word_loader_should_load_from_file(setup_data_paths):
    loader = WordsTextFile(setup_data_paths["word_set_1"])
    words_iter = loader.words

    assert next(words_iter) == "Tesla"
    assert next(words_iter) == "Facebook"


def test_text_word_loader_should_raise_if_file_empty(setup_data_paths):
    with pytest.raises(ValueError):
        WordsTextFile(setup_data_paths["empty"])


def test_text_word_loader_should_raise_if_bad_name(setup_data_paths):
    with pytest.raises(ValueError):
        WordsTextFile(setup_data_paths["bad"])
