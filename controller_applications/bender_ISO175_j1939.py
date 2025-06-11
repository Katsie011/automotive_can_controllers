from typing import Dict
import can
import struct
import j1939

type CYCLIC_MESSAGE_TYPE = tuple[function, int]


class ISO175_CA(j1939.ControllerApplication):
    """Decoder class for ISO175 device messages following J1939 protocol.

    📊 J1939 Signal Table - iso175 Insulation Monitoring Device

    | **PGN** | **CAN ID (SrcAddr=244)** | **Name**                   | **Byte(s)** | **Signal**                                 | **Unit / Description**                |
    | ------- | ------------------------ | -------------------------- | ----------- | ------------------------------------------ | ------------------------------------- |
    | 65281   | `0x18FF01F4`             | PGN_Info_General           | 0-1         | `R_iso_corrected` (neg. tolerance shifted) | kΩ (0-35000); 65535 = SNV             |
    |         |                          |                            | 2           | `R_iso_status`                             | 0xFC-0xFE = startup state; 0xFF = SNV |
    |         |                          |                            | 3           | `Isolation Measurement Counter`            | Incremented per new reading           |
    |         |                          |                            | 4           | `Status: Warnings and Alarms`              | Bit field - see below                 |
    |         |                          |                            | 5           | `Status: Device Activity`                  | 0 = Init, 1 = Normal, 2 = Self-test   |
    | 65282   | `0x18FF02F4`             | PGN_Info_IsolationDetail   | 0-1         | `R_iso_neg`                                | kΩ (0-50000)                          |
    |         |                          |                            | 2-3         | `R_iso_pos`                                | kΩ (0-50000)                          |
    |         |                          |                            | 4-5         | `R_iso_original`                           | kΩ (0-50000)                          |
    |         |                          |                            | 6           | `Isolation Measurement Counter`            | Same as above                         |
    |         |                          |                            | 7           | `Isolation Quality`                        | % (0-100), 255 = SNV                  |
    | 65283   | `0x18FF03F4`             | PGN_Info_Voltage           | 0-1         | `HV System Voltage`                        | V = value × 0.05                      |
    |         |                          |                            | 2-3         | `HV_neg to Earth`                          | V = (value - 32128) × 0.05            |
    |         |                          |                            | 4-5         | `HV_pos to Earth`                          | V = (value - 32128) × 0.05            |
    |         |                          |                            | 6           | `Voltage Measurement Counter`              | -                                     |
    | 65284   | `0x18FF04F4`             | PGN_Info_IT-System         | 0-1         | `Capacity Measured Value`                  | μF = value × 0.1                      |
    |         |                          |                            | 2           | `Capacity Measurement Counter`             | -                                     |
    |         |                          |                            | 3-4         | `Unbalance Measured Value`                 | % (0-100), 255 = SNV                  |
    |         |                          |                            | 5           | `Unbalance Measurement Counter`            | -                                     |
    |         |                          |                            | 6-7         | `Voltage Frequency`                        | Hz = value × 0.1                      |

    ⚠️ Bitfield: Status: Warnings and Alarms (Byte 4 of PGN 65281)

    Each bit represents a status flag:
    Bit	Meaning
    | **Bit** | **Meaning**                          |
    | ------- | ------------------------------------ |
    | 0       | Device error active                  |
    | 1       | HV_pos connection failure            |
    | 2       | HV_neg connection failure            |
    | 3       | Earth connection failure             |
    | 4       | Iso Alarm (value < error threshold)  |
    | 5       | Iso Warning (value < warning thresh) |
    | 6       | Iso Outdated (value too old)         |
    | 7       | Unbalance Alarm                      |
    | 8       | Undervoltage Alarm                   |
    | 9       | Unsafe to Start                      |
    | 10      | Earthlift open                       |

    (*Byte 4 is technically 8 bits, but the document implies an extended field; you may see an additional byte or alternate PGN to deliver bits 8-10.)

    🧩 Notes for Decoding

    All PGNs are 8 bytes long.
    Byte order is Intel (little-endian).
    Values like voltage and resistance may use offsets and scaling factors, such as:
    Voltage to earth uses offset 32128, scaled by 0.05.
    Capacity scaled by 0.1 µF.
    65535 (0xFFFF) or 255 (0xFF) generally means Signal Not Valid (SNV).

    """

    def __init__(self, name, device_address_preferred=None) -> None:
        # Initialize decoders dictionary
        self.decoders = {
            65281: self.decode_pgn_65281,
            65282: self.decode_pgn_65282,
            65283: self.decode_pgn_65283,
            65284: self.decode_pgn_65284,
        }
        # Source Address of iso175 device (per manual)
        # This is a fixed address for the Bender ISO175 device
        self.source_address = 0xF4

        # Initialize cyclic message functions dictionary
        self.cyclic_message_functions: Dict[int, CYCLIC_MESSAGE_TYPE] = {}

        # Initialize storage for decoded values
        self.general_info = {}
        self.isolation_detail = {}
        self.voltage_info = {}
        self.it_system_info = {}

        # Call parent class constructor
        j1939.ControllerApplication.__init__(self, name, device_address_preferred)

    def start(self):
        """Starts the Controller Application."""
        return j1939.ControllerApplication.start(self)

    def stop(self):
        """Stops the Controller Application."""
        return j1939.ControllerApplication.stop(self)

    def on_message(self, pgn, data):
        """Handle incoming messages.

        Args:
            pgn: Parameter Group Number of the message
            data: Data of the PDU
        """
        print(f"PGN {pgn} length {len(data)}")

        # Try to decode the message
        if pgn in self.decoders:
            result = self.decode(pgn, data)
            # Print the decoded information if successful
            if isinstance(result, dict):
                if "error" not in result:
                    print(f"\nDecoded PGN {pgn}:")
                else:
                    print("Could not decode the message!")
                for key, value in result.items():
                    print(f"  {key}: {value}")

    def decode(self, pgn: int, data: bytes):
        """Decode a message based on its PGN.

        Args:
            pgn: Parameter Group Number as string
            data: Raw message data

        Returns:
            bool: True if message was decoded successfully, False otherwise
        """
        decoder = self.decoders.get(pgn)
        return decoder(data) if decoder else {"error": f"No decoder for PGN {pgn}"}

    def decode_pgn_65281(self, data: bytes):
        """Decode PGN 65281 - General Info containing device status and measurements."""
        try:
            # Unpack 16-bit values using little-endian format (<H)
            r_iso_corr = struct.unpack_from("<H", data[:2])[
                0
            ]  # Corrected isolation resistance
            r_iso_status: int = data[2]  # Status byte for isolation measurement
            meas_count: int = data[3]  # Counter for measurements
            alarms: int = struct.unpack_from("<H", data[4:6])[
                0
            ]  # Bitfield containing alarm states
            device_state = data[6]  # Current state of the device

            r_iso_status_meaning = {
                0xFC: "estimated isolation value during startup",
                0xFD: "first measured isolation value during startup",
                0xFE: "isolation value in normal operation",
                0xFF: "SNV",
            }.get(r_iso_status, "unknown status")

            # Store decoded values as instance variables
            self.general_info = {
                "r_iso_corrected": r_iso_corr if r_iso_corr != 0xFFFF else "SNV",
                "r_iso_status": r_iso_status,
                "r_iso_status_meaning": r_iso_status_meaning,
                "measurement_counter": meas_count,
                "alarms": alarms,
                "device_state": device_state,
                "device_state_meaning": (
                    ["Init", "Normal", "SelfTest"][device_state]
                    if device_state < 3
                    else "Unknown"
                ),
            }
            return self.general_info
        except Exception as e:
            print(f"Error decoding PGN 65281: {e}")
            return False

    def decode_pgn_65282(self, data: bytes):
        """Decode PGN 65282 - Isolation Detail containing detailed isolation measurements."""
        try:
            # Extract isolation resistance values (in kΩ)
            r_kΩ_negative = struct.unpack_from("<H", data[:2])[0]
            r_kΩ_positive = struct.unpack_from("<H", data[2:4])[0]
            r_kΩ_original = struct.unpack_from("<H", data[4:6])[0]
            iso_measurement_count = data[6]
            iso_measurement_quality = data[7]

            # Store decoded values
            self.isolation_detail = {
                "isolation_negative": r_kΩ_negative,
                "isolation_positive": r_kΩ_positive,
                "isolation_original": r_kΩ_original,
                "measurement_count": iso_measurement_count,
                "measurement_quality": iso_measurement_quality,
            }
            return self.isolation_detail
        except Exception as e:
            print(f"Error decoding PGN 65282: {e}")
            return False

    def decode_pgn_65283(self, data: bytes):
        """Decode PGN 65283 - Voltage Info containing high voltage system measurements."""
        try:
            # Convert raw values to voltage (V)
            hv_sys = struct.unpack_from("<H", data, 0)[0] * 0.05
            hv_neg = (struct.unpack_from("<H", data, 2)[0] - 32128) * 0.05
            hv_pos = (struct.unpack_from("<H", data, 4)[0] - 32128) * 0.05

            # Store decoded values
            self.voltage_info = {
                "hv_system_voltage": hv_sys,
                "hv_negative_to_earth": hv_neg,
                "hv_positive_to_earth": hv_pos,
            }
            return self.voltage_info
        except Exception as e:
            print(f"Error decoding PGN 65283: {e}")
            return False

    def decode_pgn_65284(self, data: bytes):
        """Decode PGN 65284 - IT-System Info containing system capacitance measurements."""
        try:
            # Extract measurements
            capacity_measured = struct.unpack_from("<H", data[:2])[0]  # in μF
            if capacity_measured == 65535:
                capacity_measured = "SNV"

            capacity_measure_count = data[2]
            unbalance_measure_value = data[3]
            unbalance_measurement = data[4]
            voltage_frequency = struct.unpack_from("<H", data[5:7])[0]  # in Hz

            # Store decoded values
            self.it_system_info = {
                "capacity_measured": capacity_measured,
                "capacity_measure_count": capacity_measure_count,
                "unbalance_measure_value": unbalance_measure_value,
                "unbalance_measurement": unbalance_measurement,
                "voltage_frequency": voltage_frequency,
            }
            return self.it_system_info
        except Exception as e:
            print(f"Error decoding PGN 65284: {e}")
            return False


if __name__ == "__main__":
    import time

    # Create the ElectronicControlUnit
    ecu = j1939.ElectronicControlUnit()

    # Connect to the CAN bus
    ecu.connect(bustype="socketcan", channel="can0", bitrate=500000)

    # Create and add the ISO175 controller application
    iso175 = ISO175_CA("ISO175")
    ecu.add_ca(controller_application=iso175)

    try:
        iso175.start()
        print("Listening to CAN bus... Press Ctrl+C to stop.\n")
        time.sleep(120)  # Run for 2 minutes
    except KeyboardInterrupt:
        print("\nUser Stopped.")
    finally:
        iso175.stop()
        ecu.disconnect()

# 400 fte
# 250 engieers
# 2.5 years development timeline for prototype
