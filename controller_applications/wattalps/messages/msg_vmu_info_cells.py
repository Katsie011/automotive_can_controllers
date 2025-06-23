from dataclasses import dataclass


@dataclass
class BmsVmuInfoCells:
    """
    BO_ 2566856990 BMS_VMU_INFO_CELLS: 6 Vector__XXX
     SG_ MaximumCellVoltage : 32|16@1+ (1,0) [0|5000] "mV" Vector__XXX
     SG_ AverageCellVoltage : 16|16@1+ (1,0) [0|5000] "mV" Vector__XXX
     SG_ MinimumCellVoltage : 0|16@1+ (1,0) [0|5000] "mV" Vector__XXX
    """

    # BMS_VMU_INFO_CELLS
    MESSAGE_ID = 2566856990
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
