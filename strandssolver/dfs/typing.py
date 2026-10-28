from typing import Any, Iterable, Protocol, Tuple

type Vertex = Any
type Node = Vertex
type Edge = Tuple[Node, Node]


class GetChildren(Protocol):
    def __call__(self, node: Node, /, **kwargs: Any) -> Iterable[Node]:
        raise NotImplementedError()


class SortNeighbors(Protocol):
    def __call__(self, neighbors: Iterable[Node], /, **kwargs: Any) -> Iterable[Node]:
        raise NotImplementedError()
