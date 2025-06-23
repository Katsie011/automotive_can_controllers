from dataclasses import dataclass

# VMU_BMS_FORCE_HEATING
MESSAGE_ID_FORCE_HEATING = 2180976640


@dataclass
class VmuBmsForceHeating:
    """
    BO_ 2180976640 VMU_BMS_FORCE_HEATING: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """

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


# VMU_BMS_FORCE_COOLING
MESSAGE_ID_FORCE_COOLING = 2180976896


@dataclass
class VmuBmsForceCooling:
    """
    BO_ 2180976896 VMU_BMS_FORCE_COOLING: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """

    NUM_BYTES = 8
    bms_dest_addr: int
    force_off: bool
    force_on: bool


def decode_force_cooling(data: bytes) -> VmuBmsForceCooling:
    assert len(data) == VmuBmsForceCooling.NUM_BYTES
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    bms_dest_addr = data[1]
    # SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
    force_off = (data[0] >> 1) & 0x01
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    force_on = data[0] & 0x01
    return VmuBmsForceCooling(
        bms_dest_addr=bms_dest_addr,
        force_off=bool(force_off),
        force_on=bool(force_on),
    )


def encode_force_cooling(msg: VmuBmsForceCooling) -> bytes:
    data = bytearray(VmuBmsForceCooling.NUM_BYTES)
    # SG_ ForceOff : 1|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    data[0] = ((int(msg.force_off) & 0x01) << 1) | (int(msg.force_on) & 0x01)
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    data[1] = msg.bms_dest_addr & 0xFF
    return data


# VMU_BMS_FORCE_PUMPING
MESSAGE_ID_FORCE_PUMPING = 2180977152


@dataclass
class VmuBmsForcePumping:
    """
    BO_ 2180977152 VMU_BMS_FORCE_PUMPING: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ ForceOn : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """

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
