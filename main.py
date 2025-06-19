"""
This is just a simple main.py app that listens for messages on the CAN Bus.
If it recognises any message, it will decode the output and print the data for debugging.

The main point of this is to provide an example of usage and provide a quick listener tool
"""

import can
import j1939
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from datetime import datetime
from controller_applications.bender_ISO175_j1939 import ISO175_CA
from controller_applications.ivt_can_controller import IVTSensor
from controller_applications.ca_kubota_engine import Kubota_D902k_CA

# Initialize Rich console
console = Console()

# Create layout
layout = Layout()
layout.split_column(
    Layout(name="header", size=3), Layout(name="main"), Layout(name="footer", size=3)
)

layout["main"].split_row(Layout(name="status"), Layout(name="messages"))


def create_header():
    """Create the header panel"""
    header_text = Text("🚗 CAN Bus Message Listener", style="bold blue")
    subtitle = Text("Real-time J1939 message decoding and monitoring", style="italic")
    header = Panel(
        Align.center(header_text + "\n" + subtitle),
        style="blue",
        border_style="bright_blue",
    )
    return header


def create_status_panel():
    """Create the status panel with spinner"""
    status_table = Table(show_header=False, box=None, padding=(0, 1))
    status_table.add_column("Status", style="cyan")
    status_table.add_column("Value", style="green")

    current_time = datetime.now().strftime("%H:%M:%S")
    status_table.add_row("🔄 Status", "Listening for messages...")
    status_table.add_row("⏰ Time", current_time)
    status_table.add_row("📡 Interface", "can0")
    status_table.add_row("📊 Messages", "0")

    return Panel(status_table, title="📊 System Status", border_style="cyan")


def create_messages_panel():
    """Create the messages display panel"""
    messages_table = Table(show_header=True, box=None)
    messages_table.add_column("Time", style="dim", width=8)
    messages_table.add_column("PGN", style="yellow", width=8)
    messages_table.add_column("Source", style="blue", width=12)
    messages_table.add_column("Data", style="green")

    return Panel(messages_table, title="📨 Recent Messages", border_style="green")


def update_messages_table(messages_table, pgn, decoded_msg, source):
    """Update the messages table with new data"""
    current_time = datetime.now().strftime("%H:%M:%S")

    # Format the decoded message for display
    if isinstance(decoded_msg, dict):
        if "waiting" in decoded_msg:
            data_display = decoded_msg["waiting"]
        else:
            data_display = ", ".join([f"{k}: {v}" for k, v in decoded_msg.items()])
    else:
        data_display = str(decoded_msg)

    # Truncate long data for display
    if len(data_display) > 50:
        data_display = data_display[:47] + "..."

    messages_table.add_row(current_time, f"0x{pgn:04X}", source, data_display)

    # Keep only the last 10 messages
    if len(messages_table.rows) > 10:
        messages_table.rows.pop(0)


def create_footer():
    """Create the footer with controls info"""
    footer_text = Text("Press Ctrl+C to exit | Rich CAN Bus Monitor", style="dim")
    footer = Panel(Align.center(footer_text), style="dim", border_style="dim")
    return footer


# Initialize CAN bus and controller applications
console.print("[bold blue]Initializing CAN Bus Interface...[/bold blue]")

try:
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
    console.print("[green]✓[/green] CAN Bus interface initialized successfully")
except Exception as e:
    console.print(f"[red]✗[/red] Failed to initialize CAN Bus: {e}")
    exit(1)

# Initialize controller applications
console.print("[bold blue]Loading Controller Applications...[/bold blue]")

try:
    kubota = Kubota_D902k_CA("KubotaD902K")
    console.print("[green]✓[/green] Kubota D902K controller loaded")
except Exception as e:
    console.print(f"[yellow]⚠[/yellow] Kubota controller failed to load: {e}")
    kubota = None

try:
    iso_175 = ISO175_CA("ISO175")
    console.print("[green]✓[/green] ISO175 controller loaded")
except Exception as e:
    console.print(f"[yellow]⚠[/yellow] ISO175 controller failed to load: {e}")
    iso_175 = None

try:
    ivt_sensor = IVTSensor("IVT", bus=bus)
    console.print("[green]✓[/green] IVT sensor controller loaded")
except Exception as e:
    console.print(f"[yellow]⚠[/yellow] IVT sensor controller failed to load: {e}")
    ivt_sensor = None

console.print("\n[bold green]Starting CAN Bus Monitor...[/bold green]\n")

# Initialize counters
message_count = 0
decoded_msg = {"waiting": "No messages received yet"}

# Create initial layout
layout["header"].update(create_header())
layout["status"].update(create_status_panel())
layout["messages"].update(create_messages_panel())
layout["footer"].update(create_footer())

try:
    with Live(layout, refresh_per_second=4, screen=True) as live:
        console.print("[bold green]🎯 Listening for CAN messages...[/bold green]")

        while True:
            msg = bus.recv(timeout=1.0)  # Wait for a CAN message (timeout in seconds)

            if msg is None:
                # No message received, just update the display
                layout["status"].update(create_status_panel())
                continue

            message_count += 1

            # Try to extract PGN (Parameter Group Number) from the CAN message
            arbitration_id = msg.arbitration_id
            pgn = (arbitration_id >> 8) & 0xFFFF
            data = msg.data

            # Try to decode with each controller application
            source = "Unknown"
            if (
                ivt_sensor
                and hasattr(ivt_sensor, "MESSAGE_IDS")
                and pgn in ivt_sensor.MESSAGE_IDS.keys()
            ):
                decoded_msg = ivt_sensor.decode(pgn=pgn, data=data)
                source = "IVT Sensor"
            elif (
                kubota and hasattr(kubota, "decoders") and pgn in kubota.decoders.keys()
            ):
                decoded_msg = kubota.decode(pgn=pgn, data=data)
                source = "Kubota Engine"
            elif (
                iso_175
                and hasattr(iso_175, "decoders")
                and pgn in iso_175.decoders.keys()
            ):
                decoded_msg = iso_175.decode(pgn=pgn, data=data)
                source = "ISO175"
            else:
                console.print(
                    f"[yellow]⚠[/yellow] No decoder found for PGN: 0x{pgn:04X}"
                )
                decoded_msg = {"unknown_pgn": pgn, "raw_data": data.hex()}
                source = "Unknown"

            # Update the messages table
            messages_table = Table(show_header=True, box=None)
            messages_table.add_column("Time", style="dim", width=8)
            messages_table.add_column("PGN", style="yellow", width=8)
            messages_table.add_column("Source", style="blue", width=12)
            messages_table.add_column("Data", style="green")

            # Add the new message
            update_messages_table(messages_table, pgn, decoded_msg, source)

            # Update status panel with new message count
            status_table = Table(show_header=False, box=None, padding=(0, 1))
            status_table.add_column("Status", style="cyan")
            status_table.add_column("Value", style="green")

            current_time = datetime.now().strftime("%H:%M:%S")
            status_table.add_row("🔄 Status", "Message received!")
            status_table.add_row("⏰ Time", current_time)
            status_table.add_row("📡 Interface", "can0")
            status_table.add_row("📊 Messages", str(message_count))

            # Update layout
            layout["status"].update(
                Panel(status_table, title="📊 System Status", border_style="cyan")
            )
            layout["messages"].update(
                Panel(messages_table, title="📨 Recent Messages", border_style="green")
            )

            # Log the decoded message to console as well
            console.print(
                f"[bold blue]📨[/bold blue] PGN: [yellow]0x{pgn:04X}[/yellow] | Source: [blue]{source}[/blue] | Data: [green]{decoded_msg}[/green]"
            )

except KeyboardInterrupt:
    console.print("\n[bold red]🛑 Stopped by user.[/bold red]")
    console.print("[yellow]Shutting down CAN Bus interface...[/yellow]")
    bus.shutdown()
    console.print("[green]✓[/green] Cleanup completed. Goodbye!")
