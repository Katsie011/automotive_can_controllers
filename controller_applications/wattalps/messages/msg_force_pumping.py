from dataclasses import dataclass


@dataclass
class VmuBmsForcePumping:
    """
    BO_ 2180977152 VMU_BMS_FORCE_PUMPING: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """

    # VMU_BMS_FORCE_PUMPING
    MESSAGE_ID_FORCE_PUMPING = 2180977152
    NUM_BYTES = 8
    bms_dest_addr: int
    force_on: bool


def decode_force_pumping(data: bytes) -> VmuBmsForcePumping:
    assert len(data) == VmuBmsForcePumping.NUM_BYTES
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    bms_dest_addr = data[1]
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    force_on = data[0] & 0x01
    return VmuBmsForcePumping(
        bms_dest_addr=bms_dest_addr,
        force_on=bool(force_on),
    )


def encode_force_pumping(msg: VmuBmsForcePumping) -> bytes:
    data = bytearray(VmuBmsForcePumping.NUM_BYTES)
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    data[0] = int(msg.force_on) & 0x01
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    data[1] = msg.bms_dest_addr & 0xFF
    return data
