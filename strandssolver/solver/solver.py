import networkx as nx
import numpy as np
import pygtrie
import collections

from dataclasses import dataclass
from typing import List, Tuple, Set, Iterable

from strandssolver.models import gamestate
from strandssolver.solver import strandsdfsvisitor, optimizecovering
from strandssolver.dfs import depthfirstsearch
from strandssolver.dfs.typing import Node


@dataclass
class Solver:
    graph: nx.Graph
    game: gamestate.GameState
    trie: pygtrie.Trie

    def solve(self) -> List[Tuple[Node]]:
        words = self.find_all_words()
        covering = self.find_best_covering(words)
        return list(covering)

    def find_all_words(self) -> List[Tuple[Node]]:
        words = []

        for node in self.graph.nodes():
            visitor = strandsdfsvisitor.StrandsDFSVisitor(self.graph,
                                                          self.trie)
            edges = depthfirstsearch.dfs_edges(self.graph, source=node,
                                               depth_limit=8,
                                               dfs_visitor=visitor)
            # Exhaust the iterator so the visitor builds all words
            collections.deque(edges, maxlen=0)
            words.extend(visitor.words.keys())

        return words

    def find_best_covering(self, words: Iterable[Tuple[Node]]
                           ) -> Iterable[Tuple[Node]]:
        problem = optimizecovering.convert_words_to_problem_matrix(words,
                                                                   self.graph)
        target = np.ones(len(self.graph.nodes), dtype=np.bool_).T

        max_number_of_words_in_solution = (self.game.number_of_total_words
                                           - self.game.number_of_solved_words)
        # Sometimes the spangram is a compound word so add 1 to be safe
        max_number_of_words_in_solution += 1
        optimizer = optimizecovering.BinaryOptimizer(
            problem,
            target,
            max_number_of_words_in_solution
        )
        solution = optimizer.optimize_binary_vector()
        covering = optimizecovering.convert_problem_solution_to_words(solution,
                                                                      words)
        return covering


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    from matplotlib import pyplot as plt
    graph = stubgraph.StubGraphBuilder.build_graph_from_board()
    game = stubgamestate.StubGameState()
    trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()

    solver = Solver(graph=graph, game=game, trie=trie)
    solution = solver.solve()
    for word in solution:
        string = ""
        for node in word:
            string += graph.nodes[node]["character"]
        print(string)

    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos=pos)
    nx.draw_networkx_labels(graph,
                            labels={node: data["character"]
                                    for node, data in graph.nodes(data=True)},
                            pos=pos)
    cm = plt.get_cmap('gist_rainbow')
    colors = (cm(x) for x in np.linspace(0, 1, len(solution)))
    for word, color in zip(solution, colors):
        print(color)
        r, g, b, _ = color
        color = (r, g, b)
        edgelist = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
        nx.draw_networkx_edges(graph, edgelist=edgelist, pos=pos,
                               edge_color=color, width=4)
        nx.draw_networkx_nodes(graph, nodelist=[word[0]], pos=pos,
                               node_color=color, node_size=200)
    plt.show()


def _profile() -> None:
    import cProfile
    cProfile.run('_test()')


if __name__ == "__main__":
    _test()
