import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import functools
import numpy.typing

from typing import Tuple

from strandssolver.models import gamestate


class CharacterGraphBuilder:

    @staticmethod
    def build_graph_from_board(board: gamestate.Board) -> nx.Graph:
        graph = CharacterGraphBuilder.diagonally_connected_grid_graph(
            board.shape)

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

        for node in graph:
            neighbours = CharacterGraphBuilder.valid_neighbour_indices(
                node, shape, only_diagonals=True)
            edges = [(node, tuple(neighbour)) for neighbour in neighbours]
            graph.add_edges_from(edges)

        return graph

    @staticmethod
    @functools.cache
    def neighbour_index_offsets(shape: Tuple[int, ...],
                                exclude_self: bool = True,
                                only_diagonals: bool = False,
                                ) -> np.typing.NDArray[np.int_]:
        # Adapted from
        # https://stackoverflow.com/questions/34905274/how-to-find-the-neighbors-of-a-cell-in-an-ndarray
        number_of_dims = len(shape)

        # generate an (m, ndims) array containing all strings
        # over the alphabet {0, 1, 2}:
        offset_idx = np.indices((3,) * number_of_dims
                                ).reshape(number_of_dims, -1).T

        # use these to index into np.array([-1, 0, 1]) to get offsets
        offsets = np.r_[-1, 0, 1].take(offset_idx)

        # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
        if exclude_self:
            offsets = offsets[np.any(offsets, 1)]
        if only_diagonals:
            diagonal_mask = (np.sum(np.abs(offsets), axis=1) > 1)
            offsets = offsets[diagonal_mask]

        return offsets

    @staticmethod
    def valid_neighbour_indices(home_index: Tuple[int, ...],
                                shape: Tuple[int, ...],
                                only_diagonals: bool = False,
                                ) -> np.typing.NDArray[np.int_]:
        offsets = CharacterGraphBuilder.neighbour_index_offsets(
            shape, only_diagonals=only_diagonals)
        neighbours: np.typing.NDArray[np.int_] = home_index + offsets

        in_bounds = np.all(
            (neighbours < np.array(shape)) & (neighbours >= 0),
            axis=1
        )
        neighbours = neighbours[in_bounds]

        return neighbours


def _test() -> None:
    from test.stubs import stubhtmlreader
    from strandssolver.parsers import htmlparser
    from timeit import timeit

    parser = htmlparser.HTMLParser(html_reader=stubhtmlreader.StubHTMLReader())
    game = parser.parse()
    game.board.solved_states[[1, 2, 3], [1, 2, 3]] = True

    loop = 1000
    time = timeit(
        lambda: CharacterGraphBuilder.build_graph_from_board(game.board),
        number=loop
    )
    print(time / loop)
    graph = CharacterGraphBuilder.build_graph_from_board(game.board)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos=pos)
    nx.draw_networkx_labels(graph,
                            labels={node: data["character"]
                                    for node, data in graph.nodes(data=True)},
                            pos=pos)
    plt.show()


if __name__ == "__main__":
    _test()
