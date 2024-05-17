from typing import Protocol, Any, Tuple, Iterable, NewType

from strandssolver.dfs.typing import Edge, Vertex


class DFSVisitor(Protocol):
    def back_edge(self, edge: Edge) -> None:
        raise NotImplementedError()

    def discover_vertex(self, vertex: Vertex) -> None:
        raise NotImplementedError()

    def finish_vertex(self, vertex: Vertex) -> None:
        raise NotImplementedError()

    def forward_or_cross_edge(self, edge: Edge) -> None:
        raise NotImplementedError()

    def tree_edge(self, edge: Edge) -> None:
        raise NotImplementedError()

    def sort_neighbors(self, neighbors: Iterable[Vertex]) -> Iterable[Vertex]:
        raise NotImplementedError()


class IdleDFSVisitor(DFSVisitor):
    def back_edge(self, edge: Edge) -> None:
        """
        When encountering a back edge, do nothing.
        :param edge: back edge
        :return: None
        """
        pass

    def discover_vertex(self, vertex: Vertex) -> None:
        """
        When encountering a vertex, do nothing.
        :param vertex: discovered vertex
        :return: None
        """
        pass

    def finish_vertex(self, vertex: Vertex) -> None:
        """
        When finishing a vertex, do nothing.
        :param vertex: finished vertex
        :return: None
        """
        pass

    def forward_or_cross_edge(self, edge: Edge) -> None:
        """
        When encountering a forward or cross edge, do nothing.
        :param edge: forward or cross edge
        :return: None
        """
        pass

    def tree_edge(self, edge: Edge) -> None:
        """
        When encountering a tree edge, do nothing.
        :param edge: tree edge
        :return: None
        """
        pass

    def sort_neighbors(self, neighbors: Iterable[Vertex]) -> Iterable[Vertex]:
        """
        When sorting neighbors, return original ordering.
        :param neighbors: neighbors
        :return: original ordering
        """
        return neighbors


def _test() -> None:
    pass


if __name__ == "__main__":
    _test()
