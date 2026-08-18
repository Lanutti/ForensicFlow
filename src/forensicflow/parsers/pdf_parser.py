from pathlib import Path


class PdfParser:
    """Optional PDF parser using pypdf."""

    supported_extensions = frozenset({".pdf"})

    @classmethod
    def supports(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.supported_extensions

    def parse(self, path: Path) -> dict:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError(
                "PDF support requires pypdf. Install with: pip install -e '.[pdf]'"
            ) from exc

        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return {
            "type": "pdf",
            "path": str(path),
            "page_count": len(reader.pages),
            "text": text,
        }
