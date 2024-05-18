import os

from importlib import resources
from typing import override

from strandssolver.models import dictionary
from strandssolver.test import data
from strandssolver.test.data import filenames


class StubDictionary(dictionary.Dictionary):
    DEFAULT_DICTIONARY_PATH = resources.files(data).joinpath(
        filenames.words_dictionary)

    @override
    def __init__(self, path: str | bytes | os.PathLike = None) -> None:
        self.filter_condition = lambda word: len(word) >= 1
        if path is None:
            path = StubDictionary.DEFAULT_DICTIONARY_PATH
        self.words = dictionary.DictionaryBuilder.load_keys_from_json(path)
