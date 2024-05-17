from typing import override

from strandssolver.parsers import htmlparser
from strandssolver.readers import reader
from strandssolver.test.stubs import stubhtmlreader


class StubHTMLParser(htmlparser.HTMLParser):
    @override
    def __init__(self,
                 html: str = None,
                 html_reader: reader.Reader = None
                 ) -> None:
        if html_reader is not None:
            html_reader = stubhtmlreader.StubHTMLReader()
        super().__init__(html=html, html_reader=html_reader)
