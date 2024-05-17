import networkx as nx

from typing import Callable, Iterable, Set

from strandssolver.dfs import dfsvisitor, dfsexceptions
from strandssolver.dfs.typing import Node, Edge


def dfs_edges(
        G: nx.Graph, source: Node = None, depth_limit: int = None, *,
        sort_neighbors: Callable[[Iterable[Node]], Iterable[Node]] = None,
        dfs_visitor: dfsvisitor.DFSVisitor = None) -> Iterable[Edge]:
    if source is None:
        # edges for all components
        nodes = G
    else:
        # edges for components with source
        nodes = [source]
    if depth_limit is None:
        depth_limit = len(G)
    if dfs_visitor is None:
        dfs_visitor = dfsvisitor.IdleDFSVisitor()

    get_children = (
        G.neighbors
        if sort_neighbors is None
        else lambda n: iter(sort_neighbors(G.neighbors(n)))
    )

    visited = set()
    for start in nodes:
        try:
            yield _single_start_node_dfs(start, depth_limit=depth_limit,
                                         visited=visited,
                                         get_children=get_children,
                                         dfs_visitor=dfs_visitor)
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _single_start_node_dfs(
        start: Node, depth_limit: int = None, visited: Set[Node] = None, *,
        get_children: Callable[[Node], Iterable[Node]] = None,
        dfs_visitor: dfsvisitor.DFSVisitor = None
) -> Iterable[Edge]:
    if visited is None:
        visited = set()
    if dfs_visitor is None:
        dfs_visitor = dfsvisitor.IdleDFSVisitor()
    if start in visited:
        raise dfsexceptions.NextSourceNode()

    visited.add(start)
    stack = [(start, get_children(start))]
    back_vertices = set(start)
    depth_now = 1

    while stack:
        parent, children = stack[-1]
        back_vertices.add(parent)
        dfs_visitor.discover_vertex(parent)
        for child in children:
            edge = (parent, child)
            if child not in visited:
                try:
                    dfs_visitor.tree_edge(edge)
                except dfsexceptions.PruneSearch:
                    continue
                yield parent, child
                visited.add(child)
                if depth_now < depth_limit:
                    stack.append((child, get_children(child)))
                    depth_now += 1
                    break
            elif child in back_vertices:
                try:
                    dfs_visitor.back_edge(edge)
                except dfsexceptions.PruneSearch:
                    continue
            else:
                try:
                    dfs_visitor.forward_or_cross_edge(edge)
                except dfsexceptions.PruneSearch:
                    # Not really necessary since the edge was about to be
                    # removed anyway, but better to not raise an exception
                    continue
        else:
            back_vertices.remove(parent)
            stack.pop()
            depth_now -= 1
            # No need to check for prune because vertex was already removed
            dfs_visitor.finish_vertex(parent)


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    g = stubgraph.StubGraphBuilder.build_graph_from_board()
    original = nx.dfs_edges(g, depth_limit=4)
    print(list(original))
    with_visitor = dfs_edges(g, depth_limit=4)
    print(list(with_visitor))
    difference = [a == b for a, b in zip(original, with_visitor)]
    print(all(difference))
    print(difference)


if __name__ == "__main__":
    _test()
