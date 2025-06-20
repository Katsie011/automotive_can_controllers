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

        self.cyclic_message_functions: Dict[int, CYCLIC_MESSAGE_TYPE] = {
            65265: (self.timer_callback_65265, 100)
        }

        # old fashion calling convention for compatibility with Python2
        j1939.ControllerApplication.__init__(self, name, device_address_preferred)

    def start(self):
        """Starts the CA
        (OVERLOADED function)
        """
        # add our timer event
        if self._ecu is not None:
            self._ecu.add_timer(0.100, self.timer_callback_65265)
        # call the super class function
        return j1939.ControllerApplication.start(self)

    def stop(self):
        """Stops the CA
        (OVERLOADED function)
        """
        if self._ecu is not None:
            self._ecu.remove_timer(self.timer_callback_65265)

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

        self.send_message(6, self.PGN_TRANSMIT_VEHICLE_SPEED, self.vehicle_speed)

        # returning true keeps the timer event active
        return True

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

    # create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
    ecu = j1939.ElectronicControlUnit()

    # Connect to the CAN bus
    # and configure CAN interface with 500 kbps bitrate
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/stable/bus.html).
    ecu.connect(bustype="socketcan", channel="can0")

    # ecu.connect(bustype='kvaser', channel=0, bitrate=500000)
    # ecu.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    # ecu.connect(bustype='ixxat', channel=0, bitrate=500000)
    # ecu.connect(bustype='vector', app_name='CANalyzer', channel=0, bitrate=500000)
    # ecu.connect(bustype='nican', channel='CAN0', bitrate=500000)

    kubota = Kubota_D902k_CA("KubotaD902K")
    ecu.add_ca(controller_application=kubota)

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
