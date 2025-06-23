from dataclasses import dataclass

# BMS_VMU_INFO
MESSAGE_ID_INFO = 2566856734


@dataclass
class BmsVmuInfo:
    """
    BO_ 2566856734 BMS_VMU_INFO: 7 Vector__XXX
     SG_ SOH : 48|8@1+ (1,0) [0|100] "%" Vector__XXX
     SG_ DownStreamVoltage : 32|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
     SG_ UpStreamVoltage : 16|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
     SG_ Current : 0|16@1- (0.1,0) [-3276.8|3276.7] "A" Vector__XXX
    """

    soh: int  # %
    downstream_voltage: float  # V
    upstream_voltage: float  # V
    current: float  # A
    NUM_BYTES = 7


def decode_info(data: bytes) -> BmsVmuInfo:
    assert len(data) == BmsVmuInfo.NUM_BYTES
    # SG_ SOH : 48|8@1+ (1,0) [0|100] "%" Vector__XXX
    soh = data[6]
    # SG_ DownStreamVoltage : 32|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    downstream_voltage_raw = (data[4] << 8) | data[5]
    downstream_voltage = downstream_voltage_raw * 0.1
    # SG_ UpStreamVoltage : 16|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    upstream_voltage_raw = (data[2] << 8) | data[3]
    upstream_voltage = upstream_voltage_raw * 0.1
    # SG_ Current : 0|16@1- (0.1,0) [-3276.8|3276.7] "A" Vector__XXX
    current_raw = (data[0] << 8) | data[1]
    if current_raw & 0x8000:
        current_raw -= 0x10000
    current = current_raw * 0.1
    return BmsVmuInfo(
        soh=soh,
        downstream_voltage=downstream_voltage,
        upstream_voltage=upstream_voltage,
        current=current,
    )


def encode_info(msg: BmsVmuInfo) -> bytes:
    data = bytearray(BmsVmuInfo.NUM_BYTES)
    # SG_ Current : 0|16@1- (0.1,0) [-3276.8|3276.7] "A" Vector__XXX
    current_raw = int(round(msg.current / 0.1)) & 0xFFFF
    data[0] = (current_raw >> 8) & 0xFF
    data[1] = current_raw & 0xFF
    # SG_ UpStreamVoltage : 16|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    upstream_voltage_raw = int(round(msg.upstream_voltage / 0.1)) & 0xFFFF
    data[2] = (upstream_voltage_raw >> 8) & 0xFF
    data[3] = upstream_voltage_raw & 0xFF
    # SG_ DownStreamVoltage : 32|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    downstream_voltage_raw = int(round(msg.downstream_voltage / 0.1)) & 0xFFFF
    data[4] = (downstream_voltage_raw >> 8) & 0xFF
    data[5] = downstream_voltage_raw & 0xFF
    # SG_ SOH : 48|8@1+ (1,0) [0|100] "%" Vector__XXX
    data[6] = msg.soh & 0xFF
    return bytes(data)


# BMS_VMU_INFO_CELLS
MESSAGE_ID_INFO_CELLS = 2566856990


@dataclass
class BmsVmuInfoCells:
    """
    BO_ 2566856990 BMS_VMU_INFO_CELLS: 6 Vector__XXX
     SG_ MaximumCellVoltage : 32|16@1+ (1,0) [0|5000] "mV" Vector__XXX
     SG_ AverageCellVoltage : 16|16@1+ (1,0) [0|5000] "mV" Vector__XXX
     SG_ MinimumCellVoltage : 0|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    """

    maximum_cell_voltage: int  # mV
    average_cell_voltage: int  # mV
    minimum_cell_voltage: int  # mV
    NUM_BYTES = 6


def decode_info_cells(data: bytes) -> BmsVmuInfoCells:
    assert len(data) == BmsVmuInfoCells.NUM_BYTES
    # SG_ MaximumCellVoltage : 32|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    maximum_cell_voltage = (data[4] << 8) | data[5]
    # SG_ AverageCellVoltage : 16|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    average_cell_voltage = (data[2] << 8) | data[3]
    # SG_ MinimumCellVoltage : 0|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    minimum_cell_voltage = (data[0] << 8) | data[1]
    return BmsVmuInfoCells(
        maximum_cell_voltage=maximum_cell_voltage,
        average_cell_voltage=average_cell_voltage,
        minimum_cell_voltage=minimum_cell_voltage,
    )


def encode_info_cells(msg: BmsVmuInfoCells) -> bytes:
    data = bytearray(BmsVmuInfoCells.NUM_BYTES)
    # SG_ MinimumCellVoltage : 0|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    data[0] = (msg.minimum_cell_voltage >> 8) & 0xFF
    data[1] = msg.minimum_cell_voltage & 0xFF
    # SG_ AverageCellVoltage : 16|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    data[2] = (msg.average_cell_voltage >> 8) & 0xFF
    data[3] = msg.average_cell_voltage & 0xFF
    # SG_ MaximumCellVoltage : 32|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    data[4] = (msg.maximum_cell_voltage >> 8) & 0xFF
    data[5] = msg.maximum_cell_voltage & 0xFF
    return bytes(data)


# BMS_VMU_INFO_TEMPERATURE
MESSAGE_ID_INFO_TEMPERATURE = 2566857246


@dataclass
class BmsVmuInfoTemperature:
    """
    BO_ 2566857246 BMS_VMU_INFO_TEMPERATURE: 3 Vector__XXX
     SG_ MaximumCellTemperature : 16|8@1- (1,0) [-128|127] "°C" Vector__XXX
     SG_ AverageCellTemperature : 8|8@1- (1,0) [-128|127] "°C" Vector__XXX
     SG_ MinimumCellTemperature : 0|8@1- (1,0) [-128|127] "°C" Vector__XXX
    """

    maximum_cell_temperature: int  # °C
    average_cell_temperature: int  # °C
    minimum_cell_temperature: int  # °C
    NUM_BYTES = 3


def decode_info_temperature(data: bytes) -> BmsVmuInfoTemperature:
    assert len(data) == BmsVmuInfoTemperature.NUM_BYTES
    # SG_ MaximumCellTemperature : 16|8@1- (1,0) [-128|127] "°C" Vector__XXX
    max_temp = data[2]
    if max_temp >= 0x80:
        max_temp -= 0x100
    # SG_ AverageCellTemperature : 8|8@1- (1,0) [-128|127] "°C" Vector__XXX
    avg_temp = data[1]
    if avg_temp >= 0x80:
        avg_temp -= 0x100
    # SG_ MinimumCellTemperature : 0|8@1- (1,0) [-128|127] "°C" Vector__XXX
    min_temp = data[0]
    if min_temp >= 0x80:
        min_temp -= 0x100
    return BmsVmuInfoTemperature(
        maximum_cell_temperature=max_temp,
        average_cell_temperature=avg_temp,
        minimum_cell_temperature=min_temp,
    )


def encode_info_temperature(msg: BmsVmuInfoTemperature) -> bytes:
    data = bytearray(BmsVmuInfoTemperature.NUM_BYTES)
    # SG_ MinimumCellTemperature : 0|8@1- (1,0) [-128|127] "°C" Vector__XXX
    data[0] = msg.minimum_cell_temperature & 0xFF
    # SG_ AverageCellTemperature : 8|8@1- (1,0) [-128|127] "°C" Vector__XXX
    data[1] = msg.average_cell_temperature & 0xFF
    # SG_ MaximumCellTemperature : 16|8@1- (1,0) [-128|127] "°C" Vector__XXX
    data[2] = msg.maximum_cell_temperature & 0xFF
    return bytes(data)


# BMS_VMU_INFO_INSULATION
MESSAGE_ID_INFO_INSULATION = 2566857502


@dataclass
class BmsVmuInfoInsulation:
    """
    BO_ 2566857502 BMS_VMU_INFO_INSULATION: 4 Vector__XXX
     SG_ InsulationResistance : 0|32@1+ (1,0) [0|1e+006] "kOhm" Vector__XXX
    """

    insulation_resistance: int  # kOhm


def decode_info_insulation(data: bytes) -> BmsVmuInfoInsulation:
    assert len(data) == 4
    # SG_ InsulationResistance : 0|32@1+ (1,0) [0|1e+006] "kOhm" Vector__XXX
    insulation_resistance = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    return BmsVmuInfoInsulation(
        insulation_resistance=insulation_resistance,
    )


def encode_info_insulation(msg: BmsVmuInfoInsulation) -> bytes:
    # SG_ InsulationResistance : 0|32@1+ (1,0) [0|1e+006] "kOhm" Vector__XXX
    val = msg.insulation_resistance & 0xFFFFFFFF
    return bytes(
        [
            (val >> 24) & 0xFF,
            (val >> 16) & 0xFF,
            (val >> 8) & 0xFF,
            val & 0xFF,
        ]
    )


# BMS_VMU_INFO_JB_TEMPERATURE
MESSAGE_ID_INFO_JB_TEMPERATURE = 2566857758


@dataclass
class BmsVmuInfoJbTemperature:
    """
    BO_ 2566857758 BMS_VMU_INFO_JB_TEMPERATURE: 8 Vector__XXX
     SG_ JunctionBoxThermTempMax : 48|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxThermTempMeas : 32|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxShuntTempMax : 16|16@1- (1,0) [-128|300] "°C" Vector__XXX
     SG_ JunctionBoxShuntTempMeas : 0|16@1- (1,0) [-128|300] "°C" Vector__XXX
    """

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
