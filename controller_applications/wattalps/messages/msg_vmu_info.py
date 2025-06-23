from dataclasses import dataclass


@dataclass
class BmsVmuInfo:
    """
    BO_ 2566856734 BMS_VMU_INFO: 7 Vector__XXX
     SG_ SOH : 48|8@1+ (1,0) [0|100] "%" Vector__XXX
     SG_ DownStreamVoltage : 32|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
     SG_ UpStreamVoltage : 16|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
     SG_ Current : 0|16@1- (0.1,0) [-3276.8|3276.7] "A" Vector__XXX
    """

    # BMS_VMU_INFO
    MESSAGE_ID = 2566856734
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
