import csv
from pathlib import Path

from forensicflow.parsers.base import Parser


class CsvParser(Parser):
    supported_extensions = frozenset({".csv"})

    def parse(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        return {
            "type": "csv",
            "path": str(path),
            "columns": reader.fieldnames or [],
            "rows": rows,
            "row_count": len(rows),
        }
