import networkx as nx

from matplotlib import pyplot as plt

from strandssolver.solver import solver
from strandssolver.readers import htmlreader
from strandssolver.parsers import htmlparser
from strandssolver.models import graph, dictionarytrie
from strandssolver.test.data import filepaths


def main() -> None:
    reader = htmlreader.HTMLReader()
    parser = htmlparser.HTMLParser(html_reader=reader)
    game = parser.parse()
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
