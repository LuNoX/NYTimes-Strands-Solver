import networkx as nx
import more_itertools
import pygtrie
import sys

from typing import Optional

from matplotlib import pyplot as plt

from strandssolver.solver import rankcovering, solver
from strandssolver.readers import htmlreader, jsonreader
from strandssolver.parsers import htmlparser, jsonparser
from strandssolver.models import gamestate, graph, dictionary, dictionarytrie
from strandssolver.test.data import filepaths

MINIMUM_WORD_LENGTH = 4


def read_game() -> Optional[gamestate.GameState]:
    try:
        json_reader = jsonreader.JSONReader()
        return jsonparser.JSONParser(json_reader=json_reader).parse()
    except Exception as error:
        print(
            f"Could not load the puzzle from the NYT API "
            f"({describe(error)}), trying the website instead",
            file=sys.stderr,
        )
    try:
        html_reader = htmlreader.HTMLReader()
        return htmlparser.HTMLParser(html_reader=html_reader).parse()
    except Exception as error:
        print(
            f"Could not load the puzzle from the website ({describe(error)})",
            file=sys.stderr,
        )
    return None


def describe(error: Exception) -> str:
    # Selenium appends a stacktrace to its error messages
    first_line = next(iter(str(error).splitlines()), "")
    return f"{type(error).__name__}: {first_line}"


def load_trie() -> pygtrie.Trie:
    minimum_zipf_frequency = dictionary.DictionaryBuilder.DEFAULT_MINIMUM_ZIPF_FREQUENCY
    cache_path = filepaths.data_directory / (
        f"words_trie_cache_zipf{minimum_zipf_frequency}_min{MINIMUM_WORD_LENGTH}.json"
    )

    def build_trie() -> pygtrie.Trie:
        trie = dictionarytrie.DictionaryTrieBuilder.load_trie_from_json(
            filepaths.words_trie_path, cast_to=pygtrie.CharTrie
        )
        common_words = dictionary.DictionaryBuilder.build_dictionary_from_wordfreq(
            minimum_zipf_frequency=minimum_zipf_frequency,
            filter_condition=lambda word: len(word) >= MINIMUM_WORD_LENGTH,
        )
        dictionarytrie.DictionaryTrieBuilder.add_dictionary_to_trie(trie, common_words)
        return trie

    return dictionarytrie.DictionaryTrieBuilder.load_or_build_trie(
        cache_path, build_trie
    )


def main() -> None:
    game = read_game()
    if game is None:
        sys.exit("Could not load today's puzzle")
    game_graph = graph.CharacterGraphBuilder.build_graph_from_board(game.board)
    trie = load_trie()

    game_solver = solver.Solver(graph=game_graph, game=game, trie=trie)
    ranked_coverings = game_solver.solve()
    if not ranked_coverings:
        print("Could not find a solution! You'll have to try this one yourself :(")
        return
    print(f"Todays's puzzle: {game.theme}")
    print("Found the following solution(s):")
    max_score = rankcovering.CoveringRanker().max_score
    for ranked_covering in ranked_coverings:
        words = [game_solver.spell(word) for word in ranked_covering.covering]
        print(
            f"{', '.join(words)} with confidence {ranked_covering.score / max_score:.2f}/1.00"
        )
    solution = ranked_coverings[0].covering

    plt.figure("StrandsSolver")
    pos = {(row, column): (column, -row) for row, column in game_graph.nodes}
    nx.draw_networkx_nodes(game_graph, pos=pos)
    nx.draw_networkx_labels(
        game_graph,
        labels={node: data["character"] for node, data in game_graph.nodes(data=True)},
        pos=pos,
        verticalalignment="center_baseline",
    )

    for word in solution:
        edgelist = list(more_itertools.pairwise(word))
        nx.draw_networkx_edges(
            game_graph, edgelist=edgelist, pos=pos, edge_color="b", width=4
        )
        nx.draw_networkx_nodes(
            game_graph, nodelist=[word[0]], pos=pos, node_color="r", node_size=200
        )
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.title(f"{game.theme}")
    plt.show()


if __name__ == "__main__":
    main()
