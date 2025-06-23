MESSAGE_ID_VMU_STATS = 2566864926

from dataclasses import dataclass


@dataclass
class BmsVmuStats:
    """
    BO_ 2566864926 BMS_VMU_STATS: 8 Vector__XXX
     SG_ CounterDischarge : 32|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
     SG_ CounterCharge : 0|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
    """

    NUM_BYTES = 8
    counter_discharge: int  # raw value, multiply by 0.01 for Ah
    counter_charge: int  # raw value, multiply by 0.01 for Ah


def decode_vmu_stats(data: bytes) -> BmsVmuStats:
    assert len(data) == BmsVmuStats.NUM_BYTES
    # SG_ CounterDischarge : 32|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
    counter_discharge = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7]
    # SG_ CounterCharge : 0|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
    counter_charge = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
    return BmsVmuStats(
        counter_discharge=counter_discharge,
        counter_charge=counter_charge,
    )


def encode_vmu_stats(msg: BmsVmuStats) -> bytes:
    data = bytearray(BmsVmuStats.NUM_BYTES)
    # SG_ CounterCharge : 0|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
    data[0] = (msg.counter_charge >> 24) & 0xFF
    data[1] = (msg.counter_charge >> 16) & 0xFF
    data[2] = (msg.counter_charge >> 8) & 0xFF
    data[3] = msg.counter_charge & 0xFF
    # SG_ CounterDischarge : 32|32@1+ (0.01,0) [0|4.29497e+007] "Ah" Vector__XXX
    data[4] = (msg.counter_discharge >> 24) & 0xFF
    data[5] = (msg.counter_discharge >> 16) & 0xFF
    data[6] = (msg.counter_discharge >> 8) & 0xFF
    data[7] = msg.counter_discharge & 0xFF
    return bytes(data)
