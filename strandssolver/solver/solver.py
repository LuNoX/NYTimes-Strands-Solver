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

    def dfs_edges(G, source=None, depth_limit=None, *, sort_neighbors=None):
        """Adapted from https://networkx.org/documentation/stable/_modules/networkx/algorithms/traversal/depth_first_search.html#dfs_edges

        Iterate over edges in a depth-first-search (DFS).

        Perform a depth-first-search over the nodes of `G` and yield
        the edges in order. This may not generate all edges in `G`
        (see `~networkx.algorithms.traversal.edgedfs.edge_dfs`).

        Parameters
        ----------
        G : NetworkX graph

        source : node, optional
           Specify starting node for depth-first search and yield edges in
           the component reachable from source.

        depth_limit : int, optional (default=len(G))
           Specify the maximum search depth.

        sort_neighbors : function (default=None)
            A function that takes an iterator over nodes as the input, and
            returns an iterable of the same nodes with a custom ordering.
            For example, `sorted` will sort the nodes in increasing order.

        Yields
        ------
        edge: 2-tuple of nodes
           Yields edges resulting from the depth-first-search.

        Examples
        --------
         G = nx.path_graph(5)
         list(nx.dfs_edges(G, source=0))
        [(0, 1), (1, 2), (2, 3), (3, 4)]
         list(nx.dfs_edges(G, source=0, depth_limit=2))
        [(0, 1), (1, 2)]

        Notes
        -----
        If a source is not specified then a source is chosen arbitrarily and
        repeatedly until all components in the graph are searched.

        The implementation of this function is adapted from David Eppstein's
        depth-first search function in PADS [1]_, with modifications
        to allow depth limits based on the Wikipedia article
        "Depth-limited search" [2]_.

        See Also
        --------
        dfs_preorder_nodes
        dfs_postorder_nodes
        dfs_labeled_edges
        :func:`~networkx.algorithms.traversal.edgedfs.edge_dfs`
        :func:`~networkx.algorithms.traversal.breadth_first_search.bfs_edges`

        References
        ----------
        .. [1] http://www.ics.uci.edu/~eppstein/PADS
        .. [2] https://en.wikipedia.org/wiki/Depth-limited_search
        """
        if source is None:
            # edges for all components
            nodes = G
        else:
            # edges for components with source
            nodes = [source]
        if depth_limit is None:
            depth_limit = len(G)

        get_children = (
            G.neighbors
            if sort_neighbors is None
            else lambda n: iter(sort_neighbors(G.neighbors(n)))
        )

        visited = set()
        for start in nodes:
            if start in visited:
                continue
            visited.add(start)
            stack = [(start, get_children(start))]
            depth_now = 1
            while stack:
                parent, children = stack[-1]
                for child in children:
                    if child not in visited:
                        yield parent, child
                        visited.add(child)
                        if depth_now < depth_limit:
                            stack.append((child, get_children(child)))
                            depth_now += 1
                            break
                else:
                    stack.pop()
                    depth_now -= 1

        visited = set()
        for start in nodes:
            if start in visited:
                continue
            visited.add(start)
            stack = [(start, get_children(start))]
            depth_now = 1
            while stack:
                parent, children = stack[-1]
                for child in children:
                    if child not in visited:
                        yield parent, child
                        visited.add(child)
                        if depth_now < depth_limit:
                            stack.append((child, get_children(child)))
                            depth_now += 1
                            break
                else:
                    stack.pop()
                    depth_now -= 1


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie
    graph = stubgraph.StubGraphBuilder.build_graph_from_board()
    # game = stubgamestate.StubGameState()
    # trie = stubdictionarytrie.StubDictionaryTrieBuilder.load_trie_from_json()
    # solver = Solver(graph=graph, game=game, trie=trie)
    # solver.solve()


if __name__ == "__main__":
    _test()
