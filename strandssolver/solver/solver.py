from dataclasses import dataclass
from typing import List, Iterable, Tuple, Set, Callable
import networkx as nx

from strandssolver.models import gamestate


@dataclass
class Solver:
    graph: nx.Graph
    game: gamestate.GameState

    def solve(self) -> List[Set[Tuple[int, ...]]]:
        ...
