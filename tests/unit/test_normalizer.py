from pathlib import Path

from forensicflow.normalization.normalizer import extract_entities, normalize


def test_extract_entities():
    text = "admin@example.com 192.168.1.10 https://example.com 2026-08-18T14:30:00Z"
    entities = extract_entities(text)
    assert "admin@example.com" in entities["emails"]
    assert "192.168.1.10" in entities["ip_addresses"]
    assert "https://example.com" in entities["urls"]
    assert "2026-08-18T14:30:00Z" in entities["timestamps"]


def test_normalize():
    result = normalize({"type": "text", "text": "user@example.com"}, Path("evidence.txt"))
    assert result.entities["emails"] == ["user@example.com"]
