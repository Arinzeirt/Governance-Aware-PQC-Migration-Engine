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

    if not findings:
        console.print("[yellow]No cryptographic indicators found.[/yellow]")
        return

    for file_path, matches in findings.items():
        console.print(f"\n[bold cyan]{file_path}[/bold cyan]")

        for match in matches:
            console.print(f"  • {match}")

    console.print("\n[bold green]Inventory saved to inventory.json[/bold green]")
    console.print("[bold green]Report saved to reports/pqc_report.txt[/bold green]")

if __name__ == "__main__":
    app()
