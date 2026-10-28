from typing import override, Optional

from strandssolver.parsers import htmlparser
from strandssolver.readers import reader
from strandssolver.test.stubs import stubhtmlreader


class StubHTMLParser(htmlparser.HTMLParser):
    @override
    def __init__(
        self, html: Optional[str] = None, html_reader: Optional[reader.Reader] = None
    ) -> None:
        if html_reader is None:
            html_reader = stubhtmlreader.StubHTMLReader()
        super().__init__(html=html, html_reader=html_reader)
