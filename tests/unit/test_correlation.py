from pathlib import Path

from forensicflow.correlation.correlator import correlate
from forensicflow.normalization.normalizer import normalize


def test_cross_file_correlation():
    first = normalize({"type": "text", "text": "Connection from 10.0.0.5"}, Path("one.txt"))
    second = normalize({"type": "text", "text": "Blocked 10.0.0.5"}, Path("two.txt"))
    result = correlate([first, second])
    assert len(result) == 1
    assert result[0].entity == "10.0.0.5"
