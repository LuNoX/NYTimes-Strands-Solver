import bs4
import time

from datetime import timedelta
from typing import Tuple, override
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from strandssolver import gamestate
from strandssolver.parsers import parser


class HTMLParser(parser.Parser):
    default_strands_url = "https://www.nytimes.com/games/strands"

    def __int__(self):
        ...

    @override
    def parse(self, url: str | bytes = None) -> gamestate.GameState:
        html = HTMLParser._get_html(url)
        soup = bs4.BeautifulSoup(html, 'lxml')
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
    def _get_html(url: str | bytes = None,
                  max_attempts: int = 5,
                  time_between_attempts: float | timedelta = 5,
                  load_complete_when_this_str_is_present: str = "TODAY’S THEME"
                  ) -> str:
        if url is None:
            url = HTMLParser.default_strands_url
        if isinstance(time_between_attempts, timedelta):
            time_between_attempts = timedelta.total_seconds()

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        html = driver.page_source
        # Previous line is the first attempt, so entering the loop is attempt 2
        for attempt in range(2, max_attempts + 1):
            if load_complete_when_this_str_is_present.lower() in html.lower():
                break
            if attempt == max_attempts:
                raise TimeoutError(
                    f"Request timed out after {max_attempts} attempts."
                )
            time.sleep(time_between_attempts)
            html = driver.page_source

        return html

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
    print(HTMLParser._get_html())


if __name__ == "__main__":
    _test()
