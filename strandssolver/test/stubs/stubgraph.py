import networkx as nx

from typing import override

from strandssolver.test.stubs import stubgamestate
from strandssolver.models import graph, gamestate


class StubGraphBuilder(graph.CharacterGraphBuilder):

    @staticmethod
    @override
    def build_graph_from_board(board: gamestate.Board = None) -> nx.Graph:
        if board is None:
            game = stubgamestate.StubGameState()
            game.board.solved_states[[1, 2, 3], [1, 2, 3]] = True
            board = game.board
        return super(StubGraphBuilder, StubGraphBuilder
                     ).build_graph_from_board(board)

    @staticmethod
    def build_small_graph() -> nx.Graph:
        game = stubgamestate.StubSmallGameState()
        return StubGraphBuilder.build_graph_from_board(game.board)
