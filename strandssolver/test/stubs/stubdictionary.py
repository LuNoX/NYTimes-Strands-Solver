import os

from typing import Optional

from strandssolver.models import dictionary
from strandssolver.test.data import filepaths


class StubDictionary(dictionary.Dictionary):
    DEFAULT_DICTIONARY_PATH = filepaths.words_dictionary_path

    def __init__(self, path: Optional[str | bytes | os.PathLike] = None) -> None:
        self.filter_condition = lambda word: len(word) >= 1
        if path is None:
            path = StubDictionary.DEFAULT_DICTIONARY_PATH
        self.words = dictionary.DictionaryBuilder.load_keys_from_json(path)
