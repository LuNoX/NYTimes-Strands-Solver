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
        self.html = html

    @override
    def parse(self) -> gamestate.GameState:
        soup = bs4.BeautifulSoup(self.html, 'lxml')
        theme = HTMLParser._get_theme_from_response(soup)
        solved_words, total_words = HTMLParser._get_word_counts_from_response(
            soup)
        hints, next_hint = HTMLParser._get_hint_counts_from_response(soup)
        board = HTMLParser._get_board_from_response(soup)
        game_state = gamestate.GameState(
            board=board,
            theme=theme,
            number_of_solved_words=solved_words,
            number_of_total_words=total_words,
            number_of_hints_available=hints,
            number_of_finds_until_next_hint=next_hint
        )
        return game_state

    @staticmethod
    def _get_board_from_response(tree
                                 ) -> gamestate.Board:
        ...

    @staticmethod
    def _get_theme_from_response(tree) -> str:
        # <h1 class="umfyna_clue">theme</h1>
        theme = tree.xpath('//h1[@class="umfyna_clue"]')
        if len(theme) > 1:
            raise ValueError('Multiple themes found')
        return theme[0].text

    @staticmethod
    def _get_word_counts_from_response(tree
                                       ) -> Tuple[int, int]:
        ...

    @staticmethod
    def _get_hint_counts_from_response(tree
                                       ) -> Tuple[int, int]:
        ...


def _test() -> None:
    # with open("Strands_ Uncover words. - The New York Times.html",
    #           "r", encoding='utf-8') as f:
    #     tree = html.fromstring(f.read())
    #     print(HtmlReader._get_theme_from_response(tree))
    ...


if __name__ == "__main__":
    _test()
