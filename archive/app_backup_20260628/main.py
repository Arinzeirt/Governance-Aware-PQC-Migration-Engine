import typer
from rich.console import Console
from scanner import scan_directory
from inventory import save_inventory
from report import generate_report

app = typer.Typer()
console = Console()

@app.command()
def scan(path: str):
    console.print(f"[bold green]Scanning:[/bold green] {path}")

    findings = scan_directory(path)
    inventory = save_inventory(findings)
    generate_report(inventory)

    if not inventory:
        console.print("[yellow]No cryptographic indicators found.[/yellow]")
        return

    for item in inventory:
        console.print(f"\n[bold cyan]{item['file']}[/bold cyan]")

        if item["finding_type"] == "keyword":
            console.print(f"  • Keyword: {item['algorithm']}")
            console.print(f"    Risk: {item['risk']}")
            console.print(f"    Status: {item['pqc_status']}")

        elif item["finding_type"] == "classification":
            console.print(f"  • Asset Type: {item['asset_type']}")
            console.print(f"    Classification: {item['classification']}")
            console.print(f"    PQC Relevance: {item['pqc_relevance']}")
            console.print(f"    Readiness Score: {item['readiness_score']}/100")
            console.print(f"    Urgency: {item['urgency']}")
            console.print(f"    Coverage Status: {item['coverage_status']}")
            console.print(f"    Coverage Reason: {item['coverage_reason']}")
            console.print(f"    Priority: {item['priority']}")
            console.print(f"    Recommendation: {item['recommendation']}")
            console.print(f"    Timeline: {item['timeline']}")
            console.print(f"    Owner: {item['owner']}")
            console.print(f"    Criticality: {item['criticality']}")
            console.print(f"    Approver: {item['approver']}")
            console.print(f"    Evidence Required: {item['evidence']}")
            console.print(f"    Migration Status: {item['migration_status']}")

    console.print("\n[bold green]Inventory saved to inventory.json[/bold green]")
    console.print("[bold green]Report saved to reports/pqc_report.txt[/bold green]")

if __name__ == "__main__":
    app()
