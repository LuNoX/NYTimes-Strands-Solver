from importlib import resources

from strandssolver.test import data
from strandssolver.test.data import filenames

strands_html_path = resources.files(data).joinpath(filenames.strands_html)
strands_html_partial_solve_path = resources.files(data).joinpath(
    filenames.strands_html_partial_solve)
words_dictionary_path = resources.files(data).joinpath(
    filenames.words_dictionary)
words_trie_path = resources.files(data).joinpath(filenames.words_trie)
