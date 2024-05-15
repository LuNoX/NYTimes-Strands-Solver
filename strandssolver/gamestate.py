from dataclasses import dataclass
import numpy as np
import numpy.typing
from typing import Tuple, List


class Board:
    DEFAULT_SHAPE = (8, 6)

    def __init__(self,
                 characters: np.typing.NDArray[np.str_],
                 solved_states: np.typing.NDArray[np.bool_] = None,
                 partially_solved: bool = True
                 ) -> None:
        self.characters = characters
        if solved_states is None:
            solved_states = self._default_solved_states()
            partially_solved = False
        self.solved_states = solved_states
        self.partially_solved = partially_solved

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.characters.shape

    def _default_solved_states(self) -> np.typing.NDArray[np.bool_]:
        return np.zeros(self.shape, dtype=bool)

    @classmethod
    def characters_matrix_from_letters(cls, letters: List[str],
                                       shape: Tuple[int, ...] = DEFAULT_SHAPE
                                       ) -> np.typing.NDArray[np.str_]:
        array = np.array(letters)
        characters = array.reshape(shape)
        return characters

    def __repr__(self) -> str:
        representation = {
            "shape": self.shape,
            "characters": self.characters,
            "solved_states": self.solved_states,
            "partial_solved": self.partially_solved
        }
        return str(representation)

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class GameState:
    board: Board
    theme: str
    number_of_total_words: int
    number_of_solved_words: int = 0
