import sys
import time
import os
import csv

import random

sys.path.extend(os.path.basename(os.path.basename(__file__)))
from controller_applications.wattalps.messages.msg_status import (
    VmuBmsStatus,
    encode_vmu_bms_status,
    decode_vmu_bms_status,
    BmsVmuStatus,
    encode_bms_vmu_status,
    decode_bms_vmu_status,
)

try:
    import can
except ImportError:
    can = None


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def format_bms_vmu_status(decoded):
    """Format BmsVmuStatus as a rich Table for pretty printing."""
    table = Table(
        show_header=False, box=None, show_lines=False, expand=False, padding=(0, 1)
    )
    table.add_row("charge_phase", str(decoded.charge_phase))
    table.add_row("is_thermal_forcing", str(decoded.is_thermal_forcing))
    table.add_row("is_cooling", str(decoded.is_cooling))
    table.add_row("is_pumping", str(decoded.is_pumping))
    table.add_row("is_heating", str(decoded.is_heating))
    table.add_row("is_dc_contactor_closed", str(decoded.is_dc_contactor_closed))
    table.add_row("is_end_of_charge", str(decoded.is_end_of_charge))
    table.add_row("is_balancing", str(decoded.is_balancing))
    table.add_row("is_alert", str(decoded.is_alert))
    table.add_row("is_warning", str(decoded.is_warning))
    table.add_row("is_failure", str(decoded.is_failure))
    table.add_row("soc", str(decoded.soc))
    table.add_row("mode", str(decoded.mode))
    return table


def test_vmu_bms_status_hil(
    test_mode=False,
    can_channel="can0",
    bustype="socketcan",
    bitrate=500000,
    log_dir="./logs/hil_logs",
):
    """
    Hardware-in-the-loop test for VMU_BMS_STATUS and BMS_VMU_STATUS messages.
    Sends all possible VMU_BMS_STATUS requests and logs all responses.
    If test_mode is True, simulates CAN bus and responses.
    """
    console = Console()
    # Prepare log file
    log_dir = os.path.join(log_dir, "simulated") if test_mode else log_dir
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(
        log_dir, f"hil_log_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    )
    log_file = open(log_filename, mode="w", newline="")
    csv_writer = csv.writer(log_file)
    csv_writer.writerow(["timestamp", "direction", "msg_id", "data_hex", "decoded"])

    # Prepare CAN bus
    bus = None
    if not test_mode:
        if can is None:
            console.print(
                "[bold red]python-can is required for hardware mode.[/bold red]"
            )
            log_file.close()
            return
        try:
            bus = can.interface.Bus(
                channel=can_channel, bustype=bustype, bitrate=bitrate
            )
            console.print(
                f"[bold green]Connected to CAN bus[/bold green] [cyan]{can_channel}[/cyan] "
                f"([magenta]{bustype}[/magenta]) at [yellow]{bitrate}[/yellow] bps"
            )
        except Exception as e:
            console.print(f"[bold red]Failed to connect to CAN bus:[/bold red] {e}")
            log_file.close()
            return
    else:
        console.print("[bold yellow]Running in simulation/offline mode.[/bold yellow]")

    # Prepare all VMU_BMS_STATUS requests to send
    vmu_bms_status_requests = [
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=False,
            ask_mode=VmuBmsStatus.ASK_MODE_STANDBY,
        ),
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=False,
            ask_mode=VmuBmsStatus.ASK_MODE_CHARGE,
        ),
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=False,
            ask_mode=VmuBmsStatus.ASK_MODE_DRIVE,
        ),
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=True,
            ask_mode=VmuBmsStatus.ASK_MODE_STANDBY,
        ),
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=True,
            ask_mode=VmuBmsStatus.ASK_MODE_CHARGE,
        ),
        VmuBmsStatus(
            bms_dest_addr=0x01,
            insu_res_meas_en=True,
            ask_mode=VmuBmsStatus.ASK_MODE_DRIVE,
        ),
    ]

    # Send each request and listen for responses
    for req in vmu_bms_status_requests:
        encoded = encode_vmu_bms_status(req)
        msg_id = VmuBmsStatus.MESSAGE_ID
        data_hex = encoded.hex()
        timestamp = time.time()
        csv_writer.writerow([timestamp, "TX", f"0x{msg_id:X}", data_hex, str(req)])
        log_file.flush()

        time.sleep(1)
        req_text = Text(f"Sending VMU_BMS_STATUS: ", style="bold blue")
        req_text.append(str(req), style="cyan")
        req_text.append(f" (hex: ", style="bold blue")
        req_text.append(data_hex, style="magenta")
        req_text.append(")", style="bold blue")
        console.print(req_text)

        if not test_mode:
            msg = can.Message(arbitration_id=msg_id, data=encoded, is_extended_id=False)
            try:
                bus.send(msg)
            except Exception as e:
                console.print(f"[bold red]Failed to send message:[/bold red] {e}")
                continue
        else:
            # Simulate sending
            time.sleep(0.1)

        # Listen for responses for a short period
        start_time = time.time()
        timeout = 2.0  # seconds to listen for a response
        while time.time() - start_time < timeout:
            if not test_mode:
                rx_msg = bus.recv(timeout=0.2)
                if rx_msg is None:
                    continue
                rx_id = rx_msg.arbitration_id
                rx_data = rx_msg.data
            else:
                # Simulate a BMS_VMU_STATUS response
                rx_id = BmsVmuStatus.MESSAGE_ID
                # Simulate a plausible response
                rx_obj = BmsVmuStatus(
                    charge_phase=random.randint(0, 6),
                    is_thermal_forcing=bool(random.getrandbits(1)),
                    is_cooling=bool(random.getrandbits(1)),
                    is_pumping=bool(random.getrandbits(1)),
                    is_heating=bool(random.getrandbits(1)),
                    is_dc_contactor_closed=bool(random.getrandbits(1)),
                    is_end_of_charge=bool(random.getrandbits(1)),
                    is_balancing=bool(random.getrandbits(1)),
                    is_alert=bool(random.getrandbits(1)),
                    is_warning=bool(random.getrandbits(1)),
                    is_failure=bool(random.getrandbits(1)),
                    soc=random.randint(0, 100),
                    mode=random.choice(
                        [
                            BmsVmuStatus.MODE_STANDBY,
                            BmsVmuStatus.MODE_CHARGE,
                            BmsVmuStatus.MODE_DRIVE,
                            BmsVmuStatus.MODE_ERROR,
                        ]
                    ),
                )
                rx_data = encode_bms_vmu_status(rx_obj)
                time.sleep(1)

            # Only interested in BMS_VMU_STATUS responses
            if rx_id == BmsVmuStatus.MESSAGE_ID:
                try:
                    decoded = decode_bms_vmu_status(rx_data)
                except Exception as e:
                    decoded = f"Decode error: {e}"
                rx_data_hex = rx_data.hex() if hasattr(rx_data, "hex") else str(rx_data)
                timestamp = time.time()
                csv_writer.writerow(
                    [timestamp, "RX", f"0x{rx_id:X}", rx_data_hex, str(decoded)]
                )
                log_file.flush()
                if isinstance(decoded, BmsVmuStatus):
                    panel = Panel(
                        format_bms_vmu_status(decoded),
                        title="[bold green]Received BMS_VMU_STATUS[/bold green]",
                        subtitle=f"[magenta]hex:[/magenta] {rx_data_hex}",
                        border_style="green",
                    )
                    console.print(panel)
                else:
                    console.print(
                        f"[bold red]Received BMS_VMU_STATUS decode error:[/bold red] {decoded} (hex: [magenta]{rx_data_hex}[/magenta])"
                    )
                break  # Only log the first response for each request

    console.print(
        f"[bold green]Test complete.[/bold green] Log written to [yellow]{log_filename}[/yellow]"
    )
    log_file.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="HIL test for VMU_BMS_STATUS/BMS_VMU_STATUS"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run in simulation/offline mode"
    )
    parser.add_argument(
        "--can-channel", type=str, default="can0", help="CAN channel (default: can0)"
    )
    parser.add_argument(
        "--bustype",
        type=str,
        default="socketcan",
        help="CAN bustype (default: socketcan)",
    )
    parser.add_argument(
        "--bitrate", type=int, default=500000, help="CAN bitrate (default: 500000)"
    )
    parser.add_argument(
        "--log-dir", type=str, default="./logs/hil_logs", help="Directory for log files"
    )
    args = parser.parse_args()

    test_vmu_bms_status_hil(
        test_mode=args.test,
        can_channel=args.can_channel,
        bustype=args.bustype,
        bitrate=args.bitrate,
        log_dir=args.log_dir,
    )
