# -------------------- VMU_BMS_STATUS --------------------

from dataclasses import dataclass


@dataclass
class VmuBmsStatus:
    """
    BO_ 2180972544 VMU_BMS_STATUS: 8 Vector__XXX
     SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
     SG_ InsuResMeasEn : 4|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ AskMode : 0|2@1+ (1,0) [0|2] "" Vector__XXX
    """

    MESSAGE_ID = 2180972544
    NUM_BYTES = 8
    bms_dest_addr: int
    insu_res_meas_en: bool
    ask_mode: int
    ASK_MODE_DRIVE = 2
    ASK_MODE_CHARGE = 1
    ASK_MODE_STANDBY = 0


def decode_vmu_bms_status(data: bytes) -> VmuBmsStatus:
    assert len(data) == VmuBmsStatus.NUM_BYTES
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    bms_dest_addr = data[1]
    # SG_ InsuResMeasEn : 4|1@1- (1,0) [0|1] "" Vector__XXX
    insu_res_meas_en = (data[0] >> 4) & 0x01
    # SG_ AskMode : 0|2@1+ (1,0) [0|2] "" Vector__XXX
    ask_mode = data[0] & 0x03
    return VmuBmsStatus(
        bms_dest_addr=bms_dest_addr,
        insu_res_meas_en=bool(insu_res_meas_en),
        ask_mode=ask_mode,
    )


def encode_vmu_bms_status(msg: VmuBmsStatus) -> bytes:
    data = bytearray(VmuBmsStatus.NUM_BYTES)
    # SG_ InsuResMeasEn : 4|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ AskMode : 0|2@1+ (1,0) [0|2] "" Vector__XXX
    data[0] = ((int(msg.insu_res_meas_en) & 0x01) << 4) | (msg.ask_mode & 0x03)
    # SG_ BmsDestAddr : 8|8@1+ (1,0) [256|0] "" Vector__XXX
    data[1] = msg.bms_dest_addr & 0xFF
    return data


# -------------------- BMS_VMU_STATUS --------------------


@dataclass
class BmsVmuStatus:
    """
    BO_ 2566848798 BMS_VMU_STATUS: 4 Vector__XXX
     SG_ ChargePhase : 28|4@1+ (1,0) [0|7] "" Vector__XXX
     SG_ IsThermalForcing : 25|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsCooling : 24|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsPumping : 23|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsHeating : 22|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsDcContactorClosed : 21|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsEndOfCharge : 20|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsBalancing : 19|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsAlert : 18|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsWarning : 17|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ IsFailure : 16|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Soc : 8|8@1+ (1,0) [0|100] "%" Vector__XXX
     SG_ Mode : 0|3@1+ (1,0) [0|7] "" Vector__XXX
    """

    MESSAGE_ID = 2566848798

    NUM_BYTES = 4
    MODE_ERROR = 3
    MODE_DRIVE = 2
    MODE_CHARGE = 1
    MODE_STANDBY = 0

    """
    Charge phase indication:
- 0 : Not charging
- 1 : Preconditioning
- 2 : Standard Charge
- 3 : Wait Balancing
- 4 : Balancing
- 5 : Complementary Charge
- 6 : Charge Ended
"""
    charge_phase: int

    is_thermal_forcing: bool
    is_cooling: bool
    is_pumping: bool
    is_heating: bool
    is_dc_contactor_closed: bool
    is_end_of_charge: bool
    is_balancing: bool
    is_alert: bool
    is_warning: bool
    is_failure: bool
    soc: int
    mode: int


def decode_bms_vmu_status(data: bytes) -> BmsVmuStatus:
    assert len(data) == BmsVmuStatus.NUM_BYTES
    # SG_ ChargePhase : 28|4@1+ (1,0) [0|7] "" Vector__XXX
    charge_phase = (data[3] >> 4) & 0x0F
    # SG_ IsThermalForcing : 25|1@1- (1,0) [0|1] "" Vector__XXX
    is_thermal_forcing = (data[3] >> 1) & 0x01
    # SG_ IsCooling : 24|1@1- (1,0) [0|1] "" Vector__XXX
    is_cooling = data[3] & 0x01
    # SG_ IsPumping : 23|1@1- (1,0) [0|1] "" Vector__XXX
    is_pumping = (data[2] >> 7) & 0x01
    # SG_ IsHeating : 22|1@1- (1,0) [0|1] "" Vector__XXX
    is_heating = (data[2] >> 6) & 0x01
    # SG_ IsDcContactorClosed : 21|1@1- (1,0) [0|1] "" Vector__XXX
    is_dc_contactor_closed = (data[2] >> 5) & 0x01
    # SG_ IsEndOfCharge : 20|1@1- (1,0) [0|1] "" Vector__XXX
    is_end_of_charge = (data[2] >> 4) & 0x01
    # SG_ IsBalancing : 19|1@1- (1,0) [0|1] "" Vector__XXX
    is_balancing = (data[2] >> 3) & 0x01
    # SG_ IsAlert : 18|1@1- (1,0) [0|1] "" Vector__XXX
    is_alert = (data[2] >> 2) & 0x01
    # SG_ IsWarning : 17|1@1- (1,0) [0|1] "" Vector__XXX
    is_warning = (data[2] >> 1) & 0x01
    # SG_ IsFailure : 16|1@1- (1,0) [0|1] "" Vector__XXX
    is_failure = data[2] & 0x01
    # SG_ Soc : 8|8@1+ (1,0) [0|100] "%" Vector__XXX
    soc = data[1]
    # SG_ Mode : 0|3@1+ (1,0) [0|7] "" Vector__XXX
    mode = data[0] & 0x07
    return BmsVmuStatus(
        charge_phase=charge_phase,
        is_thermal_forcing=bool(is_thermal_forcing),
        is_cooling=bool(is_cooling),
        is_pumping=bool(is_pumping),
        is_heating=bool(is_heating),
        is_dc_contactor_closed=bool(is_dc_contactor_closed),
        is_end_of_charge=bool(is_end_of_charge),
        is_balancing=bool(is_balancing),
        is_alert=bool(is_alert),
        is_warning=bool(is_warning),
        is_failure=bool(is_failure),
        soc=soc,
        mode=mode,
    )


def encode_bms_vmu_status(msg: BmsVmuStatus) -> bytes:
    data = bytearray(BmsVmuStatus.NUM_BYTES)
    # SG_ Mode : 0|3@1+ (1,0) [0|7] "" Vector__XXX
    data[0] = msg.mode & 0x07
    # SG_ Soc : 8|8@1+ (1,0) [0|100] "%" Vector__XXX
    data[1] = msg.soc & 0xFF
    # SG_ IsFailure : 16|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsWarning : 17|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsAlert : 18|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsBalancing : 19|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsEndOfCharge : 20|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsDcContactorClosed : 21|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsHeating : 22|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsPumping : 23|1@1- (1,0) [0|1] "" Vector__XXX
    data[2] = (
        ((int(msg.is_pumping) & 0x01) << 7)
        | ((int(msg.is_heating) & 0x01) << 6)
        | ((int(msg.is_dc_contactor_closed) & 0x01) << 5)
        | ((int(msg.is_end_of_charge) & 0x01) << 4)
        | ((int(msg.is_balancing) & 0x01) << 3)
        | ((int(msg.is_alert) & 0x01) << 2)
        | ((int(msg.is_warning) & 0x01) << 1)
        | (int(msg.is_failure) & 0x01)
    )
    # SG_ ChargePhase : 28|4@1+ (1,0) [0|7] "" Vector__XXX
    # SG_ IsThermalForcing : 25|1@1- (1,0) [0|1] "" Vector__XXX
    # SG_ IsCooling : 24|1@1- (1,0) [0|1] "" Vector__XXX
    data[3] = (
        ((msg.charge_phase & 0x0F) << 4)
        | ((int(msg.is_thermal_forcing) & 0x01) << 1)
        | (int(msg.is_cooling) & 0x01)
    )
    return data
