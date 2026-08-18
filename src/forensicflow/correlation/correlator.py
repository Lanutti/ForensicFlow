from collections import defaultdict
from dataclasses import dataclass

from forensicflow.normalization.normalizer import NormalizedEvidence


@dataclass(frozen=True)
class Correlation:
    entity_type: str
    entity: str
    sources: tuple[str, ...]


def correlate(evidence: list[NormalizedEvidence]) -> list[Correlation]:
    index = defaultdict(set)

    for item in evidence:
        for entity_type, values in item.entities.items():
            for value in values:
                index[(entity_type, value)].add(item.source_path)

    return [
        Correlation(entity_type, entity, tuple(sorted(sources)))
        for (entity_type, entity), sources in sorted(index.items())
        if len(sources) > 1
    ]