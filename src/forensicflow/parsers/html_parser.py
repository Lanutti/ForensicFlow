from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = data.strip()
        if value:
            self.parts.append(value)


class HtmlParser:
    supported_extensions = frozenset({".html", ".htm"})

    @classmethod
    def supports(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.supported_extensions

    def parse(self, path: Path) -> dict:
        content = path.read_text(encoding="utf-8", errors="replace")
        parser = _TextExtractor()
        parser.feed(content)
        return {
            "type": "html",
            "path": str(path),
            "text": "\n".join(parser.parts),
            "title": self._extract_title(content),
        }

    @staticmethod
    def _extract_title(content: str) -> str | None:
        lowered = content.lower()
        start = lowered.find("<title>")
        end = lowered.find("</title>")
        if start == -1 or end == -1 or end <= start:
            return None
        return content[start + 7:end].strip()
