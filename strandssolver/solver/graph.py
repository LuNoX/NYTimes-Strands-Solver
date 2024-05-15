import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from typing import Tuple

from strandssolver import gamestate


class CharacterGraph:
    def __init__(self, board: gamestate.Board) -> None:
        self.board = board
        self.graph = CharacterGraph.generate_graph_from_board(board)

    @staticmethod
    def generate_graph_from_board(board: gamestate.Board) -> nx.Graph:
        graph = CharacterGraph.diagonally_connected_grid_graph(board.shape)

        it = np.nditer(board.characters, flags=['multi_index'])
        node_attributes = {it.multi_index: {"character": str(character)}
                           for character in it}
        nx.set_node_attributes(graph, node_attributes)

        it = np.nditer(board.solved_states, flags=['multi_index'])
        solved_nodes = [it.multi_index for solved in it if solved]
        graph.remove_nodes_from(solved_nodes)

        return graph

    @staticmethod
    def diagonally_connected_grid_graph(shape: Tuple[int, ...]) -> nx.Graph:
        graph = nx.grid_graph(list(reversed(shape)))

        # TODO: diagonals

        return graph


def _test() -> None:
    from test.stubs import stubhtmlreader
    from strandssolver.parsers import htmlparser

    parser = htmlparser.HTMLParser(html_reader=stubhtmlreader.StubHTMLReader())
    game = parser.parse()
    game.board.solved_states[1, 2] = True
    graph = CharacterGraph(game.board)

    pos = nx.spring_layout(graph.graph)
    nx.draw(graph.graph, pos=pos)
    nx.draw_networkx_labels(graph.graph,
                            labels={node[0]: node[1]["character"]
                                    for node in graph.graph.nodes(data=True)},
                            pos=pos)
    plt.show()


if __name__ == "__main__":
    _test()
