from typing import Any, Tuple, NewType

Vertex = NewType('Vertex', Any)
Node = NewType('Node', Vertex)
Edge = NewType('Edge', Tuple[Node, Node])
