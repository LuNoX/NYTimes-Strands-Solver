import os
import pygtrie

from typing import Type, override
from importlib import resources

from strandssolver.models import dictionarytrie
from strandssolver.models.dictionary import Dictionary
from strandssolver.test import data
from strandssolver.test.data import filenames
from strandssolver.test.stubs import stubdictionary


class StubDictionaryTrieBuilder(dictionarytrie.DictionaryTrieBuilder):
    DEFAULT_TRIE_PATH = resources.files(data).joinpath(filenames.words_trie)

    @staticmethod
    @override
    def build_trie_from_dictionary(dictionary: Dictionary = None
                                   ) -> pygtrie.CharTrie:
        if dictionary is None:
            dictionary = stubdictionary.StubDictionary()
        return super().build_trie_from_dictionary(dictionary)

    @staticmethod
    @override
    def load_trie_from_json(path: str | bytes | os.PathLike = None,
                            encoding: str = None,
                            cast_to: Type[pygtrie.Trie] = pygtrie.CharTrie
                            ) -> pygtrie.Trie:
        if path is None:
            path = StubDictionaryTrieBuilder.DEFAULT_TRIE_PATH
        return super(
            StubDictionaryTrieBuilder, StubDictionaryTrieBuilder
        ).load_trie_from_json(path, encoding=encoding, cast_to=cast_to)

    @staticmethod
    @override
    def store_trie_as_json(trie: pygtrie.Trie = None,
                           path: str | bytes | os.PathLike = None,
                           encoding: str = None,
                           ensure_ascii: bool = None,
                           indent: int = None
                           ) -> None:
        """
        Stub method
        """
        pass
