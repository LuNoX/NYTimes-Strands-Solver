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
        board = self._parse_board()
        game_state = gamestate.GameState(
            board=board,
            theme=theme,
            number_of_solved_words=solved_words,
            number_of_total_words=total_words,
        )
        return game_state

    def _parse_board(self) -> gamestate.Board:
        ...

    def _parse_theme(self) -> str:
        # <h1 class="umfyna_clue">theme</h1>
        theme = self.soup.find('h1', attrs={'class': 'umfyna_clue'})
        return theme.text

    def _parse_word_counts(self) -> Tuple[int, int]:
        # <div class="XmXXwG_hint" id="hint" style="visibility: visible;">
        #   <div>...</div>
        #   <p>
        #       <b>0</b> of <b>7</b> theme words found.
        #   </p>
        #   ...
        # </div>
        hint = self.soup.find(id='hint')
        paragraph = hint.find("p", recursive=False)
        solved = paragraph.find("b")
        total = solved.findNextSibling()
        return int(solved.text), int(total.text)


def _test() -> None:
    with open("Strands_ Uncover words. - The New York Times.html",
              "r", encoding="utf-8") as f:
        html = f.read()
        html_parser = HTMLParser(html=html)
        print(html_parser._parse_theme())
        print(html_parser._parse_word_counts())


if __name__ == "__main__":
    _test()
