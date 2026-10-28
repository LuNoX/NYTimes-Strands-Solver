import os

from typing import override, Optional

from strandssolver.readers import htmlreader
from strandssolver.test.data import filepaths


class StubHTMLReader(htmlreader.HTMLReader):
    DEFAULT_FILE_PATH = filepaths.strands_html_path

    def __init__(self):
        pass

    @override
    def read(self, filepath: Optional[str | bytes | os.PathLike] = None) -> str:
        if filepath is None:
            filepath = StubHTMLReader.DEFAULT_FILE_PATH
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            return html
