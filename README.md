# ForensicFlow

A Python-based digital evidence analysis platform for file scanning, data extraction, normalization, correlation, and automated reporting.

> Portfolio project. ForensicFlow is educational software and does not claim legal or evidentiary validity.

## Features

- Recursive evidence-directory scanning
- SHA-256 hashing
- File metadata collection
- CSV, JSON, HTML, TXT, and optional PDF parsing
- Evidence normalization
- Extraction of IPs, URLs, emails, and timestamps
- Cross-file correlation
- JSON and HTML reports
- CLI interface
- Unit and integration tests

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/YOUR_USERNAME/forensicflow.git
cd forensicflow
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e ".[dev]"
```

Optional PDF support:

```bash
python -m pip install -e ".[pdf]"
```

## Usage

```bash
python -m forensicflow.cli --help
python -m forensicflow.cli version
python -m forensicflow.cli scan examples/evidence
python -m forensicflow.cli report examples/evidence --output reports/report.html
python -m forensicflow.cli report examples/evidence --format json --output reports/report.json
```

## Architecture

```text
Evidence Directory
       |
       v
 File Scanner
       |
       v
    Parsers
       |
       v
 Normalization
       |
       v
  Correlation
       |
       v
   Analysis
       |
       v
  Reporting
```

## Structure

```text
forensicflow/
├── src/forensicflow/
│   ├── __init__.py
│   ├── cli.py
│   ├── scanner/
│   ├── parsers/
│   ├── normalization/
│   ├── correlation/
│   ├── analysis/
│   └── reporting/
├── tests/
│   ├── unit/
│   └── integration/
├── examples/evidence/
├── reports/
├── docs/
├── pyproject.toml
├── README.md
├── .gitignore
├── .env.example
└── LICENSE
```

## Development

```bash
pytest
pytest --cov=forensicflow --cov-report=term-missing
```

## Roadmap

- [x] Project architecture
- [x] CLI
- [x] File scanner
- [x] SHA-256 hashing
- [x] TXT/LOG/MD parser
- [x] JSON parser
- [x] CSV parser
- [x] HTML parser
- [x] Optional PDF parser
- [x] Normalization
- [x] Entity extraction
- [x] Cross-file correlation
- [x] JSON/HTML reporting
- [ ] FastAPI service
- [ ] Persistent storage
- [ ] Background processing
- [ ] Docker deployment
- [ ] Web dashboard
- [ ] CI/CD

## Disclaimer

Only analyze data you are authorized to process. ForensicFlow is not a replacement for validated forensic tooling, chain-of-custody procedures, legal processes, or expert examination.

## License

MIT. See `LICENSE`.
