import json

from forensicflow.parsers.csv_parser import CsvParser
from forensicflow.parsers.json_parser import JsonParser
from forensicflow.parsers.text_parser import TextParser


def test_text_parser(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("hello\nworld", encoding="utf-8")
    result = TextParser().parse(file)
    assert result["line_count"] == 2


def test_json_parser(tmp_path):
    file = tmp_path / "sample.json"
    file.write_text(json.dumps({"ip": "192.168.1.1"}), encoding="utf-8")
    result = JsonParser().parse(file)
    assert result["data"]["ip"] == "192.168.1.1"


def test_csv_parser(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text("name,ip\nserver,10.0.0.1\n", encoding="utf-8")
    result = CsvParser().parse(file)
    assert result["rows"][0]["ip"] == "10.0.0.1"
