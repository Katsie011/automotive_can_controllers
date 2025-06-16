import pytest
from unittest.mock import Mock, patch
import struct
import j1939
import sys
import os

# Append the root dir of the library suite... There has to be a better way to do this.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller_applications.bender_ISO175_j1939 import ISO175_CA


@pytest.fixture
def iso175():
    """Fixture to create and configure ISO175_CA instance for testing."""
    with patch("j1939.ControllerApplication.__init__", return_value=None):
        iso175 = ISO175_CA("ISO175")
        iso175._ecu = Mock()
        # TODO check if this runs without the
        # iso175.state = j1939.ControllerApplication.State.NORMAL
        return iso175


def test_initialization(iso175):
    """Test proper initialization of the ISO175_CA class."""
    assert iso175.source_address == 0xF4
    assert 65281 in iso175.decoders
    assert 65282 in iso175.decoders
    assert 65283 in iso175.decoders
    assert 65284 in iso175.decoders
    assert iso175.cyclic_message_functions == {}


def test_decode_pgn_65281_general_info(iso175):
    """Test decoding of PGN 65281 (General Info)."""
    # Test case 1: Normal operation
    data = struct.pack(
        "<HBBHB",
        1000,  # r_iso_corr (1000 kΩ)
        0xFE,  # r_iso_status (normal operation)
        42,  # measurement counter
        0x0000,  # no alarms
        1,  # device state (Normal)
    )
    result = iso175.decode_pgn_65281(data)
    assert result["r_iso_corrected"] == 1000
    assert result["r_iso_status"] == 0xFE
    assert result["r_iso_status_meaning"] == "isolation value in normal operation"
    assert result["measurement_counter"] == 42
    assert result["device_state"] == 1
    assert result["device_state_meaning"] == "Normal"

    # Test case 2: SNV (Signal Not Valid)
    data = struct.pack(
        "<HBBHB",
        0xFFFF,  # r_iso_corr (SNV)
        0xFF,  # r_iso_status (SNV)
        0,  # measurement counter
        0x0000,  # no alarms
        0,  # device state (Init)
    )
    result = iso175.decode_pgn_65281(data)
    assert result["r_iso_corrected"] == "SNV"
    assert result["r_iso_status"] == 0xFF
    assert result["r_iso_status_meaning"] == "SNV"


def test_decode_pgn_65282_isolation_detail(iso175):
    """Test decoding of PGN 65282 (Isolation Detail)."""
    data = struct.pack(
        "<HHHBB",
        1000,  # r_kΩ_negative
        2000,  # r_kΩ_positive
        1500,  # r_kΩ_original
        42,  # measurement counter
        75,  # measurement quality (75%)
    )
    result = iso175.decode_pgn_65282(data)
    assert result["isolation_negative"] == 1000
    assert result["isolation_positive"] == 2000
    assert result["isolation_original"] == 1500
    assert result["measurement_count"] == 42
    assert result["measurement_quality"] == 75


def test_decode_pgn_65283_voltage_info(iso175):
    """Test decoding of PGN 65283 (Voltage Info)."""
    # Test case with specific voltage values
    hv_sys = int(400 / 0.05)  # 400V
    hv_neg = int(-100 / 0.05) + 32128  # -100V
    hv_pos = int(300 / 0.05) + 32128  # 300V

    data = struct.pack("<HHH", hv_sys, hv_neg, hv_pos)
    result = iso175.decode_pgn_65283(data)
    assert result["hv_system_voltage"] == pytest.approx(400.0)
    assert result["hv_negative_to_earth"] == pytest.approx(-100.0)
    assert result["hv_positive_to_earth"] == pytest.approx(300.0)


def test_decode_pgn_65284_it_system(iso175):
    """Test decoding of PGN 65284 (IT-System Info)."""
    # Test case 1: Normal values
    data = struct.pack(
        "<HBBBH",
        100,  # capacity (10.0 μF)
        42,  # capacity measurement counter
        50,  # unbalance measure value (50%)
        1,  # unbalance measurement counter
        # TODO Check if we can remove this padding
        # 0,  # padding
        600,  # voltage frequency (60.0 Hz)
    )
    result = iso175.decode_pgn_65284(data)
    assert result["capacity_measured"] == 100
    assert result["capacity_measure_count"] == 42
    assert result["unbalance_measure_value"] == 50
    assert result["unbalance_measurement"] == 1
    assert result["voltage_frequency"] == 600

    # Test case 2: SNV for capacity
    data = struct.pack(
        "<HBBBBH",
        0xFFFF,  # capacity (SNV)
        42,  # capacity measurement counter
        50,  # unbalance measure value
        1,  # unbalance measurement counter
        0,  # padding
        600,  # voltage frequency
    )
    result = iso175.decode_pgn_65284(data)
    assert result["capacity_measured"] == "SNV"


def test_decode_invalid_pgn(iso175):
    """Test decoding of invalid PGN."""
    result = iso175.decode(99999, b"\x00" * 8)
    assert "error" in result
    assert result["error"] == "No decoder for PGN 99999"


def test_on_message(iso175):
    """Test the on_message handler."""
    # Test with valid PGN
    with patch("builtins.print") as mock_print:
        data = struct.pack(
            "<HBBHB",
            1000,  # r_iso_corr (1000 kΩ)
            0xFE,  # r_iso_status (normal operation)
            42,  # measurement counter
            0x0000,  # no alarms
            1,  # device state (Normal)
        )
        iso175.on_message(65281, data)
        mock_print.assert_called()

    # Test with invalid PGN
    with patch("builtins.print") as mock_print:
        iso175.on_message(99999, b"\x00" * 8)
        mock_print.assert_called_with("PGN 99999 length 8")


def test_start_stop(iso175):
    """Test start and stop methods."""
    # Mock the parent class methods
    iso175.start()
    iso175.stop()

    # Verify that the parent class methods were called
    assert hasattr(iso175, "_ecu")
