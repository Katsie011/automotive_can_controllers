from dataclasses import dataclass


@dataclass
class BmsVmuConfVersion:
    """
    BO_ 2566861598 BMS_VMU_CONF_VERSION: 8 Vector__XXX
    SG_ ApplConfVerChar_3 : 56|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ ApplConfVerChar_2 : 48|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ ApplConfVerChar_1 : 40|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ ApplConfVerChar_0 : 32|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ SafetyConfVerChar_3 : 24|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ SafetyConfVerChar_2 : 16|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ SafetyConfVerChar_1 : 8|8@1+ (1,0) [0|255] "" Vector__XXX
    SG_ SafetyConfVerChar_0 : 0|8@1+ (1,0) [0|255] "" Vector__XXX
    """

    MESSAGE_ID = 2566861598
    NUM_BYTES = 8
    appl_conf_ver_char_3: int
    appl_conf_ver_char_2: int
    appl_conf_ver_char_1: int
    appl_conf_ver_char_0: int
    safety_conf_ver_char_3: int
    safety_conf_ver_char_2: int
    safety_conf_ver_char_1: int
    safety_conf_ver_char_0: int


def decode_conf_version(data: bytes) -> BmsVmuConfVersion:
    assert len(data) == BmsVmuConfVersion.NUM_BYTES
    # SG_ ApplConfVerChar_3 : 56|8@1+ (1,0) [0|255] "" Vector__XXX
    appl_conf_ver_char_3 = data[7]
    # SG_ ApplConfVerChar_2 : 48|8@1+ (1,0) [0|255] "" Vector__XXX
    appl_conf_ver_char_2 = data[6]
    # SG_ ApplConfVerChar_1 : 40|8@1+ (1,0) [0|255] "" Vector__XXX
    appl_conf_ver_char_1 = data[5]
    # SG_ ApplConfVerChar_0 : 32|8@1+ (1,0) [0|255] "" Vector__XXX
    appl_conf_ver_char_0 = data[4]
    # SG_ SafetyConfVerChar_3 : 24|8@1+ (1,0) [0|255] "" Vector__XXX
    safety_conf_ver_char_3 = data[3]
    # SG_ SafetyConfVerChar_2 : 16|8@1+ (1,0) [0|255] "" Vector__XXX
    safety_conf_ver_char_2 = data[2]
    # SG_ SafetyConfVerChar_1 : 8|8@1+ (1,0) [0|255] "" Vector__XXX
    safety_conf_ver_char_1 = data[1]
    # SG_ SafetyConfVerChar_0 : 0|8@1+ (1,0) [0|255] "" Vector__XXX
    safety_conf_ver_char_0 = data[0]
    return BmsVmuConfVersion(
        appl_conf_ver_char_3=appl_conf_ver_char_3,
        appl_conf_ver_char_2=appl_conf_ver_char_2,
        appl_conf_ver_char_1=appl_conf_ver_char_1,
        appl_conf_ver_char_0=appl_conf_ver_char_0,
        safety_conf_ver_char_3=safety_conf_ver_char_3,
        safety_conf_ver_char_2=safety_conf_ver_char_2,
        safety_conf_ver_char_1=safety_conf_ver_char_1,
        safety_conf_ver_char_0=safety_conf_ver_char_0,
    )


def encode_conf_version(msg: BmsVmuConfVersion) -> bytes:
    data = bytearray(BmsVmuConfVersion.NUM_BYTES)
    # SG_ SafetyConfVerChar_0 : 0|8@1+ (1,0) [0|255] "" Vector__XXX
    data[0] = msg.safety_conf_ver_char_0 & 0xFF
    # SG_ SafetyConfVerChar_1 : 8|8@1+ (1,0) [0|255] "" Vector__XXX
    data[1] = msg.safety_conf_ver_char_1 & 0xFF
    # SG_ SafetyConfVerChar_2 : 16|8@1+ (1,0) [0|255] "" Vector__XXX
    data[2] = msg.safety_conf_ver_char_2 & 0xFF
    # SG_ SafetyConfVerChar_3 : 24|8@1+ (1,0) [0|255] "" Vector__XXX
    data[3] = msg.safety_conf_ver_char_3 & 0xFF
    # SG_ ApplConfVerChar_0 : 32|8@1+ (1,0) [0|255] "" Vector__XXX
    data[4] = msg.appl_conf_ver_char_0 & 0xFF
    # SG_ ApplConfVerChar_1 : 40|8@1+ (1,0) [0|255] "" Vector__XXX
    data[5] = msg.appl_conf_ver_char_1 & 0xFF
    # SG_ ApplConfVerChar_2 : 48|8@1+ (1,0) [0|255] "" Vector__XXX
    data[6] = msg.appl_conf_ver_char_2 & 0xFF
    # SG_ ApplConfVerChar_3 : 56|8@1+ (1,0) [0|255] "" Vector__XXX
    data[7] = msg.appl_conf_ver_char_3 & 0xFF
    return bytes(data)
