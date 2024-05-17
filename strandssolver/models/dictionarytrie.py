import pygtrie
import os
import json

from typing import Type

from strandssolver.models.dictionary import Dictionary


class DictionaryTrieBuilder:
    DEFAULT_JSON_ENCODING = 'utf-8'
    DEFAULT_ENSURE_JSON_IS_ASCII = False
    DEFAULT_JSON_INDENTATION = 4

    @staticmethod
    def build_trie_from_dictionary(dictionary: Dictionary) -> pygtrie.CharTrie:
        trie = pygtrie.CharTrie()
        for word in dictionary:
            trie[word] = True
        return trie

    @staticmethod
    def store_trie_as_json(trie: pygtrie.Trie,
                           path: str | bytes | os.PathLike,
                           encoding: str = None,
                           ensure_ascii: bool = None,
                           indent: int = None
                           ) -> None:
        if encoding is None:
            encoding = DictionaryTrieBuilder.DEFAULT_JSON_ENCODING
        if ensure_ascii is None:
            ensure_ascii = DictionaryTrieBuilder.DEFAULT_ENSURE_JSON_IS_ASCII
        if indent is None:
            indent = DictionaryTrieBuilder.DEFAULT_JSON_INDENTATION

        with open(path, 'w', encoding=encoding) as f:
            json.dump(dict(trie), f, ensure_ascii=ensure_ascii, indent=indent)

    @staticmethod
    def load_trie_from_json(path: str | bytes | os.PathLike,
                            encoding: str = DEFAULT_JSON_ENCODING,
                            cast_to: Type[pygtrie.Trie] = pygtrie.Trie
                            ) -> pygtrie.Trie:
        with open(path, 'r', encoding=encoding) as f:
            trie_dict = json.load(f)
            return cast_to(trie_dict)


def _test() -> None:
    from strandssolver.test.stubs import stubdictionary
    dictionary = stubdictionary.StubDictionary()
    trie = DictionaryTrieBuilder.build_trie_from_dictionary(dictionary)
    print(trie)


if __name__ == "__main__":
    _test()
