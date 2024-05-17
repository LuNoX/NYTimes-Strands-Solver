import networkx as nx
import pygtrie

from dataclasses import dataclass
from typing import List, Tuple, Set

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
        # TODO: parallelize this
        for node, data in self.graph.nodes(data=True):
            # DFS
            # Break if prefix not in dict
            # append words and paths to list
            ...
            for edge in nx.dfs_edges(self.graph, depth_limit=6):
                continue
            print(f"node: {node},"" edges: {list(edges)}")
        return words

    def dfs(self):
        visited = set()
        for node, data in nodes:
            ...


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    solver = Solver(
        graph=stubgraph.StubGraphBuilder.build_graph_from_board(),
        game=stubgamestate.StubGameState(),
        trie=stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()
    )
    solver.solve()


if __name__ == "__main__":
    _test()
