from dataclasses import dataclass


@dataclass
class BmsVmuSpCharge:
    """
    BO_ 2566849054 BMS_VMU_SP_CHARGE: 4 Vector__XXX
    SG_ MaxChargeCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    SG_ ChargeVoltage : 0|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    """

    MESSAGE_ID = 2566849054
    NUM_BYTES = 4
    max_charge_current: float  # A
    max_charge_voltage: float  # V


def decode_charge(data: bytes) -> BmsVmuSpCharge:
    assert len(data) == BmsVmuSpCharge.NUM_BYTES
    # SG_ MaxChargeCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_charge_current = (data[2] << 8) | data[3]
    max_charge_current = max_charge_current * 0.1
    # SG_ ChargeVoltage : 0|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    max_charge_voltage = (data[0] << 8) | data[1]
    max_charge_voltage = max_charge_voltage * 0.1
    return BmsVmuSpCharge(
        max_charge_current=max_charge_current, max_charge_voltage=max_charge_voltage
    )


def encode_charge(msg: BmsVmuSpCharge) -> bytes:
    # SG_ MaxChargeCurrent : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    max_charge_current_raw = int(round(msg.max_charge_current / 0.1)) & 0xFFFF
    # SG_ ChargeVoltage : 0|16@1+ (0.1,0) [0|6553.5] "V" Vector__XXX
    max_charge_voltage_raw = int(round(msg.max_charge_voltage / 0.1)) & 0xFFFF
    data = bytearray(BmsVmuSpCharge.NUM_BYTES)
    data[0] = (max_charge_voltage_raw >> 8) & 0xFF
    data[1] = max_charge_voltage_raw & 0xFF
    data[2] = (max_charge_current_raw >> 8) & 0xFF
    data[3] = max_charge_current_raw & 0xFF
    return bytes(data)
