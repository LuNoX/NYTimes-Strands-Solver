import asyncio

from typing import override, List
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from strandssolver.readers import reader


class HTMLReader(reader.Reader):
    DEFAULT_URL = "https://www.nytimes.com/games/strands"
    DEFAULT_MAX_ATTEMPTS = 5
    DEFAULT_TIME_BETWEEN_ATTEMPTS = 5.0
    DEFAULT_WEBDRIVER_ARGUMENTS = ["--headless=new"]
    DEFAULT_LOAD_COMPLETE_WHEN_HTML_CONTAINS_THIS = "TODAY’S THEME"

    def __init__(self,
                 url: str | bytes = DEFAULT_URL,
                 max_attempts: int = DEFAULT_MAX_ATTEMPTS,
                 webdriver_arguments: List[str] = None,
                 seconds_between_attempts: float | datetime.timedelta =
                 DEFAULT_TIME_BETWEEN_ATTEMPTS,
                 load_complete_when_html_contains_this: str =
                 DEFAULT_LOAD_COMPLETE_WHEN_HTML_CONTAINS_THIS
                 ) -> None:
        self.url = url
        self.max_attempts = max_attempts
        self._seconds_between_attempts = None
        self.seconds_between_attempts = seconds_between_attempts
        self.load_complete_when_html_contains_this = \
            load_complete_when_html_contains_this
        if webdriver_arguments is None:
            webdriver_arguments = HTMLReader.DEFAULT_WEBDRIVER_ARGUMENTS
        self.webdriver_arguments = webdriver_arguments
        self.webdriver = self._setup_webdriver()

    def _setup_webdriver(self) -> webdriver.Chrome:
        chrome_options = Options()
        for argument in self.webdriver_arguments:
            chrome_options.add_argument(argument)
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    @property
    def seconds_between_attempts(self) -> float:
        return self._seconds_between_attempts

    @seconds_between_attempts.setter
    def seconds_between_attempts(self, seconds: float | datetime.timedelta
                                 ) -> None:
        if isinstance(seconds, datetime.timedelta):
            seconds = seconds.total_seconds()
        self._seconds_between_attempts = seconds

    @override
    def read(self, url: str | bytes = None) -> str:
        if url is None:
            url = self.url
        self.webdriver.get(url)
        html = asyncio.run(self._get_html_source())
        return html

    async def _get_html_source(self) -> str:
        html = self.webdriver.page_source
        # Previous line is the first attempt, so entering the loop is attempt 2
        for _ in range(2, self.max_attempts + 1):
            if self.load_complete_when_html_contains_this.lower(
            ) in html.lower():
                return html
            await asyncio.sleep(self.seconds_between_attempts)
            html = self.webdriver.page_source
        raise TimeoutError(
            f"Request timed out after {self.max_attempts} attempts."
        )


def _test() -> None:
    html_reader = HTMLReader()
    print(html_reader.read())


if __name__ == "__main__":
    _test()
