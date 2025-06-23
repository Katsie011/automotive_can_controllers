from dataclasses import dataclass


@dataclass
class BmsVmuSpDrive:
    """
    BO_ 2566849310 BMS_VMU_SP_DRIVE: 4 Vector__XXX
     SG_ MaxRegenCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ MaxDischargeCurrent : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566849310
    NUM_BYTES = 4
    max_regen_current: float  # in A
    max_discharge_current: float  # in A


def decode_drive(data: bytes) -> BmsVmuSpDrive:
    assert len(data) == BmsVmuSpDrive.NUM_BYTES
    # SG_ MaxRegenCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_regen_current_raw = (data[2] << 8) | data[3]
    max_regen_current = max_regen_current_raw * 0.1
    # SG_ MaxDischargeCurrent : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_discharge_current_raw = (data[0] << 8) | data[1]
    max_discharge_current = max_discharge_current_raw * 0.1
    return BmsVmuSpDrive(
        max_regen_current=max_regen_current,
        max_discharge_current=max_discharge_current,
    )


def encode_drive(msg: BmsVmuSpDrive) -> bytes:
    # SG_ MaxRegenCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_regen_current_raw = int(round(msg.max_regen_current / 0.1)) & 0xFFFF
    # SG_ MaxDischargeCurrent : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_discharge_current_raw = int(round(msg.max_discharge_current / 0.1)) & 0xFFFF
    data = bytearray(BmsVmuSpDrive.NUM_BYTES)
    data[0] = (max_discharge_current_raw >> 8) & 0xFF
    data[1] = max_discharge_current_raw & 0xFF
    data[2] = (max_regen_current_raw >> 8) & 0xFF
    data[3] = max_regen_current_raw & 0xFF
    return bytes(data)
