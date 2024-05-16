from dataclasses import dataclass
from typing import List, Iterable, Tuple, Set, Callable
import networkx as nx

from strandssolver import gamestate


@dataclass
class Solver:
    graph: nx.Graph
    game: gamestate.GameState

    def solve(self) -> List[Set[Tuple[int, ...]]]:
        ...

    def find_all_words_in_graph_then_construct_partitions(self):
        ...

    def find_all_partitions_then_check_if_partition_is_a_valid_solution(self):
        ...

    def generate_all_potential_solutions(self) -> List:
        for clique in nx.enumerate_all_cliques(self.graph):
            ...

    @staticmethod
    def generate_all_cliques_of_minimum_size_k(
            graph: nx.Graph, k: int) -> Iterable[Set[Tuple[int, ...]]]:
        cliques = Solver.generate_all_cliques_fulfilling_condition(
            graph, lambda clique: len(clique) >= k)
        return cliques

    @staticmethod
    def generate_all_cliques_fulfilling_condition(
            graph: nx.Graph, condition: Callable[[Set[Tuple[int, ...]]], bool]
    ) -> Iterable[Set[Tuple[int, ...]]]:
        cliques = (clique for clique in nx.enumerate_all_cliques(graph)
                   if condition(clique))
        return cliques
