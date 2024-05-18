from dataclasses import dataclass


@dataclass
class Depth:
    depth_limit: int
    depth_now: int = 1
