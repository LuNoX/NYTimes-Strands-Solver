import networkx as nx
import numpy as np
import numpy.typing
from typing import Tuple
from functools import cache

from strandssolver import gamestate


class CharacterGraph:
    def __init__(self, board: gamestate.Board) -> None:
        self.board = board
        self.graph = CharacterGraph.generate_graph_from_board(board)

    @staticmethod
    def generate_graph_from_board(board: gamestate.Board) -> nx.Graph:
        graph = nx.Graph()

        it = np.nditer(board.characters, flags=['multi_index'])
        for character in it:
            graph.add_node(it.multi_index, character=character)

        it.reset()
        for _ in it:
            neighbours = CharacterGraph.valid_neighbour_indices(it.multi_index,
                                                                board.shape)
            edges = [(it.multi_index, tuple(neighbour)) for neighbour in
                     neighbours]
            graph.add_edges_from(edges)

        print(graph)
        return graph

    @staticmethod
    @cache
    def neighbour_index_offsets(shape: Tuple[int, ...],
                                exclude_self: bool = True
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

        return offsets

    @staticmethod
    def valid_neighbour_indices(home_index: Tuple[int, ...],
                                shape: Tuple[int, ...],
                                ) -> np.typing.NDArray[np.int_]:
        offsets = CharacterGraph.neighbour_index_offsets(shape)
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

    parser = htmlparser.HTMLParser(html_reader=stubhtmlreader.StubHTMLReader())
    game = parser.parse()
    graph = CharacterGraph(game.board)

    grid = nx.grid_graph(game.board.shape)
    print(grid)


if __name__ == "__main__":
    _test()
