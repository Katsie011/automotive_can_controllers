from enum import Enum
import struct
from typing import Dict
import j1939

# import logging


# logging.getLogger("j1939").setLevel(logging.DEBUG)
# logging.getLogger("can").setLevel(logging.DEBUG)

# Type alias for cyclic message functions
# Each tuple contains (callback_function, interval_ms)
# Type for the cyclic messages returned by the class.
## For python 3.12:
type CYCLIC_MESSAGE_TYPE = tuple[function, int]


class Kubota_D902k_CA(j1939.ControllerApplication):
    """
    Controller Application for reading and writing to the Kubota D902k engine

    """

    # CONSTANTS
    BITS_PER_LITRE_FUEL = 0.05  # 0.05 L/h per bit
    BITS_PER_RPM_ENGINE_SPEED = 0.125  # 0.125 rpm/bit
    BITS_PER_PERCENT_THROTTLE = 0.4  # 0.4 %/bit
    BITS_PER_VOLT_BATTERY_POTENTIAL = 0.05  #  0.05V/bit
    BITS_PER_KPA_BAROMETRIC_PRESSURE = 0.5  # 0.5 kPa/bit
    BITS_PER_LITRE_TOTAL_FUEL_USED = 0.5  # 0.5 L/bit
    PGN_TRANSMIT_VEHICLE_SPEED = 65265  # pgn  for the vehicle speed.
    PGN_TRANSMIT_ENGINE_CONTROL = 65363  # PGN for the engine control

    """0000: start not requested
    0010: starter active (gear engaged)
    0100: starter inhibited due to engine already running
    1100: starter inhibited
    Other status are not supported
    """
    ENGINE_STARTER_MODE = {
        0b0000: "START_NOT_REQUESTED",
        0b0010: "STARTER ACTIVE",
        0b0100: "START INHIBITED - ENGINE ALREADY RUNNING",
        0b1100: "START INHIBITED ",
    }

    def __init__(self, name, device_address_preferred=None) -> None:
        self.decoders = {
            61444: self.decode_61444,
            61443: self.decode_61443,
            65247: self.decode_65247,
            65262: self.decode_65262,
            65266: self.decode_65266,
            65271: self.decode_65271,
            65269: self.decode_65269,
            65257: self.decode_65257,
            65252: self.decode_65252,
        }
        self.vehicle_speed = j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8
        self.throttle_pos = j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8
        self.park_brake = j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8
        self.control_mode = j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8

        self.neutral_switch: int = 0  # 0 or 1
        self.accelerator_pedal_error_info: int = 0  # 0 or 1
        self.icr_integration_paragraph_stop: int = 0  # 0 or 1
        self.icr_proportion_paragraph_stop: int = 0  # 0 or 1
        self.icr_target_engine_speed: int = 0  # 0-64255, rpm
        self.governor_characteristic_info: int = 0  # 0 or 1
        self.droop_map_select_info: int = 0  # 0-2
        self.engine_stop_info: int = 0  # 0 or 1
        self.accelerator_pedal_position: float = 0.0  # 0-100, percent
        self.vehicle_speed: float = 0.0  # 0-642.55, km/h
        self.cyclic_message_functions: Dict[int, CYCLIC_MESSAGE_TYPE] = {
            65265: (self.timer_callback_65265, 100),
            6563: (self.timer_callback_6563, 10),
        }

        # old fashion calling convention for compatibility with Python2
        j1939.ControllerApplication.__init__(self, name, device_address_preferred)

    def start(self):
        """Starts the CA
        (OVERLOADED function)
        """
        # add our timer event
        if self._ecu is not None:
            for callback, period in self.cyclic_message_functions.items():
                self._ecu.add_timer(period, callback)

        # call the super class function
        return j1939.ControllerApplication.start(self)

    def stop(self):
        """Stops the CA
        (OVERLOADED function)
        """
        if self._ecu is not None:
            for callback, period in self.cyclic_message_functions.items():
                self._ecu.remove_timer(period, callback)

    def on_message(self, pgn, data):
        """Feed incoming message to this CA.
        (OVERLOADED function)
        :param int pgn:
            Parameter Group Number of the message
        :param bytearray data:
            Data of the PDU
        """
        print("PGN {} length {}".format(pgn, len(data)))

        # Try to decode the message
        if pgn in self.decoders.keys():
            result = self.decode(pgn, data)
            # Print the decoded information if successful
            if type(result) == dict:
                if "error" not in result:
                    print(f"\nDecoded PGN {pgn}:")
                else:
                    print("Could not decode the message!")
                for key, value in result.items():
                    print(f"  {key}: {value}")

    def decode(self, pgn, data):
        """Dispatch decoder based on PGN."""
        decoder = self.decoders.get(pgn)
        return decoder(data) if decoder else {"error": f"No decoder for PGN {pgn}"}

    def decode_61444(self, data):
        """EEC1 - Engine Speed, Torque, Starter Mode, etc."""
        demand_torque = data[1] - 125
        actual_torque = data[2] - 125
        engine_speed = self._engine_speed_bits_to_rpm(
            struct.unpack_from("<H", data, 3)[0]
        )
        tsc1_src_address = data[5]
        # starter_mode = (
        #     data[6] & 0xF0
        # ) >> 4  # TODO: Not convinced this is right. Needs to be checked
        starter_mode = data[6]
        return {
            "PGN": 61444,
            "Engine Speed (RPM)": engine_speed,
            "Driver's Demand Torque (%)": demand_torque,
            "Actual Engine Torque (%)": actual_torque,
            "Starter Mode": starter_mode,
            "Starter Message": self.ENGINE_STARTER_MODE.get(
                starter_mode, "STATUS UNKNOWN"
            ),
            "TSC1 Source Address": tsc1_src_address,
        }

    def decode_61443(self, data):
        """EEC2 - Pedal Position, Engine Load"""
        engine_load = data[2] * 1.0
        accel_pos = data[1] * 0.4
        return {
            "PGN": 61443,
            "Engine Load (%)": engine_load,
            "Accelerator Pedal Position (%)": accel_pos,
        }

    def decode_65247(self, data):
        """EEC3 - Desired Engine Speed"""
        desired_speed = struct.unpack_from("<H", data, 1)[0] * 0.125
        return {
            "PGN": 65247,
            "Desired Engine Speed (RPM)": desired_speed,
        }

    def decode_65262(self, data):
        """ET1 - Engine Coolant Temperature"""
        temp_c = data[0] - 40
        return {
            "PGN": 65262,
            "Engine Coolant Temp (°C)": temp_c,
        }

    def set_vehicle_speed_65265(self, km_hr: float):
        """Transmit vehicle speed"""
        self.vehicle_speed = int(km_hr / 250.996)
        # CCVS	18FEF1VA*	65265	2-3	2 bytes	84	Vehicle Speed		X	6	100	0 to 250.996 km/h, 1/256 km/h per bit, 0 offset

    def timer_callback_65265(self, cookie):
        """Callback for sending the vehicle speed message for the kubota to read

        This callback is registered at the ECU timer event mechanism to be
        executed every 100ms.

        :param cookie:
            A cookie registered at 'add_timer'. May be None.
        """
        # wait until we have our device_address
        if self.state != j1939.ControllerApplication.State.NORMAL:
            # returning true keeps the timer event active
            return True

        # Alternatively, this works:
        # pgn = j1939.ParameterGroupNumber(
        #     0, # data_page
        #  0xFE, # pdu_format
        # 65265, # pdu_specific
        # )

        self.send_message(
            priority=6,
            parameter_group_number=self.PGN_TRANSMIT_VEHICLE_SPEED,
            # data=self.vehicle_speed,
            # TODO THIS IS WRONG! WHERE IS THE REST OF THE DATA BYTES ARRAY
        )

        # returning true keeps the timer event active
        return True

    def set_throttle_percent(self, throttle_percent: int):
        self.throttle_pos = throttle_percent

    def decode_65266(self, data):
        """LFE - Fuel Rate, Throttle Position"""

        # 2 bytes, position 1-2,  0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset
        fuel_rate = self._fuel_rate_bits_to_litres(struct.unpack_from("<H", data, 0)[0])

        throttle = self._throttle_bits_to_percent(data[6])
        return {
            "PGN": 65266,
            "Fuel Rate (L/h)": fuel_rate,
            "Throttle Position (%)": throttle,
        }

    def decode_65271(self, data):
        """VEP1 - Battery Potential"""
        # position 5-6, 2 bytes,  0 to 3212.75 V, 0.05 V/bit, 0 offset, rate 1000ms
        voltage = (
            struct.unpack_from("<H", data, 4)[0] * self.BITS_PER_VOLT_BATTERY_POTENTIAL
        )
        return {
            "PGN": 65271,
            "Battery Voltage (V)": voltage,
        }

    def decode_65269(self, data):
        """AMB - Barometric Pressure"""
        #  0 to 125 kPa, 0.5 kPa/bit, 0 offset
        pressure = data[0] * self.BITS_PER_KPA_BAROMETRIC_PRESSURE
        return {
            "PGN": 65269,
            "Barometric Pressure (kPa)": pressure,
        }

    def decode_65257(self, data):
        """LFC - Total Fuel Used"""
        #  0 to 2105540607.5 L, 0.5 L/bit, 0 offset

        fuel_total = (
            struct.unpack_from("<I", data, 4)[0] * self.BITS_PER_LITRE_TOTAL_FUEL_USED
        )
        return {
            "PGN": 65257,
            "Total Fuel Used (L)": fuel_total,
        }

    def decode_65252(self, data):
        """SHUTDN - Wait to Start Lamp, Shutdown Status"""
        wait_to_start = data[3] & 0x03
        shutdown = data[4] & 0x03
        return {
            "PGN": 65252,
            "Wait to Start Lamp": wait_to_start,
            "Shutdown Active": shutdown,
        }

    def encode_65363(self) -> bytes:
        """
        Encodes PGN 65363 (Kubota Engine Control Command).
        Period:         10  ms
        Data Length:    8   bytes

        Signal Layout:
        ------------------------------------------------------------------------
        Byte(s)  | Bit(s) | Bit    | Signal Name                        | Unit   | Resolution | Offset | Min    | Max     | Notes
        Pos      | Pos    | Length |                                    |        |            |        |        |         |
        ------------------------------------------------------------------------
        DT1      | 1-2    | 2      | Neutral Switch                     |        | 1          | 0      | 0      | 1       | 00: Neutral Off, 01: Neutral On
                 | 3-4    | 2      | Accelerator Pedal Error Info       |        | 1          | 0      | 0      | 1       | 00: Normal, 01: Abnormal
                 | 5-6    | 2      | ICR Integration Paragraph Stop     |        | 1          | 0      | 0      | 1       | 00: Execution, 01: Stop
                 | 7-8    | 2      | ICR Proportion Paragraph Stop      |        | 1          | 0      | 0      | 1       | 00: Execution, 01: Stop
        DT2-3    | 1-16   | 16     | ICR Target Engine Speed            | rpm    | 1          | 0      | 0      | 64255   | Byte 2: LSB, Byte 3: MSB
        DT4      | 1-2    | 2      | Governor Characteristic Info       |        | 1          | 0      | 0      | 1       | 00: Droop, 01: Isochronous
                 | 3-6    | 4      | Droop Map Select Info              |        | 1          | 0      | 0      | 2       | 0000: Map 1, 0001: Map 2, 0010: Map 3
                 | 7-8    | 2      | Engine Stop Info                   |        | 1          | 0      | 0      | 1       | 00: Not Stop, 01: Stop
        DT5-6    | 1-16   | 16     | Accelerator Pedal Position         | %      | 0.1        | 0      | 0      | 100     | Byte 5: LSB, Byte 6: MSB
        DT7-8    | 1-16   | 16     | Vehicle Speed                      | km/h   | 0.01       | 0      | 0      | 642.55  | Byte 7: LSB, Byte 8: MSB

        Notes:
        - All bit positions are within their respective bytes unless otherwise noted.
        - Multi-byte fields are little-endian (LSB first).
        """
        # TODO rework this code
        # Collect all required state variables
        neutral_switch = getattr(self, "neutral_switch", 0)  # 0 or 1
        accelerator_pedal_error_info = getattr(
            self, "accelerator_pedal_error_info", 0
        )  # 0 or 1
        icr_integration_paragraph_stop = getattr(
            self, "icr_integration_paragraph_stop", 0
        )  # 0 or 1
        icr_proportion_paragraph_stop = getattr(
            self, "icr_proportion_paragraph_stop", 0
        )  # 0 or 1
        icr_target_engine_speed = getattr(
            self, "icr_target_engine_speed", 0
        )  # 0-64255, rpm
        governor_characteristic_info = getattr(
            self, "governor_characteristic_info", 0
        )  # 0 or 1
        droop_map_select_info = getattr(self, "droop_map_select_info", 0)  # 0-2
        engine_stop_info = getattr(self, "engine_stop_info", 0)  # 0 or 1
        accelerator_pedal_position = getattr(
            self, "accelerator_pedal_position", 0.0
        )  # 0-100, percent
        vehicle_speed = getattr(self, "vehicle_speed", 0.0)  # 0-642.55, km/h

        # Clamp and convert values to valid ranges
        neutral_switch = int(bool(neutral_switch)) & 0x01
        accelerator_pedal_error_info = int(bool(accelerator_pedal_error_info)) & 0x01
        icr_integration_paragraph_stop = (
            int(bool(icr_integration_paragraph_stop)) & 0x01
        )
        icr_proportion_paragraph_stop = int(bool(icr_proportion_paragraph_stop)) & 0x01
        icr_target_engine_speed = int(icr_target_engine_speed) & 0xFFFF
        governor_characteristic_info = int(governor_characteristic_info) & 0x01
        droop_map_select_info = int(droop_map_select_info) & 0x0F
        engine_stop_info = int(bool(engine_stop_info)) & 0x01
        accelerator_pedal_position = max(
            0, min(1000, int(round(accelerator_pedal_position * 10)))
        )  # 0.1%/bit
        vehicle_speed = max(
            0, min(64255, int(round(vehicle_speed * 100)))
        )  # 0.01 km/h/bit

        data = bytearray(8)

        # Byte 0 (DT1)
        # bits 0-1: Neutral Switch
        # bits 2-3: Accelerator Pedal Error Info
        # bits 4-5: ICR Integration Paragraph Stop
        # bits 6-7: ICR Proportion Paragraph Stop
        data[0] = (
            ((neutral_switch & 0x03) << 0)
            | ((accelerator_pedal_error_info & 0x03) << 2)
            | ((icr_integration_paragraph_stop & 0x03) << 4)
            | ((icr_proportion_paragraph_stop & 0x03) << 6)
        )

        # Byte 1-2 (DT2-3): ICR Target Engine Speed, little-endian
        data[1] = icr_target_engine_speed & 0xFF
        data[2] = (icr_target_engine_speed >> 8) & 0xFF

        # Byte 3 (DT4)
        # bits 0-1: Governor Characteristic Info
        # bits 2-5: Droop Map Select Info
        # bits 6-7: Engine Stop Info
        data[3] = (
            ((governor_characteristic_info & 0x03) << 0)
            | ((droop_map_select_info & 0x0F) << 2)
            | ((engine_stop_info & 0x03) << 6)
        )

        # Byte 4-5 (DT5-6): Accelerator Pedal Position, little-endian, 0.1%/bit
        data[4] = accelerator_pedal_position & 0xFF
        data[5] = (accelerator_pedal_position >> 8) & 0xFF

        # Byte 6-7 (DT7-8): Vehicle Speed, little-endian, 0.01 km/h/bit
        data[6] = vehicle_speed & 0xFF
        data[7] = (vehicle_speed >> 8) & 0xFF

        return data

    def timer_callback_6563(self, cookie):
        """
        Timer callback for PGN 65363 (Kubota Engine Control Command).
        This callback is registered at the ECU timer event mechanism,
        Period:         10  ms
        Data Length:    8   bytes

        :param cookie:
            A cookie registered at 'add_timer'. May be None.
        """
        # wait until we have our device_address
        if self.state != j1939.ControllerApplication.State.NORMAL:
            # returning true keeps the timer event active
            return True

        # Alternatively, this works:
        # pgn = j1939.ParameterGroupNumber(
        #     0, # data_page
        #  0xFE, # pdu_format
        # 65265, # pdu_specific
        # )
        # TODO Assert that the PGN is correct

        data = self.encode_65363()

        self.send_message(
            priority=6,
            parameter_group_number=self.PGN_TRANSMIT_ENGINE_CONTROL,
            data=data,
        )

        # returning true keeps the timer event active
        return True

    def decode_65360(self, data):
        """
        Decodes PGN 65360 (Kubota Engine Status 1).

        Signal Layout:
        ------------------------------------------------------------------------
        Byte(s)  | Bit(s) | Bit    | Signal Name                    | Unit   | Resolution | Offset | Min    | Max     | Notes
        Pos      | Pos    | Length |                                |        |            |        |        |         |
        ------------------------------------------------------------------------
        DT1-2    | 1-16   | 16     | Accelerator Pedal Position     | %      | 0.1        | 0      | 0      | 100     | Byte 1: LSB, Byte 2: MSB
        DT3-4    | 1-16   | 16     | Engine Speed                   | rpm    | 1          | 0      | 0      | 64255   | Byte 3: LSB, Byte 4: MSB
        DT5      | 1-8    | 8      | Engine Load Rate               | %      | 1          | 0      | 0      | 100
        DT6-7    | 1-16   | 16     | Fuel Injection Quantity        | mm3/st | 0.01       | 0      | 0      | 500     | Byte 6: LSB, Byte 7: MSB
        DT8      | 1-5    | 5      | Not used (All bits = 1)
                 | 6-7    | 2      | Utility Unit Error Information |        | 1          | 0      | 0      | 3
                 | 8      | 1      | Diagnosis Lamp On/Off          |        | 1          | 0      | 0      | 1
        ------------------------------------------------------------------------

        Notes:
        - All bit positions are within their respective bytes unless otherwise noted.
        - Multi-byte fields are little-endian (LSB first).
        - Message ID: 0x18FF5000
        - Period: 10 ms
        - Data length: 8 bytes
        """

        # TODO complete the decoder

        raise NotImplementedError

    def decode_65361(self, data):
        """
        Decodes PGN 65361 (Kubota Engine Status 2).

        Signal Layout:
        ------------------------------------------------------------------------
        Byte(s)  | Bit(s) | Bit    | Signal Name              | Unit   | Resolution | Offset | Min    | Max     | Notes
        Pos      | Pos    | Length |                         |        |            |        |        |         |
        ------------------------------------------------------------------------
        DT2      | 1-8    | 8      | Engine Coolant Temp      | deg.C  | 1          | -40    | -40    | 210     |
        DT3      | 1-2    | 2      | Not used (All bits = 1)  |        |            |        |        |         |
                 | 3-4    | 2      | Water In Fuel Indicator  |        | 1          | 0      | 0      | 3       | 00: Off, 01: On (Option)
                 | 5-6    | 2      | Glow Relay Flag          |        | 1          | 0      | 0      | 3       | 00: Off, 01: On, 10: Error, 11: Not available
                 | 7-8    | 2      | Glow Lamp Flag           |        | 1          | 0      | 0      | 3       | 00: Off, 01: On, 10: Error, 11: Not available
        DT4      | 1-8    | 8      | Not used (All bits = 1)  |        |            |        |        |         |
        DT5      | 1-8    | 8      | Not used (All bits = 1)  |        |            |        |        |         |
        DT7      | 1-4    | 4      | Reserved (All bits = 0)  |        |            |        |        |         |
                 | 5-6    | 2      | Over Heat Lamp           |        | 1          | 0      | 0      | 1       | 00: Off, 01: On
                 | 7-8    | 2      | Not used (All bits = 1)  |        |            |        |        |         |
        ------------------------------------------------------------------------

        Notes:
        - All bit positions are within their respective bytes unless otherwise noted.
        - Multi-bit fields are little-endian (LSB first).
        - Message ID: 0x18FF5100
        - Period: 1000 ms
        - Data length: 8 bytes
        """

        # TODO complete the decoder
        raise NotImplementedError

    def _engine_speed_rpm_to_bits(self, rpm: float) -> int:
        """0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset"""
        if rpm < 0 or rpm > 8031.875:
            raise ValueError(
                f"Engine speed must be between 0 and 8031.875 RPM, got {rpm}"
            )
        return int(rpm / self.BITS_PER_RPM_ENGINE_SPEED)

    def _engine_speed_bits_to_rpm(self, bits: int) -> float:
        """0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset"""
        rpm = bits * self.BITS_PER_RPM_ENGINE_SPEED
        if rpm < 0 or rpm > 8031.875:
            raise ValueError(
                f"Engine speed must be between 0 and 8031.875 RPM, got the equivalent of {rpm}"
            )
        return rpm

    def _fuel_rate_litres_to_bits(self, litres: float) -> int:
        """0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset"""
        if litres < 0 or litres > 3212.75:
            raise ValueError(
                f"Fuel rate must be between 0 and 3212.75 L/h, got {litres}"
            )
        return int(litres / self.BITS_PER_LITRE_FUEL)

    def _fuel_rate_bits_to_litres(self, bits: int) -> float:
        """0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset"""
        litres = bits * self.BITS_PER_LITRE_FUEL
        if litres < 0 or litres > 3212.75:
            raise ValueError(
                f"Fuel rate must be between 0 and 3212.75 L/h, got the equivalent of {litres}"
            )
        return litres

    def _throttle_bits_to_percent(self, bits: int) -> float:
        """Starts position 7, 1 byte,  0 to 100%, 0.4 %/bit, 0 offset"""
        percent = bits * self.BITS_PER_PERCENT_THROTTLE
        if percent < 0 or percent > 100:
            raise ValueError(
                f"Throttle position must be between 0 and 100%, got the equivalent of {percent}%"
            )
        return percent

    def _throttle_percent_to_bits(self, percent: float) -> int:
        """Starts position 7, 1 byte,  0 to 100%, 0.4 %/bit, 0 offset"""
        if percent < 0 or percent > 100:
            raise ValueError(
                f"Throttle position must be between 0 and 100%, got the equivalent of {percent}%"
            )
        bits = int(percent / self.BITS_PER_PERCENT_THROTTLE)
        return bits


# struct.unpack assumes little endian and uses <H for unsigned short, <I for unsigned int


if __name__ == "__main__":
    import time

    TESTING = True
    # MODE = "LISTEN"
    MODE = "TUI"
    # create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
    ecu = j1939.ElectronicControlUnit()

    # Connect to the CAN bus
    # and configure CAN interface with 500 kbps bitrate
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/stable/bus.html).
    if not TESTING:
        ecu.connect(bustype="socketcan", channel="can0")

    # ecu.connect(bustype='kvaser', channel=0, bitrate=500000)
    # ecu.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    # ecu.connect(bustype='ixxat', channel=0, bitrate=500000)
    # ecu.connect(bustype='vector', app_name='CANalyzer', channel=0, bitrate=500000)
    # ecu.connect(bustype='nican', channel='CAN0', bitrate=500000)

    kubota = Kubota_D902k_CA("KubotaD902K")
    if not TESTING:
        ecu.add_ca(controller_application=kubota)

    if MODE == "LISTEN":
        try:
            kubota.start()
            print("Listening to CAN bus... Press Ctrl+C to stop.\n")
            time.sleep(120)
        except KeyboardInterrupt:
            print("\nUser Stopped.")
        finally:
            print("Deinitializing")
            kubota.stop()
            ecu.disconnect()
    elif MODE == "TUI":
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.live import Live
        from rich.spinner import Spinner

        import threading
        import sys
        import termios
        import tty

        console = Console()
        status_lock = threading.Lock()

        # Engine control state
        throttle_percent = 0
        vehicle_speed_kph = 0.0
        park_brake = False
        neutral_switch = False
        running = True

        # For status display
        engine_status = {
            "Engine Speed (RPM)": 0,
            "Engine Load (%)": 0,
            "Coolant Temp (°C)": 0,
            "Fuel Rate (L/h)": 0,
            "Throttle Position (%)": 0,
            "Vehicle Speed (km/h)": 0.0,
            "Park Brake": "OFF",
            "Neutral Switch": "OFF",
            "Wait To Start": False,
        }

        # TODO: Add wait to start lamp to dashboard.

        def getch():
            """Read a single character from stdin (non-blocking, no echo)."""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        def key_listener():
            global throttle_percent, vehicle_speed_kph, park_brake, neutral_switch, running
            while running:
                ch = getch()
                with status_lock:
                    if ch == "\x1b":  # Arrow keys start with ESC
                        next1 = getch()
                        if next1 == "[":
                            arrow = getch()
                            if arrow == "A":  # Up
                                throttle_percent = min(100, throttle_percent + 2)
                                kubota.set_throttle_percent(throttle_percent)
                            elif arrow == "B":  # Down
                                throttle_percent = max(0, throttle_percent - 2)
                                kubota.set_throttle_percent(throttle_percent)
                    elif ch.lower() == "k":
                        vehicle_speed_kph = min(100, vehicle_speed_kph + 1)
                        kubota.set_vehicle_speed_65265(vehicle_speed_kph)
                    elif ch.lower() == "j":
                        vehicle_speed_kph = max(0, vehicle_speed_kph - 1)
                        kubota.set_vehicle_speed_65265(vehicle_speed_kph)
                    elif ch.lower() == "p":
                        park_brake = not park_brake
                        # Simulate park brake toggle (implement actual CAN message if needed)
                        engine_status["Park Brake"] = "ON" if park_brake else "OFF"
                    elif ch.lower() == "n":
                        neutral_switch = not neutral_switch
                        # Simulate neutral switch toggle (implement actual CAN message if needed)
                        engine_status["Neutral Switch"] = (
                            "ON" if neutral_switch else "OFF"
                        )
                    elif ch.lower() == "q":
                        running = False
                        break

        def update_status():
            """Poll engine status from Kubota CA and update engine_status dict."""
            # This is a placeholder. In a real implementation, you would subscribe to CAN messages
            # and update the status variables accordingly.
            # Here, we simulate by calling decode methods with dummy data.
            while running:
                with status_lock:
                    # Simulate reading engine speed, load, etc.
                    # In real code, replace with actual CAN message polling/decoding
                    # For demo, just increment engine speed if throttle > 0
                    engine_status["Engine Speed (RPM)"] = int(
                        800 + 12 * throttle_percent
                    )
                    engine_status["Engine Load (%)"] = throttle_percent
                    engine_status["Coolant Temp (°C)"] = 70 + int(throttle_percent / 10)
                    engine_status["Fuel Rate (L/h)"] = round(
                        0.5 + 0.05 * throttle_percent, 2
                    )
                    engine_status["Throttle Position (%)"] = throttle_percent
                    engine_status["Vehicle Speed (km/h)"] = round(vehicle_speed_kph, 2)
                    engine_status["Park Brake"] = "ON" if park_brake else "OFF"
                    engine_status["Neutral Switch"] = "ON" if neutral_switch else "OFF"
                time.sleep(0.2)

        def render_status_table():
            table = Table(title="Kubota Engine Status", show_lines=True, expand=True)
            table.add_column("Parameter", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            with status_lock:
                for key, value in engine_status.items():
                    table.add_row(key, str(value))
            return table

        def tui_main():
            global running
            console.print(
                Panel.fit(
                    "[bold green]Kubota Engine Control TUI[/bold green]\n"
                    "Use [yellow]Up/Down Arrows[/yellow] to change throttle\n"
                    "[yellow]k/j[/yellow] to increase/decrease vehicle speed\n"
                    "[yellow]p[/yellow] to toggle park brake, [yellow]n[/yellow] to toggle neutral\n"
                    "[yellow]q[/yellow] to quit.",
                    title="Kubota Engine",
                    border_style="green",
                )
            )
            spinner = Spinner("dots", text="Engine running...")
            # Start background threads
            # t_key = threading.Thread(target=key_listener, daemon=True)
            t_status = threading.Thread(target=update_status, daemon=True)
            # t_key.start()
            t_status.start()
            with Live(
                render_status_table(), refresh_per_second=5, console=console
            ) as live:
                while running:
                    live.update(render_status_table())
                    key_listener()
                    time.sleep(0.2)
            console.print(
                "\n[bold yellow]Exiting Kubota Engine Control. Goodbye![/bold yellow]"
            )

        tui_main()
