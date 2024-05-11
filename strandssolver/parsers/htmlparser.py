import bs4

from typing import Tuple, override

from strandssolver import gamestate
from strandssolver.parsers import parser
from strandssolver.readers import htmlreader


class HTMLParser(parser.Parser):
    def __init__(self,
                 html: str = None,
                 html_reader: htmlreader.HTMLReader = None
                 ) -> None:
        if html_reader is None:
            html_reader = htmlreader.HTMLReader()
        self.html_reader = html_reader
        if html is None:
            html = self.html_reader.read()
        self._html = None
        self.html = html

    @property
    def html(self) -> str:
        return self._html

    @html.setter
    def html(self, html: str) -> None:
        self._html = html
        self.soup = bs4.BeautifulSoup(self.html, 'lxml')

    @override
    def parse(self) -> gamestate.GameState:
        theme = self._parse_theme()
        solved_words, total_words = self._parse_word_counts()
        hints, next_hint = self._parse_hint_counts()
        board = self._parse_board()
        game_state = gamestate.GameState(
            board=board,
            theme=theme,
            number_of_solved_words=solved_words,
            number_of_total_words=total_words,
            number_of_hints_available=hints,
            number_of_finds_until_next_hint=next_hint
        )
        return game_state

    def _parse_board(self) -> gamestate.Board:
        ...

    def _parse_theme(self) -> str:
        # <h1 class="umfyna_clue">theme</h1>
        theme = self.soup.find('//h1[@class="umfyna_clue"]')
        return theme.text

    def _parse_word_counts(self) -> Tuple[int, int]:
        ...

    def _parse_hint_counts(self) -> Tuple[int, int]:
        ...


def _test() -> None:
    html_parser = HTMLParser()
    print(html_parser._)


if __name__ == "__main__":
    _test()
