import datetime
import json
import urllib.request

from typing import Any, Dict, override

from strandssolver.readers import reader


class JSONReader(reader.Reader):
    DEFAULT_URL_TEMPLATE = "https://www.nytimes.com/svc/strands/v2/{date}.json"
    DEFAULT_TIMEOUT_IN_SECONDS = 10.0

    def __init__(self,
                 url_template: str = DEFAULT_URL_TEMPLATE,
                 timeout_in_seconds: float = DEFAULT_TIMEOUT_IN_SECONDS
                 ) -> None:
        self.url_template = url_template
        self.timeout_in_seconds = timeout_in_seconds

    @override
    def read(self, date: datetime.date = None) -> Dict[str, Any]:
        if date is None:
            date = datetime.date.today()
        url = self.url_template.format(date=date.isoformat())
        with urllib.request.urlopen(url,
                                    timeout=self.timeout_in_seconds) as response:
            return json.load(response)


def _test() -> None:
    json_reader = JSONReader()
    print(json_reader.read())


if __name__ == "__main__":
    _test()
