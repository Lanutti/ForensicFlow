from __future__ import annotations

import html
import json
from pathlib import Path


def generate_json_report(analysis: dict, output: Path) -> None:
    output.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def generate_html_report(analysis: dict, output: Path) -> None:
    rows = "".join(
        f"<tr><td>{html.escape(item['name'])}</td>"
        f"<td>{html.escape(item['mime_type'])}</td>"
        f"<td>{item['size']}</td>"
        f"<td><code>{html.escape(item['sha256'])}</code></td></tr>"
        for item in analysis["files"]
    )

    correlations = "".join(
        f"<li><strong>{html.escape(item['entity_type'])}</strong>: "
        f"{html.escape(item['entity'])} "
        f"({len(item['sources'])} sources)</li>"
        for item in analysis["correlations"]
    ) or "<li>None detected.</li>"

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ForensicFlow Report</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 40px auto; padding: 0 20px; line-height: 1.5; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f4f4f4; }}
code {{ word-break: break-all; }}
</style>
</head>
<body>
<h1>ForensicFlow Analysis Report</h1>
<h2>Summary</h2>
<ul>
<li>Target: {html.escape(analysis["target"])}</li>
<li>Files: {analysis["file_count"]}</li>
<li>Extracted entities: {analysis["entity_count"]}</li>
<li>Cross-file correlations: {len(analysis["correlations"])}</li>
</ul>
<h2>Evidence Inventory</h2>
<table>
<thead><tr><th>Name</th><th>Type</th><th>Size</th><th>SHA-256</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<h2>Cross-file Correlations</h2>
<ul>{correlations}</ul>
</body>
</html>
"""
    output.write_text(document, encoding="utf-8")
