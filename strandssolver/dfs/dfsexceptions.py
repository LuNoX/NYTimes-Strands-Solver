class DFSException(Exception):
    pass


class NextSourceNode(DFSException):
    pass


class PruneSearch(DFSException):
    pass


class StopSearch(DFSException):
    pass
