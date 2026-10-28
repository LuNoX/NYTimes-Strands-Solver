import bs4
import re

from typing import Tuple, override, Optional

from strandssolver.models import gamestate
from strandssolver.parsers import parser
from strandssolver.readers import reader, htmlreader


class HTMLParser(parser.Parser):
    def __init__(
        self, html: Optional[str] = None, html_reader: Optional[reader.Reader] = None
    ) -> None:
        if html_reader is None:
            html_reader = htmlreader.HTMLReader()
        self.html_reader = html_reader
        if html is None:
            html = self.html_reader.read()
        self._html: str
        self.html = html

    @property
    def html(self) -> str:
        return self._html

    @html.setter
    def html(self, html: str) -> None:
        self._html = html
        self.soup = bs4.BeautifulSoup(self.html, "lxml")

    @override
    def parse(self) -> gamestate.GameState:
        theme = self._parse_theme()
        solved_words, total_words = self._parse_word_counts()
        board = self._parse_board()
        game_state = gamestate.GameState(
            board=board,
            theme=theme,
            number_of_solved_words=solved_words,
            number_of_total_words=total_words,
        )
        return game_state

    def _parse_board(self) -> gamestate.Board:
        """
        <form class="styles-module_wrapper__A7No7" data-testid="strands-board">
           ...
              <button class="styles-module_item__ZXXc7"
                  type="button"
                  id="button-0"
                  data-testid="strands-letter-0">
                      O
              </button>
           ...
              <button class="styles-module_item__ZXXc7"
                  type="button"
                  id="button-47"
                  data-testid="strands-letter-47">
                      P
              </button>
           ...
        </form>
        """
        buttons = self.soup.find_all("button", id=re.compile(r"^button-\d+$"))

        letters = []
        for button in buttons:
            index = int(str(button["id"]).strip("button-"))
            letter = button.text
            letters.append((index, letter))
        letters = sorted(letters, key=lambda tup: tup[0])
        letters = [letter for _, letter in letters]

        char_matrix = gamestate.Board.characters_matrix_from_letters(letters)
        board = gamestate.Board(char_matrix)
        return board

    def _parse_theme(self) -> str:
        # <section id="riddle">
        #   <h2>
        #     <span class="riddle-module_label__OY9sx">today’s theme</span>
        #     <span class="visually-hidden">:</span>
        #     <span class="riddle-module_clue__DAHxH">theme</span>
        #   </h2>
        # </section>
        theme = self.soup.select_one('#riddle [class*="clue"]')
        if theme is None:
            raise ValueError("Could not find the theme on the page")
        return theme.text

    def _parse_word_counts(self) -> Tuple[int, int]:
        # <div class="XmXXwG_hint" id="hint" style="visibility: visible;">
        #   <div>...</div>
        #   <p>
        #       <b>0</b> of <b>7</b> theme words found.
        #   </p>
        #   ...
        # </div>
        solved, total = self.soup.select("#hint > p > b")[:2]
        return int(solved.text), int(total.text)


def _test() -> None:
    from strandssolver.test.stubs.stubhtmlreader import StubHTMLReader

    html_parser = HTMLParser(html_reader=StubHTMLReader())
    print(html_parser.parse())


if __name__ == "__main__":
    _test()
