from typing import override

from strandssolver.models import gamestate
from test.stubs import stubhtmlparser


class StubGameState(gamestate.GameState):
    @override
    def __init__(self,
                 board: gamestate.Board = None,
                 theme: str = None,
                 number_of_total_words: int = None,
                 number_of_solved_words: int = None,
                 ) -> None:
        game = stubhtmlparser.StubHTMLParser().parse()
        if board is None:
            board = game.board
        if theme is None:
            theme = game.theme
        if number_of_total_words is None:
            number_of_total_words = game.number_of_total_words
        if number_of_solved_words is None:
            number_of_solved_words = game.number_of_solved_words
        super().__init__(board=board,
                         theme=theme,
                         number_of_total_words=number_of_total_words,
                         number_of_solved_words=number_of_solved_words)
