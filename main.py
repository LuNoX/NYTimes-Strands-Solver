import networkx as nx
import sys

from matplotlib import pyplot as plt

from strandssolver.solver import solver
from strandssolver.readers import htmlreader, jsonreader
from strandssolver.parsers import htmlparser, jsonparser
from strandssolver.models import gamestate, graph, dictionarytrie
from strandssolver.test.data import filepaths


def read_game() -> gamestate.GameState | None:
    try:
        json_reader = jsonreader.JSONReader()
        return jsonparser.JSONParser(json_reader=json_reader).parse()
    except Exception as error:
        print(f"Could not load the puzzle from the NYT API "
              f"({describe(error)}), trying the website instead",
              file=sys.stderr)
    try:
        html_reader = htmlreader.HTMLReader()
        return htmlparser.HTMLParser(html_reader=html_reader).parse()
    except Exception as error:
        print(f"Could not load the puzzle from the website "
              f"({describe(error)})", file=sys.stderr)
    return None


def describe(error: Exception) -> str:
    # Selenium appends a stacktrace to its error messages
    first_line = next(iter(str(error).splitlines()), "")
    return f"{type(error).__name__}: {first_line}"


def main() -> None:
    game = read_game()
    if game is None:
        sys.exit("Could not load today's puzzle")
    game_graph = graph.CharacterGraphBuilder.build_graph_from_board(game.board)
    trie = dictionarytrie.DictionaryTrieBuilder.load_trie_from_json(
        filepaths.words_trie_path)

    game_solver = solver.Solver(graph=game_graph, game=game, trie=trie)
    ranked_coverings = game_solver.solve()
    if not ranked_coverings:
        print("No covering found")
        return
    for ranked_covering in ranked_coverings:
        words = [game_solver.spell(word) for word in ranked_covering.covering]
        print(f"{ranked_covering.score:.2f}: {', '.join(words)}")
    solution = ranked_coverings[0].covering

    pos = nx.spring_layout(game_graph)
    nx.draw_networkx_nodes(game_graph, pos=pos)
    nx.draw_networkx_labels(game_graph,
                            labels={node: data["character"]
                                    for node, data in
                                    game_graph.nodes(data=True)},
                            pos=pos)

    for word in solution:
        edgelist = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
        nx.draw_networkx_edges(game_graph, edgelist=edgelist, pos=pos,
                               edge_color="b", width=4)
        nx.draw_networkx_nodes(game_graph, nodelist=[word[0]], pos=pos,
                               node_color="r", node_size=200)
    plt.show()


if __name__ == '__main__':
    main()
