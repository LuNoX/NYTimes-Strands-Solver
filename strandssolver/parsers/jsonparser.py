from typing import Any, Dict, override

from strandssolver.models import gamestate
from strandssolver.parsers import parser
from strandssolver.readers import reader, jsonreader


class JSONParser(parser.Parser):
    def __init__(
        self, puzzle: Dict[str, Any] = None, json_reader: reader.Reader = None
    ) -> None:
        if json_reader is None:
            json_reader = jsonreader.JSONReader()
        self.json_reader = json_reader
        if puzzle is None:
            puzzle = self.json_reader.read()
        self.puzzle = puzzle

    @override
    def parse(self) -> gamestate.GameState:
        """
        {
            "clue": "theme",
            "startingBoard": ["OSSEDR", ..., "BOONNP"],
            "themeWords": ["THEMEWORD", ...],
            "spangram": "SPANGRAM",
            ...
        }
        """
        rows = self.puzzle["startingBoard"]
        letters = [letter for row in rows for letter in row]
        characters = gamestate.Board.characters_matrix_from_letters(
            letters, (len(rows), len(rows[0]))
        )
        return gamestate.GameState(
            board=gamestate.Board(characters),
            theme=self.puzzle["clue"],
            # themeWords does not include the spangram
            number_of_total_words=len(self.puzzle["themeWords"]) + 1,
        )


def _test() -> None:
    json_parser = JSONParser()
    print(json_parser.parse())


if __name__ == "__main__":
    _test()
