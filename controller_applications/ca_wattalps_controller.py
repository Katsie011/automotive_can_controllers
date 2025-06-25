import can
import logging
from wattalps.decode_msg import (
    MESSAGE_ID_TO_CLASS,
    decode_message_from_id,
    MESSAGE_DECODERS,
)


if __name__ == "__main__":
    import sys
    import random

    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.spinner import Spinner
    import time

    TEST_MODE = True

    console = Console()
    logging.basicConfig(level=logging.INFO)

    # CAN bus setup
    try:
        if not TEST_MODE:
            bus = can.interface.Bus(channel="can0", bustype="socketcan", bitrate=500000)
        else:
            console.print("Connecting to bus")
    except Exception as e:
        console.print(f"[bold red]Failed to connect to CAN bus: {e}[/bold red]")
        sys.exit(1)

    console.print(
        Panel.fit(
            "[bold green]Wattalps CAN Decoder[/bold green]\nListening for CAN messages on [yellow]can0[/yellow]...\nPress [bold]Ctrl+C[/bold] to exit.",
            title="CAN Bus Monitor",
            border_style="green",
        )
    )

    def render_table(decoded_messages):
        table = Table(title="Decoded CAN Messages", show_lines=True, expand=True)
        table.add_column("Time", style="cyan", no_wrap=True)
        table.add_column("Message ID", style="magenta")
        table.add_column("Decoded Data", style="green")
        for msg_time, msg_id, decoded in decoded_messages[-10:]:
            table.add_row(
                time.strftime("%H:%M:%S", time.localtime(msg_time)),
                f"0x{msg_id:X}",
                str(decoded) if decoded else "[dim]N/A[/dim]",
            )
        return table

    decoded_messages = []
    spinner = Spinner("dots", text="Waiting for CAN messages...")

    with Live(spinner, refresh_per_second=10, console=console) as live:
        try:
            while True:
                if not TEST_MODE:
                    msg = bus.recv(timeout=1.0)
                else:
                    msg = "Testing the TUI!"

                if msg is None:
                    # No message, keep spinner
                    live.update(Spinner("dots", text="Waiting for CAN messages..."))
                    continue

                if not TEST_MODE:
                    msg_id = msg.arbitration_id  # type: ignore
                    data = msg.data  # type: ignore
                else:
                    target_id = random.randint(0, len(MESSAGE_DECODERS) - 1)
                    # print(f"Target id: {target_id}")
                    msg_id = list(MESSAGE_DECODERS.keys())[target_id]
                    # print(f"{msg_id=}")
                    data = random.randbytes(MESSAGE_ID_TO_CLASS[msg_id].NUM_BYTES)
                    # print(f"{data=}")
                    console.print(f"DATA: {data}")
                    time.sleep(1)

                decoded = None
                try:
                    decoded = decode_message_from_id(message_id=msg_id, data=data)
                    if not decoded:
                        decoded = "[dim]No decode available[/dim]"
                except Exception as e:
                    decoded = f"[bold red]Decode error:[/bold red] {e}"

                decoded_messages.append((time.time(), msg_id, decoded))
                live.update(render_table(decoded_messages))
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Exiting CAN monitor. Goodbye![/bold yellow]")
        except Exception as e:
            console.print(f"[bold red]Unexpected error: {e}[/bold red]")
