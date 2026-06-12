from rich.console import Console
from rich.panel import Panel
from datetime import datetime

console = Console()

def print_success(message: str):
    console.print(f"[bold green]✔[/bold green] {message}")

def print_error(message: str):
    console.print(f"[bold red]✘ Error:[/bold red] {message}")

def print_warning(message: str):
    console.print(f"[bold yellow]⚠ Warning:[/bold yellow] {message}")

def print_header(title: str):
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))

def parse_date(date_str: str) -> str:
    """
    Parses and normalizes a date string to YYYY-MM-DD.
    Raises ValueError if invalid.
    """
    if not date_str:
        raise ValueError("Date cannot be empty")
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Date '{date_str}' must be in YYYY-MM-DD format (e.g., 2026-06-12)")
