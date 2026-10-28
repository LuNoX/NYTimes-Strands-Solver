import os
import json
import wordfreq

from typing import Iterable, Iterator, Callable, Set, Optional
from dataclasses import dataclass


@dataclass
class Dictionary:
    words: Iterable[str]
    filter_condition: Callable[[str], bool] = lambda word: True

    def __iter__(self) -> Iterator[str]:
        return (word for word in self.words if self.filter_condition(word))

    def drop_filtered_words(
        self, filter_condition: Optional[Callable[[str], bool]] = None
    ) -> None:
        if filter_condition is None:
            filter_condition = self.filter_condition
        self.words = {word for word in self.words if filter_condition(word)}


class DictionaryBuilder:
    DEFAULT_WORDFREQ_LANGUAGE = "en"
    DEFAULT_MINIMUM_ZIPF_FREQUENCY = 3.0

    @staticmethod
    def load_keys_from_json(path: str | bytes | os.PathLike) -> Set[str]:
        with open(path, "rb") as f:
            word_dict = json.load(f)
            words = word_dict.keys()
            return words

    @staticmethod
    def build_dictionary_from_json(
        path: str | bytes | os.PathLike,
        filter_condition: Optional[Callable[[str], bool]] = None,
    ) -> Dictionary:
        words = DictionaryBuilder.load_keys_from_json(path)
        if filter_condition is None:
            return Dictionary(words)
        return Dictionary(words, filter_condition)

    @staticmethod
    def build_dictionary_from_wordfreq(
        language: Optional[str] = None,
        minimum_zipf_frequency: Optional[float] = None,
        filter_condition: Optional[Callable[[str], bool]] = None,
    ) -> Dictionary:
        if language is None:
            language = DictionaryBuilder.DEFAULT_WORDFREQ_LANGUAGE
        if minimum_zipf_frequency is None:
            minimum_zipf_frequency = DictionaryBuilder.DEFAULT_MINIMUM_ZIPF_FREQUENCY
        words: Set[str] = set()
        for word in wordfreq.iter_wordlist(language):
            if wordfreq.zipf_frequency(word, language) < minimum_zipf_frequency:
                break
            if word.isascii() and word.isalpha():
                words.add(word)
        if filter_condition is None:
            return Dictionary(words)
        return Dictionary(words, filter_condition)


def _test() -> None:
    from strandssolver.test.data import filepaths

    word_dict_json = filepaths.words_dictionary_path
    dictionary = DictionaryBuilder.build_dictionary_from_json(
        word_dict_json, lambda word: len(word) >= 20
    )
    dictionary.drop_filtered_words()
    print(dictionary)
    for word in dictionary.words:
        print(word, end=", ")


if __name__ == "__main__":
    _test()
