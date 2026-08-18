from pathlib import Path

from forensicflow.parsers.base import Parser


class TextParser(Parser):
    supported_extensions = frozenset({".txt", ".log", ".md"})

    def parse(self, path: Path) -> dict:
        text = path.read_text(encoding="utf-8", errors="replace")
        return {
            "type": "text",
            "path": str(path),
            "text": text,
            "line_count": len(text.splitlines()),
            "character_count": len(text),
        }
