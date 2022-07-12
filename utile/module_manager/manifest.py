try:
    from types import NoneType
except ImportError:
    NoneType = type(None)
import typing
import json
from dataclasses import dataclass


def variable_is_of_one_of_type(variable: typing.Any, types_list: list[typing.Type]):
    for t in types_list:
        if isinstance(variable, t):
            return True
    return False


def type_validator(t: typing.Any, field_max_length: int = None):
    def validate(value: typing.Any):
        if isinstance(t, list):
            def func(x): return variable_is_of_one_of_type(x, t) and (
                (len(x) <= field_max_length) if field_max_length is not None and x is not None else True)
        else:
            def func(x): return type(x) is t and ((len(x) <= field_max_length)
                                                  if field_max_length is not None and x is not None else True)
        return func(value)
    return validate


REQUIRED_FIELDS = ["name", "version"]
FIELDS_VALIDATORS = {
    "name": type_validator(str, 25),
    "version": lambda x: type(x) is str and len(x.split(".")) == 3 and len(x) <= 25,
    "description": type_validator([str, NoneType], 512),
    "tags": lambda x: (isinstance(x, list) and ((type(x[0]) is str) if len(x) > 0 else True) and len(x) <= 15) or type(x) is None,
    "author": type_validator([str, NoneType], 25)
}
FIELDS_DEFAULT_VALUES = {
    "description": lambda: None,
    "tags": lambda: list(),
    "author": lambda: None
}


@dataclass
class ManifestParsingErrorCode:
    INVALID_JSON = 1
    MISSING_FIELD = 2
    INVALID_FIELD_FORMAT = 3


class InvalidManifest(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class Manifest:
    def __init__(self, data: typing.Union[str, dict]):
        self.data: dict = data

        self.name, self.version, self.tags, self.description, self.author = None, None, [], None, None

        if type(data) is str:
            try:
                self.data = json.loads(data)
            except:
                raise InvalidManifest(
                    ManifestParsingErrorCode.INVALID_JSON, "INVALID_JSON")

        # Parsing content
        required_fields = REQUIRED_FIELDS
        for field in required_fields:
            if field not in self.data.keys():
                raise InvalidManifest(
                    ManifestParsingErrorCode.MISSING_FIELD, "MISSING_FIELD: {}"
                    .format(field)
                )

        for field, validator in FIELDS_VALIDATORS.items():
            field_value = self.data.get(
                field, FIELDS_DEFAULT_VALUES.get(field, lambda: None)())
            is_valid = validator(field_value)
            if not is_valid:
                raise InvalidManifest(ManifestParsingErrorCode.INVALID_FIELD_FORMAT,
                                      "INVALID_FIELD_FORMAT: {}".format(field))

            setattr(self, field, field_value)


if __name__ == "__main__":
    example_manifest = {
        "name": "double",
        "version": "0.0.1"
    }
    manifest = Manifest(example_manifest)
    print("Name: {}".format(manifest.name))
    print("Version: {}".format(manifest.version))
