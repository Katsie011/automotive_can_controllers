from dataclasses import dataclass


@dataclass
class BmsVmuInfoInsulation:
    """
    BO_ 2566857502 BMS_VMU_INFO_INSULATION: 4 Vector__XXX
     SG_ InsulationResistance : 0|32@1+ (1,0) [0|1e+006] "kOhm" Vector__XXX
    """

    # BMS_VMU_INFO_INSULATION
    MESSAGE_ID = 2566857502
    NUM_BYTES = 4
    insulation_resistance: int  # kOhm


def decode_info_insulation(data: bytes) -> BmsVmuInfoInsulation:
    assert len(data) == BmsVmuInfoInsulation.NUM_BYTES
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
