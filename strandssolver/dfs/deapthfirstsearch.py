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
    back_vertices = set()
    for start in nodes:
        if start in visited:
            continue
        try:
            visited.add(start)
            stack = [(start, get_children(start))]
            back_vertices.add(start)
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
                            # Not really necessary since the edge was about to
                            # be removed anyway, but better to not propagate an
                            # exception
                            continue
                else:
                    back_vertices.remove(parent)
                    stack.pop()
                    depth_now -= 1
                    try:
                        dfs_visitor.finish_vertex(parent)
                    except dfsexceptions.PruneSearch:
                        # Not really necessary since pruning on exit is
                        # pointless, but better to not propagate an exception
                        continue
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    g = stubgraph.StubGraphBuilder.build_graph_from_board()
    original = nx.dfs_edges(g)
    original_list = list(original)
    with_visitor = dfs_edges(g)
    with_visitor_list = list(with_visitor)
    difference = [a == b for a, b in zip(original_list, with_visitor_list)]
    print(difference)
    print(all(difference))
    print(len(with_visitor_list) == len(original_list))


if __name__ == "__main__":
    _test()
