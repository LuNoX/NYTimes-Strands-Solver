from typing import Protocol

from strandssolver import gamestate


class Reader(Protocol):
    @staticmethod
    def read() -> gamestate.GameState:
        raise NotImplementedError()
