import os

from importlib import resources
from typing import override

from strandssolver.readers import htmlreader
from strandssolver.test import data
from strandssolver.test.data import filenames


class StubHTMLReader(htmlreader.HTMLReader):
    DEFAULT_FILE_PATH = resources.files(data).joinpath(filenames.strands_html)

    @override
    def __init__(self):
        pass

    @override
    def read(self, filepath: str | bytes | os.PathLike = None) -> str:
        if filepath is None:
            filepath = StubHTMLReader.DEFAULT_FILE_PATH
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            return html

    @override
    def _setup_webdriver(self) -> None:
        """
        Stub method
        """
        pass

    @override
    def _get_html_source(self) -> None:
        """
        Stub method
        """
        pass
