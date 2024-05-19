import networkx as nx

from typing import Callable, Iterable, Set, Optional, List, Tuple

from strandssolver.dfs import dfsvisitor, dfsexceptions, dfsdepth
from strandssolver.dfs.typing import Node, Edge


def _dfs_for_child(parent: Node, child: Node,
                   stack: List[Tuple[Node, Iterable[Node]]],
                   visited: Set[Node], completed: Set[Node],
                   depth: dfsdepth.Depth,
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
        # visited.add(child)
        if depth.depth_now < depth.depth_limit:
            stack.append((child, get_children(child, **kwargs)))
            depth.depth_now += 1
            raise dfsexceptions.GoDeeper()


def _finish_node(parent: Node, stack: List[Tuple[Node, Iterable[Node]]],
                 completed: Set[Node], visited: Set[Node],
                 depth: dfsdepth.Depth,
                 dfs_visitor: dfsvisitor.DFSVisitor,
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


def _dfs_while_stack(stack: List[Tuple[Node, Iterable[Node]]],
                     visited: Set[Node], completed: Set[Node],
                     depth: dfsdepth.Depth,
                     get_children: Callable[[Node,
                                             Optional[...]], Iterable[Node]],
                     dfs_visitor: dfsvisitor.DFSVisitor,
                     **kwargs) -> Iterable[Edge]:
    parent, children = stack[-1]
    kwargs["dfs_parent"] = parent
    kwargs["dfs_children"] = children
    if parent not in visited:
        try:
            visited.add(parent)
            dfs_visitor.discover_vertex(parent, **kwargs)
        except dfsexceptions.PruneSearch:
            _finish_node(parent=parent, stack=stack,
                         completed=completed, visited=visited,
                         depth=depth,
                         dfs_visitor=dfs_visitor,
                         **kwargs)
            return
    for child in children:
        try:
            yield from _dfs_for_child(parent=parent, child=child, stack=stack,
                                      visited=visited, completed=completed,
                                      depth=depth,
                                      get_children=get_children,
                                      dfs_visitor=dfs_visitor, **kwargs)
        except dfsexceptions.PruneSearch:
            continue
        except dfsexceptions.GoDeeper:
            break
    else:
        _finish_node(parent=parent, stack=stack,
                     completed=completed, visited=visited,
                     depth=depth,
                     dfs_visitor=dfs_visitor, **kwargs)


def _dfs_edges_for_single_source_node(
        start: Node, depth_limit: int,
        visited: Set[Node], completed: Set[Node],
        get_children: Callable[[Node, Optional[...]], Iterable[Node]],
        dfs_visitor: dfsvisitor.DFSVisitor,
        **kwargs) -> Iterable[Edge]:
    if start in visited:
        raise dfsexceptions.NextSourceNode()
    # visited.add(start)
    depth = dfsdepth.Depth(depth_limit=depth_limit)
    kwargs["dfs_depth"] = depth
    stack = [(start, get_children(start, **kwargs))]
    kwargs["dfs_stack"] = stack

    while stack:
        yield from _dfs_while_stack(stack=stack,
                                    visited=visited, completed=completed,
                                    depth=depth,
                                    get_children=get_children,
                                    dfs_visitor=dfs_visitor, **kwargs)


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
    kwargs["dfs_depth_limt"] = depth_limit
    if dfs_visitor is None:
        dfs_visitor = dfsvisitor.IdleDFSVisitor()
    if sort_neighbors is None:
        sort_neighbors = dfs_visitor.sort_neighbors
    kwargs["dfs_sort_neighbors"] = sort_neighbors
    kwargs["dfs_G"] = G

    get_children = (
        lambda n, **inner_kwargs:
        iter(sort_neighbors(G.neighbors(n), **inner_kwargs))
    )
    kwargs["dfs_get_children"] = get_children

    # White := nodes that are neither in visited nor in completed
    visited = set()  # gray
    completed = set()  # black
    kwargs["dfs_visited"] = visited
    kwargs["dfs_completed"] = completed
    for start in nodes:
        try:
            yield from _dfs_edges_for_single_source_node(
                start=start, depth_limit=depth_limit,
                visited=visited, completed=completed,
                get_children=get_children,
                dfs_visitor=dfs_visitor, **kwargs
            )
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _test() -> None:
    from strandssolver.test.stubs import stubgraph
    g = stubgraph.StubGraphBuilder.build_small_graph()
    depth_limit = 4
    original = nx.dfs_edges(g, depth_limit=depth_limit)
    original_list = set(original)
    print(original_list)
    with_visitor = dfs_edges(g, depth_limit=depth_limit)
    with_visitor_list = set(with_visitor)
    print(with_visitor_list)
    difference = [a == b for a, b in zip(original_list, with_visitor_list)]
    print(difference)
    print(all(difference))
    print(len(with_visitor_list) == len(original_list))
    print(with_visitor_list - original_list)
    print(original_list - with_visitor_list)


if __name__ == "__main__":
    _test()
