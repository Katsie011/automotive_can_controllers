from dataclasses import dataclass


@dataclass
class BmsVmuInfoTemperature:
    """
    BO_ 2566857246 BMS_VMU_INFO_TEMPERATURE: 3 Vector__XXX
     SG_ MaximumCellTemperature : 16|8@1- (1,0) [-128|127] "°C" Vector__XXX
     SG_ AverageCellTemperature : 8|8@1- (1,0) [-128|127] "°C" Vector__XXX
     SG_ MinimumCellTemperature : 0|8@1- (1,0) [-128|127] "°C" Vector__XXX
    """

    # BMS_VMU_INFO_TEMPERATURE
    MESSAGE_ID = 2566857246
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
