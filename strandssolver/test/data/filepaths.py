import pathlib

from strandssolver.test.data import filenames

data_directory = pathlib.Path(__file__).parent

strands_html_path = data_directory / filenames.strands_html
strands_html_partial_solve_path = data_directory / filenames.strands_html_partial_solve
words_dictionary_path = data_directory / filenames.words_dictionary
words_trie_path = data_directory / filenames.words_trie
