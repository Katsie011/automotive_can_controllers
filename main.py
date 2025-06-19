"""
This is just a simple main.py app that listens for messages on the CAN Bus.
If it recognises any message, it will decode the output and print the data for debugging.

The main point of this is to provide an example of usage and provide a quick listener tool
"""

import can
import j1939
import time
from controller_applications.bender_ISO175_j1939 import ISO175_CA
from controller_applications.ivt_can_controller import IVTSensor
from controller_applications.ca_kubota_engine import Kubota_D902k_CA

bus = can.interface.Bus(channel="can0", bustype="socketcan")
# create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
# ecu = j1939.ElectronicControlUnit()
# Connect to the CAN bus
# and configure CAN interface with 500 kbps bitrate
# Arguments are passed to python-can's can.interface.Bus() constructor
# (see https://python-can.readthedocs.io/en/stable/bus.html).
# ecu.connect(bustype="socketcan", channel="can0")
# ecu.connect(bustype='kvaser', channel=0, bitrate=500000)
# ecu.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
# ecu.connect(bustype='ixxat', channel=0, bitrate=500000)
# ecu.connect(bustype='vector', app_name='CANalyzer', channel=0, bitrate=500000)
# ecu.connect(bustype='nican', channel='CAN0', bitrate=500000)

kubota = Kubota_D902k_CA("KubotaD902K")
iso_175 = ISO175_CA("ISO175")
ivt_sensor = IVTSensor("IVT", bus=bus)

# TODO: Setup a status spinner
# TODO: Setup a log file for the current experiment

decoded_msg = {"waiting": "No messages received yet"}

try:
    print("Listening for CAN messages. Press Ctrl+C to exit.")
    while True:
        msg = bus.recv(timeout=1.0)  # Wait for a CAN message (timeout in seconds)
        if msg is None:
            # No message received in this interval
            continue

        # Try to extract PGN (Parameter Group Number) from the CAN message
        # For J1939, PGN is typically bits 8-24 of the 29-bit arbitration_id
        # PGN = (arbitration_id >> 8) & 0xFFFF
        arbitration_id = msg.arbitration_id
        pgn = (arbitration_id >> 8) & 0xFFFF
        data = msg.data

        # Try to decode with each controller application
        if hasattr(ivt_sensor, "MESSAGE_IDS") and pgn in ivt_sensor.MESSAGE_IDS.keys():
            decoded_msg = ivt_sensor.decode(pgn=pgn, data=data)
        elif hasattr(kubota, "decoders") and pgn in kubota.decoders.keys():
            decoded_msg = kubota.decode(pgn=pgn, data=data)
        elif hasattr(iso_175, "decoders") and pgn in iso_175.decoders.keys():
            decoded_msg = iso_175.decode(pgn=pgn, data=data)
        else:
            print(f"Do not have any CAs that can decode message with PGN: {pgn}")
            decoded_msg = {"unknown_pgn": pgn, "raw_data": data.hex()}

        # Log and display the decoded message
        print(f"PGN: {pgn} | Decoded: {decoded_msg}")

        # TODO: Update the status spinner or log file here if desired

        # Reset waiting message for next loop
        decoded_msg = {"waiting": "Waiting for new messages"}

except KeyboardInterrupt:
    print("\nStopped by user.")
