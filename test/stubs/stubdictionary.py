import os

from importlib import resources
from typing import override

from strandssolver.models import dictionary
from test import data
from test.data import filenames


class StubDictionary(dictionary.Dictionary):
    DEFAULT_DICTIONARY_PATH = resources.files(data).joinpath(
        filenames.words_dictionary)

    @override
    def __init__(self, path: str | bytes | os.PathLike = None) -> None:
        self.filter_condition = lambda word: len(word) >= 4
        if path is None:
            path = StubDictionary.DEFAULT_DICTIONARY_PATH
        self.words = dictionary.DictionaryBuilder.load_keys_from_json(path)
