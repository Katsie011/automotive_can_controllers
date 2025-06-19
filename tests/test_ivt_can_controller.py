import pytest
from unittest.mock import Mock, patch, MagicMock
import struct
import j1939
import sys
import os

# Append the root dir of the library suite... There has to be a better way to do this.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller_applications.ivt_can_controller import IVTSensor, Mode


@pytest.fixture
def ivt_sensor():
    # Patch can.interface.Bus and can.Notifier to avoid real CAN hardware access
    with patch(
        "controller_applications.ivt_can_controller.can.interface.Bus"
    ) as mock_bus, patch(
        "controller_applications.ivt_can_controller.can.Notifier"
    ) as mock_notifier:
        sensor = IVTSensor(name="TestIVT", channel="vcan0", bitrate=250000)
        sensor.logger = Mock()
        yield sensor


def test_initialization_ivtsensor(ivt_sensor):
    assert ivt_sensor.name == "TestIVT"
    assert ivt_sensor.channel == "vcan0"
    assert ivt_sensor.bitrate == 250000
    assert isinstance(ivt_sensor.logger, Mock)
    assert ivt_sensor.mode == Mode.RESET
    assert not ivt_sensor.running
    assert isinstance(ivt_sensor.results, dict)
    assert 0x00 in ivt_sensor.MESSAGE_IDS.keys()


def test_start_method(ivt_sensor):
    with patch.object(ivt_sensor, "_start_sensor") as mock_start_sensor:
        ivt_sensor.start()
        assert ivt_sensor.running
        assert ivt_sensor.mode == Mode.START
        mock_start_sensor.assert_called_once()
        ivt_sensor.logger.info.assert_called_with(
            "IVTSensor started and listening on bus."
        )


def test_stop_method(ivt_sensor):
    ivt_sensor.running = True
    ivt_sensor.notifier = Mock()
    with patch.object(ivt_sensor, "_stop_sensor") as mock_stop_sensor:
        ivt_sensor.stop()
        assert not ivt_sensor.running
        assert ivt_sensor.mode == Mode.STOP
        mock_stop_sensor.assert_called_once()
        ivt_sensor.notifier.stop.assert_called_once()
        ivt_sensor.logger.info.assert_called_with("IVTSensor stopped.")


# def test_on_can_message_with_result_id(ivt_sensor):
#     # Simulate a CAN message with a valid result arbitration_id
#     msg = MagicMock()
#     msg.arbitration_id = ivt_sensor.BASE_ID
#     msg.data = bytes([0x00, 0, 0, 0, 0, 0])
#     with patch.object(ivt_sensor, "on_message") as mock_on_message:
#         ivt_sensor._on_can_message(msg)
#         mock_on_message.assert_called_once_with(0x00, msg.data)


def test_on_can_message_with_resp_id(ivt_sensor):
    msg = MagicMock()
    msg.arbitration_id = ivt_sensor.RESP_ID
    msg.data = bytes([0x00, 0, 0, 0, 0, 0])
    ivt_sensor._on_can_message(msg)
    ivt_sensor.logger.debug.assert_called()


def test_on_message_with_valid_mux(ivt_sensor):
    # Use a valid mux id (0x00)
    data = bytes([0x00, 0, 0, 0, 0, 0])
    with patch.object(
        ivt_sensor,
        "decode",
        return_value={"label": "current", "value": 123, "unit": "mA"},
    ) as mock_decode:
        ivt_sensor.on_message(0x00, data)
        mock_decode.assert_called_once_with(0x00, data)
        ivt_sensor.logger.debug.assert_called()


def test_on_message_with_invalid_mux(ivt_sensor):
    # Use an invalid mux id (not in decoders)
    data = bytes([0xFF, 0, 0, 0, 0, 0])
    with patch.object(
        ivt_sensor, "decode", return_value={"error": "No decoder for PGN/Mux 0xFF"}
    ) as mock_decode:
        ivt_sensor.on_message(0xFF, data)
        mock_decode.assert_called_once_with(0xFF, data)
        # Should not call logger.debug for error dict


def test_decode_with_valid_mux(ivt_sensor):
    """Should use the correct decoder and return its result
        --- IVT CAN Controller Info ---
    - Result messages are 6 bytes: [MuxID, MsgCount/State, 4 bytes signed value]
    - Byte 0: MuxID (0x00..0x07)
    - Byte 1: Low nibble = MsgCount (0x0..0xF), High nibble = IVT_Result_state (bit 0: OCS, bit 1: out of range/reduced precision/measurement error, bit 2: any measurement error, bit 3: any system error)
    - Bytes 2-5: signed long value (big endian)
    - Not used bytes in response messages are 0x00.
    - Command/response messages are 8 bytes, big endian, padded with 0x00.
    """
    data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x64])  # MuxID=0, value=100
    with patch.object(
        ivt_sensor,
        "_decode_mux",
        return_value={"label": "current", "value": 100, "unit": "mA"},
    ) as mock_decoder:
        result = ivt_sensor.decode(0x00, data)
        assert result["label"] == "current"
        assert result["value"] == 100
        assert result["unit"] == "mA"
        mock_decoder.assert_called_once_with(data)


def test_decode_with_invalid_mux(ivt_sensor):
    # Should return error dict if no decoder exists for PGN/Mux
    data = bytes([0x09, 0, 0, 0, 0, 0])
    result = ivt_sensor.decode(0x09, data)
    assert "error" in result
    assert result["error"] == "No decoder for PGN/Mux 9"


def test__decode_mux_valid_data(ivt_sensor):
    """
    --- IVT CAN Controller Info ---
    - _decode_mux expects 6 bytes: [MuxID, MsgCount/State, 4 bytes value]
    - Value is signed long, big endian, unit depends on MuxID.
    - For temperature (MuxID=0x04), value is in 0.1C, so divide by 10.
    """
    # Test for current (MuxID=0x00, unit mA)
    data = bytes([0x00, 0x12, 0x00, 0x00, 0x03, 0xE8])  # value=1000
    result = ivt_sensor._decode_mux(data)
    assert result["label"] == "current"
    assert result["value"] == 1000
    assert result["unit"] == "mA"
    assert result["msg_count"] == 0x2
    assert result["state_bits"] == 0x1

    # Test for temperature (MuxID=0x04, unit 0.1C, value=250 -> 25.0C)
    data = bytes([0x04, 0x10, 0x00, 0x00, 0x00, 0xFA])  # value=250
    result = ivt_sensor._decode_mux(data)
    assert result["label"] == "temperature"
    assert result["value"] == 25.0
    assert result["unit"] == "0.1C"


def test__decode_mux_invalid_length(ivt_sensor):
    """
    Should warn and return {} if data is not 6 bytes
    """
    data = bytes([0x00, 0x00, 0x00])  # too short
    result = ivt_sensor._decode_mux(data)
    assert result == {}
    ivt_sensor.logger.warning.assert_called_with("Unexpected data length")


def test_send_command(ivt_sensor):
    """
    --- IVT CAN Controller Info ---
    - send_command sends a CAN message with CMD_ID, data padded to 8 bytes, not extended.
    """
    ivt_sensor.bus = Mock()
    data = b"\x34\x01\x01\x00\x00"
    with patch("controller_applications.ivt_can_controller.can.Message") as mock_msg:
        ivt_sensor.send_command(data)
        mock_msg.assert_called_once()
        args, kwargs = mock_msg.call_args
        assert kwargs["arbitration_id"] == ivt_sensor.CMD_ID
        assert kwargs["data"] == data.ljust(8, b"\x00")
        assert kwargs["is_extended_id"] is False
        ivt_sensor.bus.send.assert_called_once()


def test_read_response_with_response(ivt_sensor):
    """
    --- IVT CAN Controller Info ---
    - read_response waits for a message with RESP_ID, returns it if found, else warns.
    """
    mock_msg = Mock()
    mock_msg.arbitration_id = ivt_sensor.RESP_ID
    ivt_sensor.bus = Mock()
    ivt_sensor.bus.recv = Mock(return_value=mock_msg)
    result = ivt_sensor.read_response(timeout=0.1)
    assert result == mock_msg
    ivt_sensor.logger.debug.assert_called_with(f"Received response: {mock_msg}")


def test_read_response_timeout(ivt_sensor):
    """
    Test that read_response returns None and warns if no response is received.
    """
    ivt_sensor.bus = Mock()
    ivt_sensor.bus.recv = Mock(return_value=None)
    result = ivt_sensor.read_response(timeout=0.01)
    assert result is None
    ivt_sensor.logger.warning.assert_called_with("No response received.")


def test__start_sensor(ivt_sensor):
    """
    --- IVT CAN Controller Info ---
    - _start_sensor sends a command (0x34, 0x01, 0x01, 0x00, 0x0000) and reads response.
    """
    with patch.object(ivt_sensor, "send_command") as mock_send, patch.object(
        ivt_sensor, "read_response"
    ) as mock_read:
        ivt_sensor._start_sensor()
        mock_send.assert_called_once()
        mock_read.assert_called_once()


def test__stop_sensor(ivt_sensor):
    """
    - _stop_sensor sends a command (0x34, 0x00, 0x00, 0x00, 0x0000) and reads response.
    """
    with patch.object(ivt_sensor, "send_command") as mock_send, patch.object(
        ivt_sensor, "read_response"
    ) as mock_read:
        ivt_sensor._stop_sensor()
        mock_send.assert_called_once()
        mock_read.assert_called_once()


def test_reset_errors(ivt_sensor):
    """
    - reset_errors sends a command (0x30, 0x03, 0x00, 0x00, 0x00000000) and reads response.
    """
    with patch.object(ivt_sensor, "send_command") as mock_send, patch.object(
        ivt_sensor, "read_response"
    ) as mock_read:
        ivt_sensor.reset_errors()
        mock_send.assert_called_once()
        mock_read.assert_called_once()


def test_trigger_measurement(ivt_sensor):
    """
    - trigger_measurement sends a command (0x31, channels) and reads response.
    """
    with patch.object(ivt_sensor, "send_command") as mock_send, patch.object(
        ivt_sensor, "read_response"
    ) as mock_read:
        ivt_sensor.trigger_measurement(channels=0xAA)
        mock_send.assert_called_once()
        mock_read.assert_called_once()


def test_get_latest_results(ivt_sensor):
    """
    Test that get_latest_results returns a copy of the results dictionary.
    Should be a copy, not a reference.
    """
    ivt_sensor.results = {"current": 123, "voltage_u1": 456}
    results = ivt_sensor.get_latest_results()
    assert results == {"current": 123, "voltage_u1": 456}
    # Should be a copy, not a reference
    results["current"] = 0
    assert ivt_sensor.results["current"] == 123
