from dataclasses import dataclass


@dataclass
class BmsVmuInfoJbTemperature:
    """
    BO_ 2566857758 BMS_VMU_INFO_JB_TEMPERATURE: 8 Vector__XXX
     SG_ JunctionBoxThermTempMax : 48|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxThermTempMeas : 32|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxShuntTempMax : 16|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxShuntTempMeas : 0|16@1- (1,0) [-128|300] "°C" Vector__XXX
    """

    # BMS_VMU_INFO_JB_TEMPERATURE
    MESSAGE_ID = 2566857758
    junction_box_therm_temp_max: int  # °C
    junction_box_therm_temp_meas: int  # °C
    junction_box_shunt_temp_max: int  # °C
    junction_box_shunt_temp_meas: int  # °C
    NUM_BYTES = 8


def decode_info_jb_temperature(data: bytes) -> BmsVmuInfoJbTemperature:
    assert len(data) == BmsVmuInfoJbTemperature.NUM_BYTES
    # SG_ JunctionBoxThermTempMax : 48|16@1- (1,0) [-128|300] "°C" Vector__XXX
    therm_temp_max_raw = (data[6] << 8) | data[7]
    if therm_temp_max_raw & 0x8000:
        therm_temp_max_raw -= 0x10000
    # SG_ JunctionBoxThermTempMeas : 32|16@1- (1,0) [-128|300] "°C" Vector__XXX
    therm_temp_meas_raw = (data[4] << 8) | data[5]
    if therm_temp_meas_raw & 0x8000:
        therm_temp_meas_raw -= 0x10000
    # SG_ JunctionBoxShuntTempMax : 16|16@1- (1,0) [-128|300] "°C" Vector__XXX
    shunt_temp_max_raw = (data[2] << 8) | data[3]
    if shunt_temp_max_raw & 0x8000:
        shunt_temp_max_raw -= 0x10000
    # SG_ JunctionBoxShuntTempMeas : 0|16@1- (1,0) [-128|300] "°C" Vector__XXX
    shunt_temp_meas_raw = (data[0] << 8) | data[1]
    if shunt_temp_meas_raw & 0x8000:
        shunt_temp_meas_raw -= 0x10000
    return BmsVmuInfoJbTemperature(
        junction_box_therm_temp_max=therm_temp_max_raw,
        junction_box_therm_temp_meas=therm_temp_meas_raw,
        junction_box_shunt_temp_max=shunt_temp_max_raw,
        junction_box_shunt_temp_meas=shunt_temp_meas_raw,
    )


def encode_info_jb_temperature(msg: BmsVmuInfoJbTemperature) -> bytes:
    data = bytearray(BmsVmuInfoJbTemperature.NUM_BYTES)
    # SG_ JunctionBoxShuntTempMeas : 0|16@1- (1,0) [-128|300] "°C" Vector__XXX
    shunt_temp_meas_raw = msg.junction_box_shunt_temp_meas & 0xFFFF
    data[0] = (shunt_temp_meas_raw >> 8) & 0xFF
    data[1] = shunt_temp_meas_raw & 0xFF
    # SG_ JunctionBoxShuntTempMax : 16|16@1- (1,0) [-128|300] "°C" Vector__XXX
    shunt_temp_max_raw = msg.junction_box_shunt_temp_max & 0xFFFF
    data[2] = (shunt_temp_max_raw >> 8) & 0xFF
    data[3] = shunt_temp_max_raw & 0xFF
    # SG_ JunctionBoxThermTempMeas : 32|16@1- (1,0) [-128|300] "°C" Vector__XXX
    therm_temp_meas_raw = msg.junction_box_therm_temp_meas & 0xFFFF
    data[4] = (therm_temp_meas_raw >> 8) & 0xFF
    data[5] = therm_temp_meas_raw & 0xFF
    # SG_ JunctionBoxThermTempMax : 48|16@1- (1,0) [-128|300] "°C" Vector__XXX
    therm_temp_max_raw = msg.junction_box_therm_temp_max & 0xFFFF
    data[6] = (therm_temp_max_raw >> 8) & 0xFF
    data[7] = therm_temp_max_raw & 0xFF
    return bytes(data)
