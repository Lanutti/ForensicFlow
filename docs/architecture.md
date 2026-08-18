# ForensicFlow Architecture

## Pipeline

```text
Scanner -> Parsers -> Normalization -> Correlation -> Analysis -> Reporting
```

### Scanner

Discovers files recursively and collects path, name, extension, MIME type, size, SHA-256 and modification time.

### Parsers

Converts supported formats into structured Python data.

Supported formats:

- TXT
- LOG
- MD
- JSON
- CSV
- HTML
- PDF (optional dependency)

### Normalization

Converts parser-specific data into `NormalizedEvidence` and extracts common entities:

- email addresses
- IP addresses
- URLs
- timestamps

### Correlation

Finds entities that occur in multiple evidence sources.

### Analysis

Orchestrates the complete processing pipeline.

### Reporting

Produces JSON or HTML output.

## Security

Real sensitive evidence must never be committed. Development data should be synthetic and authorized.
