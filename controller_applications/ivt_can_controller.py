"""
Controller and interface to communicate with the "Isabellenhuette IVT-S HIGH PRECISION CURRENT MEASUREMENT" device.


"""

import can
import logging
import struct
import time

from enum import Enum


class Mode(Enum):
    RESET = 0
    START = 1
    STOP = 2
    ERROR = 3


class IVTSensor:
    """
    Controller-style class for the Isabellenhuette IVT-S-1K-U3-I-CAN2 sensor.
    Designed to emulate the structure of a J1939 ControllerApplication.
    """

    BASE_ID = 0x521  # Start of result messages (I, U1, U2, ...)

    RESULT_IDS = {
        0x00: ("current", "mA"),
        0x01: ("voltage_u1", "mV"),
        0x02: ("voltage_u2", "mV"),
        0x03: ("voltage_u3", "mV"),
        0x04: ("temperature", "0.1C"),
        0x05: ("power", "W"),
        0x06: ("coulomb_count", "As"),
        0x07: ("energy_count", "Wh"),
    }
    MAX_ID = max(RESULT_IDS.keys())

    CMD_ID = 0x411
    RESP_ID = 0x511

    def __init__(self, name="IVT", channel="can0", bitrate=500000, logger=None):
        self.name = name
        self.channel = channel
        self.bitrate = bitrate
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.running = False
        self.results = {}
        self.decoders = {mux_id: self._decode_mux for mux_id in self.RESULT_IDS}
        self.mode: Mode = Mode.RESET

    def start(self):
        self.bus = can.interface.Bus(
            channel=self.channel, bustype="socketcan", bitrate=self.bitrate
        )
        self.running = True
        # TODO: Check if this works:
        self.notifier = can.Notifier(self.bus, [self._on_can_message])
        self._start_sensor()
        self.mode = Mode.START
        self.logger.info("IVTSensor started and listening on bus.")

    def stop(self):
        self.running = False
        if hasattr(self, "notifier"):
            self.notifier.stop()
        self.logger.info("IVTSensor stopped.")
        self.mode = Mode.STOP
        self._stop_sensor()

    def _on_can_message(self, msg):
        if msg.arbitration_id >= self.BASE_ID and msg.arbitration_id <= self.MAX_ID:
            mux_id = msg.data[0]
            self.on_message(mux_id, msg.data)
        elif msg.arbitration_id == self.RESP_ID:
            self.logger.debug(f"Received response: {msg}")

    def on_message(self, pgn, data):
        if pgn in self.decoders:
            result = self.decode(pgn, data)
            if isinstance(result, dict):
                self.logger.debug(f"Decoded result from PGN {pgn}: {result}")

    def decode(self, pgn: int, data: bytes):
        decoder = self.decoders.get(pgn)
        return decoder(data) if decoder else {"error": f"No decoder for PGN/Mux {pgn}"}

    def _decode_mux(self, data: bytes):
        if len(data) != 6:
            self.logger.warning("Unexpected data length")
            return {}

        mux_id = data[0]
        msg_count = data[1] & 0x0F
        state_bits = (data[1] >> 4) & 0x0F
        raw_val = int.from_bytes(data[2:6], byteorder="big", signed=True)

        label, unit = self.RESULT_IDS[mux_id]
        value = raw_val / 10.0 if unit == "0.1C" else raw_val
        self.results[label] = value

        return {
            "label": label,
            "value": value,
            "unit": unit,
            "state_bits": state_bits,
            "msg_count": msg_count,
        }

    def send_command(self, data: bytes):
        msg = can.Message(
            arbitration_id=self.CMD_ID,
            data=data.ljust(8, b"\x00"),
            is_extended_id=False,
        )
        self.logger.debug(f"Sending command: {msg}")
        self.bus.send(msg)

    def read_response(self, timeout=1.0):
        start = time.time()
        while time.time() - start < timeout:
            msg = self.bus.recv(timeout)
            if msg and msg.arbitration_id == self.RESP_ID:
                self.logger.debug(f"Received response: {msg}")
                return msg
        self.logger.warning("No response received.")
        return None

    def _start_sensor(self):
        data = struct.pack(">BBBBH", 0x34, 0x01, 0x01, 0x00, 0x0000)
        self.send_command(data)
        self.read_response()

    def _stop_sensor(self):
        data = struct.pack(">BBBBH", 0x34, 0x00, 0x00, 0x00, 0x0000)
        self.send_command(data)
        self.read_response()

    def reset_errors(self):
        data = struct.pack(">BBBBI", 0x30, 0x03, 0x00, 0x00, 0x00000000)
        self.send_command(data)
        self.read_response()

    def trigger_measurement(self, channels=0xFF):
        data = struct.pack(">BH", 0x31, channels)
        self.send_command(data)
        self.read_response()

    def get_latest_results(self):
        return self.results.copy()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sensor = IVTSensor()
    sensor.start()
    sensor._start_sensor()
    sensor.trigger_measurement()

    try:
        while True:
            time.sleep(1)
            results = sensor.get_latest_results()
            for k, v in results.items():
                print(f"{k}: {v}")
    except KeyboardInterrupt:
        sensor.stop()
