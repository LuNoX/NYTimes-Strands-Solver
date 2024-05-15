import bs4

from typing import Tuple, override

from strandssolver import gamestate
from strandssolver.parsers import parser
from strandssolver.readers import reader, htmlreader


class HTMLParser(parser.Parser):
    def __init__(self,
                 html: str = None,
                 html_reader: reader.Reader = None
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
        '''
        <div class="UOpmtW_board">
           <div class="F9LmoG_standard" ... data-flip-id="pulser-0" ... >
              <button class="pRjvKq_item"
                  type="button"
                  id="button-0">
                      O
              </button>
           </div>
           ...
           </div>
           <div class="F9LmoG_standard" ... data-flip-id="pulser-47" ... >
              <button class="pRjvKq_item"
                  type="button"
                  id="button-47">
                      P
              </button>
           </div>
        </div>
        '''
        board = self.soup.find("div", attrs={"class": 'UOpmtW_board'})
        buttons = board.findAll("button", attrs={"class": 'pRjvKq_item'})

        letters = []
        for button in buttons:
            index = int(button.attrs["id"].strip("button-"))
            letter = button.text
            letters.append((index, letter))
        letters = sorted(letters, key=lambda tup: tup[0])
        letters = [letter for _, letter in letters]

        char_matrix = gamestate.Board.characters_matrix_from_letters(letters)
        board = gamestate.Board(char_matrix)
        return board

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
    from test.stubs.stubhtmlreader import StubHTMLReader
    html_parser = HTMLParser(html_reader=StubHTMLReader())
    print(html_parser.parse())


if __name__ == "__main__":
    _test()
