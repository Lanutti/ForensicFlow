import json
from pathlib import Path

from forensicflow.parsers.base import Parser


class JsonParser(Parser):
    supported_extensions = frozenset({".json"})

    def parse(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {"type": "json", "path": str(path), "data": data}
