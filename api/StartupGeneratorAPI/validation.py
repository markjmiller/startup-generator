from functools import update_wrapper

from jsonschema import ValidationError, validate

word_schema = {
    "type": "object",
    "properties": {
        "word": {"type": "string"},
        "set_index": {"type": "number"},
    },
    "required": ["word", "set_index"],
}


def validate_word_request(request):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            if not request.json:
                return "No json in request", 400
            try:
                validate(instance=request.json, schema=word_schema)
            except ValidationError as e:
                return e.message, 400
            return fn(*args, **kwargs)

        return update_wrapper(wrapped_function, fn)

    return decorator
