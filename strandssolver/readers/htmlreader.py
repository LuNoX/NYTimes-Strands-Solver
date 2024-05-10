import requests

from typing import Tuple, override

from strandssolver import gamestate
from strandssolver.readers import reader


class HtmlReader(reader.Reader):
    default_strands_url = "https://www.nytimes.com/games/strands"

    @staticmethod
    @override
    def read(url: str | bytes = None) -> gamestate.GameState:
        response = HtmlReader._get_html(url)
        theme = HtmlReader._get_theme_from_response(response)
        solved_words, total_words = HtmlReader._get_word_counts_from_response(
            response)
        hints, next_hint = HtmlReader._get_hint_counts_from_response(response)
        board = HtmlReader._get_board_from_response(response)
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
    def _get_html(url: str | bytes = None) -> requests.Response:
        if url is None:
            url = HtmlReader.default_strands_url
        response = requests.get(url)
        return response

    @staticmethod
    def _get_board_from_response(response: requests.Response
                                 ) -> gamestate.Board:
        ...

    @staticmethod
    def _get_theme_from_response(response: requests.Response) -> str:
        ...

    @staticmethod
    def _get_word_counts_from_response(response: requests.Response
                                       ) -> Tuple[int, int]:
        ...

    @staticmethod
    def _get_hint_counts_from_response(response: requests.Response
                                       ) -> Tuple[int, int]:
        ...


def _test() -> None:
    response = HtmlReader.read()
    print(response)


if __name__ == "__main__":
    _test()
