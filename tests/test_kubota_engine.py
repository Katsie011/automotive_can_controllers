import pytest
from unittest.mock import Mock, patch
import struct
import j1939
import sys
import os

# Append the root dir of the library suite... There has to be a better way to do this.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller_applications.ca_kubota_engine import Kubota_D902k_CA


@pytest.fixture
def kubota():
    """Fixture to create and configure Kubota_D902k_CA instance for testing."""
    with patch("j1939.ControllerApplication.__init__", return_value=None):
        kubota = Kubota_D902k_CA("Kubota_D902k_CA")
        kubota._ecu = Mock()
        # TODO check if this runs without the
        # iso175.state = j1939.ControllerApplication.State.NORMAL
        return kubota


def test_initialization(kubota):
    """Test proper initialization of the Kubota_D902k_CA class."""
    # assert kubota.source_address == 0xF4
    assert 61444 in kubota.decoders
    assert 61443 in kubota.decoders
    assert 65247 in kubota.decoders
    assert 65262 in kubota.decoders
    assert 65266 in kubota.decoders
    assert 65271 in kubota.decoders
    assert 65269 in kubota.decoders
    assert 65257 in kubota.decoders
    assert 65252 in kubota.decoders
    assert kubota.cyclic_message_functions == {
        65265: (kubota.timer_callback_65265, 100)
    }


def test__engine_speed_to_bits(kubota):
    """Test the engine speed to bits conversion."""
    engine_speed_rpm = 1000  # 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
    engine_speed_bits = int(engine_speed_rpm / 0.125)
    result = kubota._engine_speed_to_bits(engine_speed_rpm)
    assert result == engine_speed_bits


def test__bits_to_engine_speed(kubota):
    """Test the bits to engine speed conversion."""
    engine_speed_bits = 24000
    engine_speed_rpm = engine_speed_bits * 0.125
    result = kubota._bits_to_engine_speed(engine_speed_bits)
    assert result == engine_speed_rpm

def test__fuel_rate_litres_to_bits

def test_decode_61444_eec1(kubota):
    """Test decoding of PGN 61444 (EEC1)."""

    torque_offset = -125  # -125% to 125%, 1 %/bit, -125% offset
    demand_torque = 25  # %
    actual_torque = 15  # %
    engine_speed_rpm = 1000  # 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
    engine_speed_bits = kubota._engine_speed_to_bits(engine_speed_rpm)
    data = struct.pack(
        "<BBBHBBBB",
        0,  # padding
        demand_torque - torque_offset,  # demand torque (25%)
        actual_torque - torque_offset,  # actual torque (15%)
        engine_speed_bits,  # engine speed
        0x00,  # TSC1 source address
        0b0100,  # starter mode - inhibited engine running
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_61444(data)
    print("#" * 60)
    print("test_decode_61444_eec1 result:")
    print("#" * 60)
    print(result)
    print("#" * 60)
    assert result["PGN"] == 61444
    assert result["Engine Speed (RPM)"] == engine_speed_rpm
    assert result["Driver's Demand Torque (%)"] == 25
    assert result["Actual Engine Torque (%)"] == 15
    assert result["Starter Mode"] == 0b0100
    assert result["Starter Message"] == "START INHIBITED - ENGINE ALREADY RUNNING"
    assert result["TSC1 Source Address"] == 0x00


def test_decode_61443_eec2(kubota):
    """Test decoding of PGN 61443 (EEC2)."""
    acccel_pos = 20.0
    acccel_bits = int(20 / 0.4)  # 0 to 100%, 0.4 %/bit, 0 offset
    data = struct.pack(
        "<BBBBBBBB",
        0,  # padding
        acccel_bits,  # accel pos (20%)
        75,  # engine load (75%)
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_61443(data)
    assert result["PGN"] == 61443
    assert result["Engine Load (%)"] == 75.0
    assert result["Accelerator Pedal Position (%)"] == acccel_pos


def test_decode_65247_eec3(kubota):
    """Test decoding of PGN 65247 (EEC3)."""
    desired_engine_speed = 0  # 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
    bits_engine_speed = kubota._engine_speed_to_bits(desired_engine_speed)
    data = struct.pack(
        "<BBBBBBBB",
        0,  # padding
        bits_engine_speed,  # desired speed (0 RPM)
        # 0x00,  # desired speed
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_65247(data)
    assert result["PGN"] == 65247
    assert result["Desired Engine Speed (RPM)"] == 0


def test_decode_65262_et1(kubota):
    """Test decoding of PGN 65262 (ET1)."""
    data = struct.pack(
        "<BBBBBBBB",
        90,  # temp (50°C)
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_65262(data)
    assert result["PGN"] == 65262
    assert result["Engine Coolant Temp (°C)"] == 50


def test_set_vehicle_speed_65265(kubota):
    """Test setting vehicle speed."""
    kubota.set_vehicle_speed_65265(100.0)  # 100 km/h
    expected = int(100.0 / 250.996)
    assert kubota.vehicle_speed == expected


def test_timer_callback_65265(kubota):
    """Test timer callback for vehicle speed."""
    # Test when not in NORMAL state
    kubota.state = j1939.ControllerApplication.State.NONE
    assert kubota.timer_callback_65265(None) is True

    # Test when in NORMAL state
    kubota.state = j1939.ControllerApplication.State.NORMAL
    kubota.set_vehicle_speed_65265(100.0)
    with patch.object(kubota, "send_message") as mock_send:
        assert kubota.timer_callback_65265(None) is True
        mock_send.assert_called_once_with(6, 65265, kubota.vehicle_speed)


def test_decode_65266_lfe(kubota):
    """Test decoding of PGN 65266 (LFE)."""
    data = struct.pack(
        "<BBBBBBBB",
        0x80,  # fuel rate (0 L/h)
        0x00,  # fuel rate
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        50,  # throttle (20%)
        0,  # padding
    )
    result = kubota.decode_65266(data)
    assert result["PGN"] == 65266
    assert result["Fuel Rate (L/h)"] == 0.0
    assert result["Throttle Position (%)"] == 20.0


def test_decode_65271_vep1(kubota):
    """Test decoding of PGN 65271 (VEP1)."""
    data = struct.pack(
        "<BBBBBBBB",
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0x80,  # voltage (0V)
        0x00,  # voltage
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_65271(data)
    assert result["PGN"] == 65271
    assert result["Battery Voltage (V)"] == 0.0


def test_decode_65269_amb(kubota):
    """Test decoding of PGN 65269 (AMB)."""
    data = struct.pack(
        "<BBBBBBBB",
        200,  # pressure (100 kPa)
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_65269(data)
    assert result["PGN"] == 65269
    assert result["Barometric Pressure (kPa)"] == 100.0


def test_decode_65257_lfc(kubota):
    """Test decoding of PGN 65257 (LFC)."""
    data = struct.pack(
        "<BBBBBBBB",
        0,  # padding
        0,  # padding
        0,  # padding
        0,  # padding
        0x80,  # total fuel (0L)
        0x00,  # total fuel
        0x00,  # total fuel
        0x00,  # total fuel
    )
    result = kubota.decode_65257(data)
    assert result["PGN"] == 65257
    assert result["Total Fuel Used (L)"] == 0.0


def test_decode_65252_shutdn(kubota):
    """Test decoding of PGN 65252 (SHUTDN)."""
    data = struct.pack(
        "<BBBBBBBB",
        0,  # padding
        0,  # padding
        0,  # padding
        0x01,  # wait to start (1)
        0x02,  # shutdown (2)
        0,  # padding
        0,  # padding
        0,  # padding
    )
    result = kubota.decode_65252(data)
    assert result["PGN"] == 65252
    assert result["Wait to Start Lamp"] == 1
    assert result["Shutdown Active"] == 2


def test_decode_invalid_pgn(kubota):
    """Test decoding of invalid PGN."""
    result = kubota.decode(99999, b"\x00" * 8)
    assert "error" in result
    assert result["error"] == "No decoder for PGN 99999"


def test_on_message(kubota):
    """Test the on_message handler."""
    # Test with valid PGN
    with patch("builtins.print") as mock_print:
        data = struct.pack("<BBBBBBBB", 0, 0, 0, 0, 0, 0, 0, 0)
        kubota.on_message(61444, data)
        mock_print.assert_called()

    # Test with invalid PGN
    with patch("builtins.print") as mock_print:
        kubota.on_message(99999, b"\x00" * 8)
