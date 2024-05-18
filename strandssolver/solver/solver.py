import networkx as nx
import pygtrie
import multiprocessing as mp
import itertools

from dataclasses import dataclass
from typing import List, Tuple, Set

from strandssolver.models import gamestate
from strandssolver.solver import strandsdfsvisitor
from strandssolver.dfs import depthfirstsearch, dfsvisitor
from strandssolver.dfs.typing import Node


@dataclass
class Solver:
    graph: nx.Graph
    game: gamestate.GameState
    trie: pygtrie.Trie

    def solve(self) -> List[Set[Tuple[int, ...]]]:
        self.find_all_words()

    def find_all_words(self) -> List[Tuple[str, List[Tuple[int, ...]]]]:
        words = []

        with mp.Pool(mp.cpu_count()) as pool:
            args = zip(itertools.repeat(self.graph),
                       self.graph.nodes(),
                       itertools.repeat(strandsdfsvisitor.StrandsDFSVisitor(
                           self.graph, self.trie))
                       )
            pool.starmap(find_all_paths_for_node, args)

        return words


def find_all_paths_for_node(graph: nx.Graph, node: Node,
                            dfs_visitor: strandsdfsvisitor.StrandsDFSVisitor
                            ) -> None:
    edges = depthfirstsearch.dfs_edges(graph, node, dfs_visitor=dfs_visitor)
    a = list(edges)
    print(node)
    print(dfs_visitor.words)


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    graph = stubgraph.StubGraphBuilder.build_small_graph()
    game = stubgamestate.StubSmallGameState()
    trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()

    # graph = nx.grid_2d_graph(m=4, n=4)
    # graph.add_edges_from([((0, 0), (1, 1)), ((0, 1), (1, 0))])

    solver = Solver(graph=graph, game=game, trie=trie)
    solver.solve()


if __name__ == "__main__":
    _test()
