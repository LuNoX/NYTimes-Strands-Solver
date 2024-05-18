import networkx as nx

from typing import Callable, Iterable, Set, Optional, List, Tuple

from strandssolver.dfs import dfsvisitor, dfsexceptions, dfsdepth
from strandssolver.dfs.typing import Node, Edge


def _dfs_for_child(stack: List[Tuple[Node, Iterable[Node]]],
                   parent: Node, child: Node, depth: dfsdepth.Depth,
                   visited: Set[Node], completed: Set[Node],
                   get_children: Callable[[Node,
                                           Optional[...]], Iterable[Node]],
                   dfs_visitor: dfsvisitor.DFSVisitor,
                   **kwargs) -> Iterable[Edge]:
    edge = (parent, child)
    kwargs["dfs_edge"] = edge
    # Black node?
    if child in completed:
        dfs_visitor.forward_or_cross_edge(edge, **kwargs)
    # Grey node?
    elif child in visited:
        dfs_visitor.back_edge(edge, **kwargs)
    # Then must be white node
    else:
        dfs_visitor.tree_edge(edge, **kwargs)
        yield parent, child
        visited.add(child)
        if depth.depth_now < depth.depth_limit:
            stack.append((child, get_children(child, **kwargs)))
            depth.depth_now += 1
            raise dfsexceptions.GoDeeper()


def _finish_node(parent: Node, completed: Set[Node], visited: Set[Node],
                 stack: List[Tuple[Node, Iterable[Node]]],
                 depth: dfsdepth.Depth, dfs_visitor: dfsvisitor.DFSVisitor,
                 **kwargs) -> None:
    completed.add(parent)
    visited.remove(parent)
    stack.pop()
    depth.depth_now -= 1
    try:
        dfs_visitor.finish_vertex(parent, **kwargs)
    except dfsexceptions.PruneSearch:
        # Not really necessary since pruning on exit is pointless,
        # but better to not propagate an exception
        pass


def _dfs_while_stack(
        stack: List[Tuple[Node, Iterable[Node]]],
        visited: Set[Node], completed: Set[Node], depth: dfsdepth.Depth,
        get_children: Callable[[Node, Optional[...]], Iterable[Node]],
        dfs_visitor: dfsvisitor.DFSVisitor,
        **kwargs) -> Iterable[Edge]:
    parent, children = stack[-1]
    kwargs["dfs_parent"] = parent
    kwargs["dfs_children"] = children
    try:
        dfs_visitor.discover_vertex(parent, **kwargs)
    except dfsexceptions.PruneSearch:
        _finish_node(parent, completed, visited, stack, depth, dfs_visitor,
                     **kwargs)
        return
    for child in children:
        try:
            yield from _dfs_for_child(stack, parent, child,
                                      depth,
                                      visited, completed,
                                      get_children, dfs_visitor, **kwargs)
        except dfsexceptions.PruneSearch:
            continue
        except dfsexceptions.GoDeeper:
            break
    else:
        _finish_node(parent, completed, visited, stack, depth, dfs_visitor,
                     **kwargs)


def _dfs_edges_for_single_source_node(
        start: Node, depth_limit: int,
        visited: Set[Node], completed: Set[Node],
        get_children: Callable[[Node, Optional[...]], Iterable[Node]],
        dfs_visitor: dfsvisitor.DFSVisitor,
        **kwargs) -> Iterable[Edge]:
    if start in visited:
        raise dfsexceptions.NextSourceNode()
    visited.add(start)
    depth = dfsdepth.Depth(depth_limit=depth_limit)
    kwargs["dfs_depth"] = depth
    stack = [(start, get_children(start, **kwargs))]
    kwargs["dfs_stack"] = stack

    while stack:
        yield from _dfs_while_stack(stack, visited, completed, depth,
                                    get_children, dfs_visitor, **kwargs)


def dfs_edges(
        G: nx.Graph, source: Node = None, depth_limit: int = None, *,
        sort_neighbors: Callable[[Iterable[Node],
                                  Optional[...]], Iterable[Node]] = None,
        dfs_visitor: dfsvisitor.DFSVisitor = None,
        **kwargs) -> Iterable[Edge]:
    if source is None:
        # edges for all components
        nodes = G
    else:
        # edges for components with source
        nodes = [source]
    kwargs["dfs_nodes"] = nodes
    if depth_limit is None:
        depth_limit = len(G)
    if dfs_visitor is None:
        dfs_visitor = dfsvisitor.IdleDFSVisitor()
    if sort_neighbors is None:
        sort_neighbors = dfs_visitor.sort_neighbors
    kwargs["sort_neighbors"] = sort_neighbors

    get_children = (
        lambda n, **inner_kwargs:
        iter(sort_neighbors(G.neighbors(n), **inner_kwargs))
    )
    kwargs["dfs_get_children"] = get_children

    # White := nodes that are neither in visited nor in completed
    visited = set()  # gray
    completed = set()  # black
    for start in nodes:
        try:
            yield from _dfs_edges_for_single_source_node(start, depth_limit,
                                                         visited, completed,
                                                         get_children,
                                                         dfs_visitor, **kwargs)
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    g = stubgraph.StubGraphBuilder.build_graph_from_board()
    original = nx.dfs_edges(g, depth_limit=20)
    original_list = list(original)
    print(original_list)
    with_visitor = dfs_edges(g, depth_limit=20)
    with_visitor_list = list(with_visitor)
    print(with_visitor_list)
    difference = [a == b for a, b in zip(original_list, with_visitor_list)]
    print(difference)
    print(all(difference))
    print(len(with_visitor_list) == len(original_list))


if __name__ == "__main__":
    _test()
