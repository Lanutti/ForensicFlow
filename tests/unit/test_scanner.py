from pathlib import Path

from forensicflow.scanner.file_scanner import calculate_sha256, scan_directory


def test_calculate_sha256(tmp_path: Path):
    file = tmp_path / "sample.txt"
    file.write_text("hello", encoding="utf-8")
    assert calculate_sha256(file) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_scan_directory(tmp_path: Path):
    (tmp_path / "one.txt").write_text("one", encoding="utf-8")
    (tmp_path / "two.txt").write_text("two", encoding="utf-8")
    results = scan_directory(tmp_path)
    assert len(results) == 2
