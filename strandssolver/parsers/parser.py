from typing import Protocol

from strandssolver import gamestate


class Parser(Protocol):
    def parse(self) -> gamestate.GameState:
        raise NotImplementedError()
