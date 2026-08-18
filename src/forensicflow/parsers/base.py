from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Parser(ABC):
    supported_extensions: frozenset[str] = frozenset()

    @classmethod
    def supports(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.supported_extensions

    @abstractmethod
    def parse(self, path: Path) -> dict[str, Any]:
        raise NotImplementedError
