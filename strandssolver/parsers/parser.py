from typing import Protocol

from strandssolver.models import gamestate


class Parser(Protocol):
    def parse(self) -> gamestate.GameState:
        raise NotImplementedError()
