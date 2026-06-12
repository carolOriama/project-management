from rich.console import Console
from rich.panel import Panel
from datetime import datetime

console = Console()

def print_success(message):
    console.print(f"[bold green]✔[/bold green] {message}")

def print_error(message):
    console.print(f"[bold red]✘ Error:[/bold red] {message}")

def print_warning(message):
    console.print(f"[bold yellow]⚠ Warning:[/bold yellow] {message}")

def print_header(title):
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))

def parse_date(date_str):
    if not date_str:
        raise ValueError("Date cannot be empty")
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Date '{date_str}' must be in YYYY-MM-DD format (e.g., 2026-06-12)")
