from __future__ import annotations

import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class EvidenceFile(BaseModel):
    model_config = ConfigDict(frozen=True)

    path: str
    name: str
    extension: str
    mime_type: str
    size: int
    sha256: str
    modified_at: datetime


def calculate_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def scan_file(path: Path) -> EvidenceFile:
    stat = path.stat()
    mime_type, _ = mimetypes.guess_type(path.name)
    return EvidenceFile(
        path=str(path),
        name=path.name,
        extension=path.suffix.lower(),
        mime_type=mime_type or "application/octet-stream",
        size=stat.st_size,
        sha256=calculate_sha256(path),
        modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
    )


def scan_directory(directory: Path) -> list[EvidenceFile]:
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    files = [p for p in directory.rglob("*") if p.is_file() and p.name != ".gitkeep"]
    return [scan_file(p) for p in sorted(files)]
