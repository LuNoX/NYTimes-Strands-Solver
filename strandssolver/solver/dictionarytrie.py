import pygtrie

from strandssolver.solver.dictionary import Dictionary


class DictionaryTrieBuilder:
    @staticmethod
    def build_trie_from_dictionary(dictionary: Dictionary) -> pygtrie.CharTrie:
        trie = pygtrie.CharTrie()
        for word in dictionary:
            trie[word] = True
        return trie
