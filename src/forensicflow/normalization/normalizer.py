from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
URL_RE = re.compile(r'https?://[^\s<>\'"]+')
TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?\b"
)


class NormalizedEvidence(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_path: str
    evidence_type: str
    text: str = ""
    entities: dict[str, list[str]] = Field(default_factory=dict)
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def extract_entities(text: str) -> dict[str, list[str]]:
    return {
        "emails": sorted(set(EMAIL_RE.findall(text))),
        "ip_addresses": sorted(set(IP_RE.findall(text))),
        "urls": sorted(set(URL_RE.findall(text))),
        "timestamps": sorted(set(TIMESTAMP_RE.findall(text))),
    }


def normalize(parsed: dict[str, Any], source: Path) -> NormalizedEvidence:
    evidence_type = str(parsed.get("type", "unknown"))
    text = str(parsed.get("text", ""))

    if not text and evidence_type == "json":
        text = json.dumps(parsed.get("data"), ensure_ascii=False, default=str)

    if not text and evidence_type == "csv":
        text = json.dumps(parsed.get("rows", []), ensure_ascii=False, default=str)

    return NormalizedEvidence(
        source_path=str(source),
        evidence_type=evidence_type,
        text=text,
        entities=extract_entities(text),
    )
