import networkx as nx
import pygtrie

from typing import override, Any

from strandssolver.models import graph as ssgraph
from strandssolver.dfs import dfsvisitor, dfsexceptions
from strandssolver.dfs.typing import Vertex, Edge


class StrandsDFSVisitor(dfsvisitor.IdleDFSVisitor):
    @override
    def __init__(self, graph: nx.Graph, trie: pygtrie.Trie) -> None:
        self.graph = graph
        self.trie = trie
        self.current_prefix = ""
        self.current_path = []
        self.words = {}

    def backtrack_until_vertex(self, vertex: Vertex) -> int:
        if len(self.current_path) <= 0:
            raise ValueError(f'Trying to backtrack to vertex "{vertex}" '
                             'on empty path!'
                             'Path cannot be empty when backtracking.')
        steps_taken = 0
        while self.current_path[-1] != vertex:
            self.current_path.pop()
            steps_taken += 1
            if len(self.current_path) <= 0:
                raise ValueError(f'Trying to backtrack to vertex "{vertex}" '
                                 'on path but vertex was never encountered!'
                                 'Path must contain target vertex when '
                                 'backtracking.')
        return steps_taken

    def get_character_from_vertex(self, vertex: Vertex,
                                  key_for_character: Any = None) -> str:
        if key_for_character is None:
            key_for_character = ssgraph.CharacterGraphBuilder. \
                DEFAULT_KEY_FOR_CHARACTER
        return self.graph.nodes[vertex][key_for_character]

    def travel_edge(self, edge: Edge) -> None:
        origin, _ = edge
        steps_backtracked = self.backtrack_until_vertex(origin)
        if steps_backtracked > 0:
            self.current_prefix = self.current_prefix[:-steps_backtracked]

    @override
    def discover_vertex(self, vertex: Vertex, **kwargs) -> None:
        self.current_path.append(vertex)
        self.current_prefix += self.get_character_from_vertex(vertex).lower()
        if not self.trie.has_subtrie(self.current_prefix):
            return
            raise dfsexceptions.PruneSearch
        if self.trie.has_key(self.current_prefix):
            self.words[tuple(self.current_path)] = self.current_prefix

    @override
    def finish_vertex(self, vertex: Vertex, **kwargs) -> None:
        kwargs['dfs_completed'].remove(vertex)
        self.current_path.pop()
        self.current_prefix = self.current_prefix[:-1]

    @override
    def tree_edge(self, edge: Edge, **kwargs) -> None:
        self.travel_edge(edge)
        _, destination = edge
        next_character = self.get_character_from_vertex(destination).lower()
        if not self.trie.has_subtrie(self.current_prefix + next_character):
            return
            raise dfsexceptions.PruneSearch
