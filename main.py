import networkx as nx
import numpy as np

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
    solution = game_solver.solve()
    for word in solution:
        string = ""
        for node in word:
            string += game_graph.nodes[node]["character"]
        print(string)

    pos = nx.spring_layout(game_graph)
    nx.draw_networkx_nodes(game_graph, pos=pos)
    nx.draw_networkx_labels(game_graph,
                            labels={node: data["character"]
                                    for node, data in
                                    game_graph.nodes(data=True)},
                            pos=pos)
    cm = plt.get_cmap('gist_rainbow')
    colors = (cm(x) for x in np.linspace(0, 1, len(solution)))
    for word, color in zip(solution, colors):
        print(color)
        r, g, b, _ = color
        color = (r, g, b)
        edgelist = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
        nx.draw_networkx_edges(game_graph, edgelist=edgelist, pos=pos,
                               edge_color=color, width=4)
        nx.draw_networkx_nodes(game_graph, nodelist=[word[0]], pos=pos,
                               node_color=color, node_size=200)
    plt.show()


if __name__ == '__main__':
    main()
