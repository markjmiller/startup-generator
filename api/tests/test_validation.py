from unittest.mock import MagicMock

from StartupGeneratorAPI.model.words import WordsDB
from StartupGeneratorAPI.validation import validate_word_request


def validate_func_factory(request):
    @validate_word_request(request)
    def func():
        return "Success", 200

    return func()


def test_validation_success():
    request = MagicMock()
    request.json = WordsDB.word_schema("test", 0)

    result = validate_func_factory(request)

    assert result[0] == "Success"
    assert result[1] == 200


def test_validation_no_json():
    request = MagicMock()
    request.json = None

    result = validate_func_factory(request)

    assert result[0] == "No json in request"
    assert result[1] == 400


def test_validation_bad():
    request = MagicMock()
    request.json = {"invalid": "invalid"}

    result = validate_func_factory(request)

    assert result[0] != "Success"
    assert result[1] == 400
