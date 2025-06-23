from dataclasses import dataclass


@dataclass
class VmuBmsForceHeating:
    """
    BO_ 2180976640 VMU_BMS_FORCE_HEATING: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """

    MESSAGE_ID_FORCE_HEATING = 2180976640
    NUM_BYTES = 8
    bms_dest_addr: int
    force_off: bool
    force_on: bool


def decode_force_heating(data: bytes) -> VmuBmsForceHeating:
    assert len(data) == VmuBmsForceHeating.NUM_BYTES
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    bms_dest_addr = data[1]
    # SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
    force_off = (data[0] >> 1) & 0x01
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    force_on = data[0] & 0x01
    return VmuBmsForceHeating(
        bms_dest_addr=bms_dest_addr,
        force_off=bool(force_off),
        force_on=bool(force_on),
    )


def encode_force_heating(msg: VmuBmsForceHeating) -> bytes:
    data = bytearray(VmuBmsForceHeating.NUM_BYTES)
    # SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    data[0] = ((int(msg.force_off) & 0x01) << 1) | (int(msg.force_on) & 0x01)
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    data[1] = msg.bms_dest_addr & 0xFF
    return data
