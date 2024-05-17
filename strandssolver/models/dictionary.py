import os
import json

from typing import Iterable, Callable, Set
from dataclasses import dataclass


@dataclass
class Dictionary:
    words: Iterable[str]
    filter_condition: Callable[[str], bool] = (lambda word: True)

    def __iter__(self) -> Iterable[str]:
        return (word for word in self.words if self.filter_condition(word))

    def drop_filtered_words(self,
                            filter_condition: Callable[[str], bool] = None
                            ) -> None:
        if filter_condition is None:
            filter_condition = self.filter_condition
        self.words = {word for word in self.words
                      if filter_condition(word)}


class DictionaryBuilder:
    @staticmethod
    def load_keys_from_json(path: str | bytes | os.PathLike) -> Set[str]:
        with open(path, 'rb') as f:
            word_dict = json.load(f)
            words = word_dict.keys()
            return words

    @staticmethod
    def build_dictionary_from_json(
            path: str | bytes | os.PathLike,
            filter_condition: Callable[[str], bool] = None
    ) -> Dictionary:
        words = DictionaryBuilder.load_keys_from_json(path)
        dictionary = Dictionary(words, filter_condition)
        return dictionary


def _test() -> None:
    from importlib import resources
    from strandssolver.test import data
    from strandssolver.test.data import filenames
    word_dict_json = resources.files(data).joinpath(filenames.words_dictionary)
    dictionary = DictionaryBuilder.build_dictionary_from_json(
        word_dict_json,
        lambda word:
        len(word) >= 20
    )
    dictionary.drop_filtered_words()
    print(dictionary)
    for word in dictionary.words:
        print(word, end=", ")


if __name__ == "__main__":
    _test()
