from typing import Protocol, Any


class Reader(Protocol):
    def read(self, source: Any) -> Any:
        raise NotImplementedError()
