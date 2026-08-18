from pathlib import Path
from typing import Any

from forensicflow.correlation.correlator import correlate
from forensicflow.normalization.normalizer import NormalizedEvidence, normalize
from forensicflow.parsers.csv_parser import CsvParser
from forensicflow.parsers.html_parser import HtmlParser
from forensicflow.parsers.json_parser import JsonParser
from forensicflow.parsers.pdf_parser import PdfParser
from forensicflow.parsers.text_parser import TextParser
from forensicflow.scanner.file_scanner import EvidenceFile, scan_directory

PARSERS = (CsvParser(), JsonParser(), HtmlParser(), TextParser(), PdfParser())


def parse_file(path: Path) -> dict[str, Any]:
    for parser in PARSERS:
        if parser.supports(path):
            return parser.parse(path)
    return {"type": "binary", "path": str(path), "text": ""}


def normalize_files(files: list[EvidenceFile]) -> list[NormalizedEvidence]:
    result = []
    for item in files:
        path = Path(item.path)
        try:
            result.append(normalize(parse_file(path), path))
        except Exception as exc:
            result.append(
                NormalizedEvidence(
                    source_path=str(path),
                    evidence_type="error",
                    entities={"errors": [str(exc)]},
                )
            )
    return result


def analyze_evidence(directory: Path, files: list[EvidenceFile] | None = None) -> dict:
    evidence_files = files if files is not None else scan_directory(directory)
    normalized = normalize_files(evidence_files)
    correlations = correlate(normalized)

    return {
        "target": str(directory),
        "file_count": len(evidence_files),
        "entity_count": sum(
            len(values) for item in normalized for values in item.entities.values()
        ),
        "files": [item.model_dump(mode="json") for item in evidence_files],
        "normalized": [item.model_dump(mode="json") for item in normalized],
        "correlations": [
            {
                "entity_type": item.entity_type,
                "entity": item.entity,
                "sources": list(item.sources),
            }
            for item in correlations
        ],
    }
