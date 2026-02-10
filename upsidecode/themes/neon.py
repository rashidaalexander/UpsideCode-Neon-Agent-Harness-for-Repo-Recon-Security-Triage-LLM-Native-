from rich.console import Console
from rich.panel import Panel
from rich.text import Text

BANNER = """
██╗   ██╗██████╗ ███████╗██╗██████╗ ███████╗
██║   ██║██╔══██╗██╔════╝██║██╔══██╗██╔════╝
██║   ██║██████╔╝███████╗██║██║  ██║█████╗  
██║   ██║██╔═══╝ ╚════██║██║██║  ██║██╔══╝  
╚██████╔╝██║     ███████║██║██████╔╝███████╗
 ╚═════╝ ╚═╝     ╚══════╝╚═╝╚═════╝ ╚══════╝
 ██████╗ ██████╗ ██████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝
██║     ██║   ██║██║  ██║█████╗  
██║     ██║   ██║██║  ██║██╔══╝  
╚██████╗╚██████╔╝██████╔╝███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
"""

SUB = "NEON EDITION • background agents • tool registry • sessions • telemetry • replay"

def splash(console: Console) -> None:
    panel = Panel(Text(BANNER, style="bold red"), subtitle=SUB, subtitle_align="center", border_style="red")
    console.print(panel)

def tag(console: Console, msg: str) -> None:
    console.print(f"[red]▌[/red] {msg}")
