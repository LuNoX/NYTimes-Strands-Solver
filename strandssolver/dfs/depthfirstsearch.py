import networkx as nx

from typing import Callable, Iterable

from strandssolver.dfs import dfsvisitor, dfsexceptions, dfsdepth
from strandssolver.dfs.typing import Node, Edge


def _dfs_for_child(stack, parent, child, depth,
                   visited, completed, get_children, dfs_visitor):
    edge = (parent, child)
    # Black node?
    if child in completed:
        dfs_visitor.forward_or_cross_edge(edge)
    # Grey node?
    elif child in visited:
        dfs_visitor.back_edge(edge)
    # Then must be white node
    else:
        dfs_visitor.tree_edge(edge)
        yield parent, child
        visited.add(child)
        if depth.depth_now < depth.depth_limit:
            stack.append((child, get_children(child)))
            depth.depth_now += 1
            raise dfsexceptions.GoDeeper()


def _finish_node(parent, completed, visited, stack, depth, dfs_visitor):
    completed.add(parent)
    visited.remove(parent)
    stack.pop()
    depth.depth_now -= 1
    try:
        dfs_visitor.finish_vertex(parent)
    except dfsexceptions.PruneSearch:
        # Not really necessary since pruning on exit is pointless,
        # but better to not propagate an exception
        pass


def _dfs_while_stack(stack, visited, completed, depth,
                     get_children,
                     dfs_visitor):
    parent, children = stack[-1]
    try:
        dfs_visitor.discover_vertex(parent)
    except dfsexceptions.PruneSearch:
        _finish_node(parent, completed, visited, stack, depth, dfs_visitor)
        return
    for child in children:
        try:
            yield from _dfs_for_child(stack, parent, child,
                                      depth,
                                      visited, completed,
                                      get_children, dfs_visitor)
        except dfsexceptions.PruneSearch:
            continue
        except dfsexceptions.GoDeeper:
            break
    else:
        _finish_node(parent, completed, visited, stack, depth, dfs_visitor)


def _dfs_edges_for_single_source_node(
        start, depth_limit, visited, completed, get_children, dfs_visitor):
    if start in visited:
        raise dfsexceptions.NextSourceNode()
    visited.add(start)
    depth = dfsdepth.Depth(depth_limit=depth_limit)
    stack = [(start, get_children(start))]

    while stack:
        yield from _dfs_while_stack(stack, visited, completed, depth,
                                    get_children, dfs_visitor)


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

    # White := nodes that are neither in visited nor in completed
    visited = set()  # gray
    completed = set()  # black
    for start in nodes:
        try:
            yield from _dfs_edges_for_single_source_node(start, depth_limit,
                                                         visited, completed,
                                                         get_children,
                                                         dfs_visitor)
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    g = stubgraph.StubGraphBuilder.build_graph_from_board()
    original = nx.dfs_edges(g, depth_limit=20)
    original_list = list(original)
    with_visitor = dfs_edges(g, depth_limit=20)
    with_visitor_list = list(with_visitor)
    difference = [a == b for a, b in zip(original_list, with_visitor_list)]
    print(difference)
    print(all(difference))
    print(len(with_visitor_list) == len(original_list))


if __name__ == "__main__":
    _test()
