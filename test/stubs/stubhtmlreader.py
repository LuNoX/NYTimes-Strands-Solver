import os

from importlib import resources

from strandssolver.readers import reader
from test import data


class StubHTMLReader(reader.Reader):
    DEFAULT_FILE_PATH = resources.files(data).joinpath(
        'Strands_ Uncover words. - The New York Times.html')

    def read(self, filepath: str | bytes | os.PathLike = None) -> str:
        if filepath is None:
            filepath = StubHTMLReader.DEFAULT_FILE_PATH
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            return html
