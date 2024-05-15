from dataclasses import dataclass
import numpy as np
import numpy.typing
from typing import Tuple, List


class Board:
    DEFAULT_SHAPE = (6, 8)

    def __init__(self,
                 characters: np.typing.NDArray[np.str_],
                 solved_states: np.typing.NDArray[np.bool_] = None,
                 ) -> None:
        self.characters = characters
        self.shape = characters.shape
        if solved_states is None:
            self._solved_states = self._default_solved_states()

    def _default_solved_states(self,
                               shape: Tuple[int, ...] = None
                               ) -> np.typing.NDArray[np.bool_]:
        if shape is None:
            shape = self.characters.shape
        return np.zeros(shape, dtype=bool)

    @classmethod
    def characters_matrix_from_letters(cls, letters: List[str],
                                       shape: Tuple[int, ...] = DEFAULT_SHAPE
                                       ) -> np.ndarray[np.str_]:
        array = np.array(letters)
        characters = array.reshape(shape)
        return characters


@dataclass
class GameState:
    board: Board
    theme: str
    number_of_total_words: int
    number_of_solved_words: int = 0
