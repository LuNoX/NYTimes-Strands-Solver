from dataclasses import dataclass
import numpy as np
import numpy.typing
from typing import Tuple


class Board:
    def __init__(self,
                 characters: np.typing.NDArray[np.str_],
                 solved_states: np.typing.NDArray[np.bool_] = None
                 ) -> None:
        self.characters = characters
        if solved_states is None:
            self._solved_states = self._default_solved_states()

    def _default_solved_states(self,
                               shape: Tuple[int, ...] = None
                               ) -> np.typing.NDArray[np.bool_]:
        if shape is None:
            shape = self.characters.shape
        return np.zeros(shape, dtype=bool)


@dataclass
class GameState:
    board: Board
    theme: str
    number_of_total_words: int
    number_of_solved_words: int = 0
