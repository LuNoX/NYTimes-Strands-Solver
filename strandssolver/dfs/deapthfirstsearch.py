import networkx as nx

from typing import Callable, Iterable, Set

from strandssolver.dfs import dfsvisitor, dfsexceptions
from strandssolver.dfs.typing import Node, Edge


@nx._dispatchable
def dfs_edges(G: nx.Graph, source: Node = None, depth_limit: int = None, *,
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
            yield _single_node_dfs(start, depth_limit=depth_limit,
                                   visited=visited,
                                   get_children=get_children,
                                   dfs_visitor=dfs_visitor)
        except dfsexceptions.StopSearch:
            return
        except dfsexceptions.NextSourceNode:
            continue


def _single_node_dfs(start: Node, depth_limit: int = None,
                     visited: Set[Node] = None, *,
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


def _test():
    pass


if __name__ == "__main__":
    _test()
