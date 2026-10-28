import networkx as nx

from typing import Dict, Iterable, Iterator, List, Tuple, Optional

from strandssolver.dfs.typing import Node


class ExactCoverEnumerator:
    def __init__(
        self,
        words: Iterable[Tuple[Node, ...]],
        graph: nx.Graph,
        max_number_of_words: Optional[int] = None,
    ) -> None:
        self.words = list(words)
        if max_number_of_words is None:
            max_number_of_words = len(graph)
        self.max_number_of_words = max_number_of_words

        # Filling the board row by row makes dead ends show up early
        nodes = sorted(graph.nodes)
        bit_per_node = {node: 1 << index for index, node in enumerate(nodes)}
        self.all_nodes_mask = (1 << len(nodes)) - 1
        self.masks = [sum(bit_per_node[node] for node in word) for word in self.words]
        self.longest_word_length = max(map(len, self.words), default=0)

        # The search always covers the lowest uncovered node next
        self.words_per_lowest_node: List[List[int]] = [[] for _ in nodes]
        for index, mask in enumerate(self.masks):
            self.words_per_lowest_node[_lowest_bit_index(mask)].append(index)

        # Covered mask -> largest number of words left it failed with
        self._dead_ends: Dict[int, int] = {}

    def enumerate(self) -> Iterator[List[Tuple[Node, ...]]]:
        for indices in self._search(0, self.max_number_of_words):
            yield [self.words[index] for index in indices]

    def _search(self, covered: int, words_left: int) -> Iterator[List[int]]:
        if covered == self.all_nodes_mask:
            yield []
            return
        uncovered = self.all_nodes_mask & ~covered
        max_coverable = words_left * self.longest_word_length
        if (
            uncovered.bit_count() > max_coverable
            or self._dead_ends.get(covered, -1) >= words_left
        ):
            return

        found_covering = False
        next_node = _lowest_bit_index(uncovered)
        for index in self.words_per_lowest_node[next_node]:
            mask = self.masks[index]
            if mask & covered:
                continue
            for rest in self._search(covered | mask, words_left - 1):
                found_covering = True
                yield [index, *rest]
        if not found_covering:
            self._dead_ends[covered] = words_left


def _lowest_bit_index(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def _test() -> None:
    graph = nx.grid_2d_graph(2, 2)
    words = [
        ((0, 0), (0, 1)),
        ((1, 0), (1, 1)),
        ((0, 0), (1, 0)),
        ((0, 1), (1, 1)),
        ((0, 0), (0, 1), (1, 1)),
    ]
    enumerator = ExactCoverEnumerator(words, graph, max_number_of_words=2)
    for covering in enumerator.enumerate():
        print(covering)


if __name__ == "__main__":
    _test()
