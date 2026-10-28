import statistics
import wordfreq

from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Tuple, Optional

from strandssolver.dfs.typing import Node


@dataclass(order=True)
class RankedCovering:
    score: float
    covering: List[Tuple[Node, ...]] = field(compare=False)


class CoveringRanker:
    DEFAULT_LANGUAGE = "en"

    def __init__(self, language: Optional[str] = None) -> None:
        if language is None:
            language = CoveringRanker.DEFAULT_LANGUAGE
        self.language = language

    def score_word(self, word: str) -> float:
        return wordfreq.zipf_frequency(word.lower(), self.language)

    def score_covering(self, words: Iterable[str]) -> float:
        scores = [self.score_word(word) for word in words]
        if not scores:
            return 0.0
        return statistics.fmean(scores)

    def rank(
        self,
        coverings: Iterable[List[Tuple[Node, ...]]],
        spell: Callable[[Tuple[Node, ...]], str],
    ) -> List[RankedCovering]:
        ranked = [
            RankedCovering(
                score=self.score_covering(spell(word) for word in covering),
                covering=covering,
            )
            for covering in coverings
        ]
        return sorted(ranked, reverse=True)


def _test() -> None:
    ranker = CoveringRanker()
    for words in [
        ["corsage", "tuxedo", "dance", "boutonniere"],
        ["tussor", "thionine", "egbo", "tunnor"],
    ]:
        print(words, ranker.score_covering(words))


if __name__ == "__main__":
    _test()
