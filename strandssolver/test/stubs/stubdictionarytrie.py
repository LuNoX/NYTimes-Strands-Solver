import os
import pygtrie

from typing import Type, override, Optional

from strandssolver.models import dictionarytrie
from strandssolver.models.dictionary import Dictionary
from strandssolver.test.data import filepaths
from strandssolver.test.stubs import stubdictionary


class StubDictionaryTrieBuilder(dictionarytrie.DictionaryTrieBuilder):
    DEFAULT_TRIE_PATH = filepaths.words_trie_path

    @staticmethod
    @override
    def build_trie_from_dictionary(
        dictionary: Optional[Dictionary] = None,
    ) -> pygtrie.CharTrie:
        if dictionary is None:
            dictionary = stubdictionary.StubDictionary()
        return super(
            StubDictionaryTrieBuilder, StubDictionaryTrieBuilder
        ).build_trie_from_dictionary(dictionary)

    @staticmethod
    @override
    def load_trie_from_json(
        path: Optional[str | bytes | os.PathLike] = None,
        encoding: Optional[str] = None,
        cast_to: Type[pygtrie.Trie] = pygtrie.CharTrie,
    ) -> pygtrie.Trie:
        if path is None:
            path = StubDictionaryTrieBuilder.DEFAULT_TRIE_PATH
        return super(
            StubDictionaryTrieBuilder, StubDictionaryTrieBuilder
        ).load_trie_from_json(path, encoding=encoding, cast_to=cast_to)

    @staticmethod
    @override
    def store_trie_as_json(
        trie: Optional[pygtrie.Trie] = None,
        path: Optional[str | bytes | os.PathLike] = None,
        encoding: Optional[str] = None,
        ensure_ascii: Optional[bool] = None,
        indent: Optional[int] = None,
    ) -> None:
        """
        Stub method
        """
        pass


def _test() -> None:
    trie = StubDictionaryTrieBuilder.build_trie_from_dictionary()
    trie_json = StubDictionaryTrieBuilder.load_trie_from_json()
    print(trie_json == trie)
    trie_json["blubbasbbsjhsjuhjksh"] = True
    print(trie_json == trie)


if __name__ == "__main__":
    _test()
