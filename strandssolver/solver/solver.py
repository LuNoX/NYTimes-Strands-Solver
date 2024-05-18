import networkx as nx
import pygtrie

from dataclasses import dataclass
from typing import List, Tuple, Set

from strandssolver.dfs import depthfirstsearch
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
        for node in self.graph.nodes():
            # DFS
            # Break if prefix not in dict
            # append words and paths to list

            for edge in depthfirstsearch.dfs_edges(self.graph, depth_limit=6):
                continue
            print(f"node: {node},"" edges: {list(edges)}")
            break
        return words


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    graph = stubgraph.StubGraphBuilder.build_graph_from_board()
    game = stubgamestate.StubGameState()
    trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()
    solver = Solver(graph=graph, game=game, trie=trie)
    solver.solve()


if __name__ == "__main__":
    _test()
