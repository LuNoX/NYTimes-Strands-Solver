import networkx as nx
import numpy as np
import pygtrie
import collections

from dataclasses import dataclass
from typing import List, Tuple, Set, Iterable

from strandssolver.models import gamestate, graph as ssgraph
from strandssolver.solver import (strandsdfsvisitor, optimizecovering,
                                  enumeratecovering, rankcovering)
from strandssolver.dfs import depthfirstsearch
from strandssolver.dfs.typing import Node


@dataclass
class Solver:
    graph: nx.Graph
    game: gamestate.GameState
    trie: pygtrie.Trie

    def solve(self) -> List[rankcovering.RankedCovering]:
        words = self.find_all_words()
        return self.rank_all_coverings(words)

    @property
    def max_number_of_words_in_solution(self) -> int:
        max_number_of_words_in_solution = (self.game.number_of_total_words
                                           - self.game.number_of_solved_words)
        # Sometimes the spangram is a compound word so add 1 to be safe
        return max_number_of_words_in_solution + 1

    def spell(self, word: Tuple[Node, ...]) -> str:
        key_for_character = ssgraph.CharacterGraphBuilder. \
            DEFAULT_KEY_FOR_CHARACTER
        return "".join(self.graph.nodes[node][key_for_character]
                       for node in word)

    def find_all_words(self) -> List[Tuple[Node]]:
        words = {}

        for node in self.graph.nodes():
            visitor = strandsdfsvisitor.StrandsDFSVisitor(self.graph,
                                                          self.trie)
            edges = depthfirstsearch.dfs_edges(self.graph, source=node,
                                               dfs_visitor=visitor)
            # Exhaust the iterator so the visitor builds all words
            collections.deque(edges, maxlen=0)
            for word, string in visitor.words.items():
                words.setdefault((frozenset(word), string), word)

        return list(words.values())

    def rank_all_coverings(self, words: Iterable[Tuple[Node]]
                           ) -> List[rankcovering.RankedCovering]:
        enumerator = enumeratecovering.ExactCoverEnumerator(
            words,
            self.graph,
            self.max_number_of_words_in_solution
        )
        ranker = rankcovering.CoveringRanker()
        return ranker.rank(enumerator.enumerate(), self.spell)

    def find_best_covering(self, words: Iterable[Tuple[Node]]
                           ) -> Iterable[Tuple[Node]]:
        problem = optimizecovering.convert_words_to_problem_matrix(words,
                                                                   self.graph)
        target = np.ones(len(self.graph.nodes), dtype=np.bool_).T

        optimizer = optimizecovering.BinaryOptimizer(
            problem,
            target,
            self.max_number_of_words_in_solution
        )
        solution = optimizer.optimize_binary_vector()
        covering = optimizecovering.convert_problem_solution_to_words(solution,
                                                                      words)
        return covering


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    graph = stubgraph.StubGraphBuilder.build_graph_from_board()
    game = stubgamestate.StubGameState()
    trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()

    solver = Solver(graph=graph, game=game, trie=trie)
    for ranked_covering in solver.solve():
        words = [solver.spell(word) for word in ranked_covering.covering]
        print(f"{ranked_covering.score:.2f}: {', '.join(words)}")


def _profile() -> None:
    import cProfile
    cProfile.run('_test()')


if __name__ == "__main__":
    _test()
