from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from forensicflow.analysis.analyzer import analyze_evidence
from forensicflow.reporting.report import generate_html_report, generate_json_report
from forensicflow.scanner.file_scanner import scan_directory

app = typer.Typer(name="forensicflow", help="Digital evidence collection and analysis toolkit.")
console = Console()


@app.command()
def version() -> None:
    """Show the application version."""
    from forensicflow import __version__
    console.print(f"ForensicFlow {__version__}")


@app.command()
def scan(
    directory: Path = typer.Argument(..., exists=True, file_okay=False, readable=True)
) -> None:
    """Scan a directory and display file metadata."""
    evidence = scan_directory(directory)
    if not evidence:
        console.print("[yellow]No files found.[/yellow]")
        return

    table = Table(title="Evidence Inventory")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Size", justify="right")
    table.add_column("SHA-256")

    for item in evidence:
        table.add_row(item.name, item.mime_type, str(item.size), item.sha256[:16] + "...")

    console.print(table)
    console.print(f"\nFiles discovered: {len(evidence)}")


@app.command()
def report(
    directory: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    output: Path = typer.Option(Path("reports/report.html"), "--output", "-o"),
    format: str = typer.Option("html", "--format", "-f"),
) -> None:
    """Analyze evidence and generate a report."""
    evidence = scan_directory(directory)
    analysis = analyze_evidence(directory, evidence)
    output.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == "json":
        generate_json_report(analysis, output)
    elif format.lower() == "html":
        generate_html_report(analysis, output)
    else:
        raise typer.BadParameter("format must be 'html' or 'json'")

    console.print(f"[green]Report generated:[/green] {output}")


if __name__ == "__main__":
    app()
