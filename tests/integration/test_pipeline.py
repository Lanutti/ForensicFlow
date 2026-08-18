from pathlib import Path

from forensicflow.analysis.analyzer import analyze_evidence


def test_full_analysis_pipeline(tmp_path: Path):
    (tmp_path / "one.txt").write_text(
        "Connection from 10.0.0.5 by admin@example.com",
        encoding="utf-8",
    )
    (tmp_path / "two.txt").write_text("Blocked 10.0.0.5", encoding="utf-8")
    result = analyze_evidence(tmp_path)
    assert result["file_count"] == 2
    assert result["correlations"]
