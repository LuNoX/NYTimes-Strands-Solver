import networkx as nx
import pygtrie
import multiprocessing as mp
import itertools

from dataclasses import dataclass
from typing import List, Tuple, Set

from strandssolver.dfs import depthfirstsearch, dfsvisitor
from strandssolver.dfs.typing import Vertex, Node
from strandssolver.models import gamestate


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
                       itertools.repeat(StrandsDFSVisitor()))
            pool.starmap(find_all_paths_for_node, args)

        return words


def find_all_paths_for_node(graph: nx.Graph, node: Node,
                            dfs_visitor: dfsvisitor.DFSVisitor
                            ) -> None:
    edges = depthfirstsearch.dfs_edges(graph, node, dfs_visitor=dfs_visitor)
    print(f"node: {node}, edges: {list(edges)}")


class StrandsDFSVisitor(dfsvisitor.IdleDFSVisitor):
    def finish_vertex(self, vertex: Vertex, **kwargs) -> None:
        kwargs['dfs_completed'].remove(vertex)


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    graph = stubgraph.StubGraphBuilder.build_graph_from_board()
    game = stubgamestate.StubGameState()
    trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()

    graph = nx.grid_2d_graph(m=5, n=5)
    # graph.add_edges_from([((0, 0), (1, 1)), ((0, 1), (1, 0))])

    solver = Solver(graph=graph, game=game, trie=trie)
    solver.solve()


if __name__ == "__main__":
    _test()
