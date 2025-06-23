from dataclasses import dataclass

# -------------------- 2S --------------------


@dataclass
class BmsVmuSpDetail2s:
    """
    BO_ 2566849566 BMS_VMU_SP_DETAIL_2S: 8 Vector__XXX
     SG_ DischargeAlertThreshold2s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent2s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold2s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent2s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566849566
    NUM_BYTES = 8
    discharge_alert_threshold_2s: float
    discharge_measured_current_2s: float
    charge_alert_threshold_2s: float
    charge_measured_current_2s: float


def decode_sp_detail_2s(data: bytes) -> BmsVmuSpDetail2s:
    assert len(data) == BmsVmuSpDetail2s.NUM_BYTES
    # SG_ DischargeAlertThreshold2s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    discharge_alert_threshold_2s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ DischargeMeasuredCurrent2s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    discharge_measured_current_2s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ ChargeAlertThreshold2s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    charge_alert_threshold_2s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ ChargeMeasuredCurrent2s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    charge_measured_current_2s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetail2s(
        discharge_alert_threshold_2s=discharge_alert_threshold_2s,
        discharge_measured_current_2s=discharge_measured_current_2s,
        charge_alert_threshold_2s=charge_alert_threshold_2s,
        charge_measured_current_2s=charge_measured_current_2s,
    )


def encode_sp_detail_2s(msg: BmsVmuSpDetail2s) -> bytes:
    data = bytearray(BmsVmuSpDetail2s.NUM_BYTES)
    # SG_ ChargeMeasuredCurrent2s : 0|16@1+ (0.1,0)
    val = int(round(msg.charge_measured_current_2s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ ChargeAlertThreshold2s : 16|16@1+ (0.1,0)
    val = int(round(msg.charge_alert_threshold_2s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ DischargeMeasuredCurrent2s : 32|16@1+ (0.1,0)
    val = int(round(msg.discharge_measured_current_2s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ DischargeAlertThreshold2s : 48|16@1+ (0.1,0)
    val = int(round(msg.discharge_alert_threshold_2s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data


# -------------------- 5S --------------------


@dataclass
class BmsVmuSpDetail5s:
    """
    BO_ 2566849822 BMS_VMU_SP_DETAIL_5S: 8 Vector__XXX
     SG_ DischargeAlertThreshold5s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent5s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold5s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent5s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566849822
    NUM_BYTES = 8
    discharge_alert_threshold_5s: float
    discharge_measured_current_5s: float
    charge_alert_threshold_5s: float
    charge_measured_current_5s: float


def decode_sp_detail_5s(data: bytes) -> BmsVmuSpDetail5s:
    assert len(data) == BmsVmuSpDetail5s.NUM_BYTES
    # SG_ DischargeAlertThreshold5s : 48|16@1+ (0.1,0)
    discharge_alert_threshold_5s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ DischargeMeasuredCurrent5s : 32|16@1+ (0.1,0)
    discharge_measured_current_5s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ ChargeAlertThreshold5s : 16|16@1+ (0.1,0)
    charge_alert_threshold_5s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ ChargeMeasuredCurrent5s : 0|16@1+ (0.1,0)
    charge_measured_current_5s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetail5s(
        discharge_alert_threshold_5s=discharge_alert_threshold_5s,
        discharge_measured_current_5s=discharge_measured_current_5s,
        charge_alert_threshold_5s=charge_alert_threshold_5s,
        charge_measured_current_5s=charge_measured_current_5s,
    )


def encode_sp_detail_5s(msg: BmsVmuSpDetail5s) -> bytes:
    data = bytearray(BmsVmuSpDetail5s.NUM_BYTES)
    # SG_ ChargeMeasuredCurrent5s : 0|16@1+ (0.1,0)
    val = int(round(msg.charge_measured_current_5s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ ChargeAlertThreshold5s : 16|16@1+ (0.1,0)
    val = int(round(msg.charge_alert_threshold_5s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ DischargeMeasuredCurrent5s : 32|16@1+ (0.1,0)
    val = int(round(msg.discharge_measured_current_5s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ DischargeAlertThreshold5s : 48|16@1+ (0.1,0)
    val = int(round(msg.discharge_alert_threshold_5s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data


# -------------------- 10S --------------------


@dataclass
class BmsVmuSpDetail10s:
    """
    BO_ 2566850078 BMS_VMU_SP_DETAIL_10S: 8 Vector__XXX
     SG_ DischargeAlertThreshold10s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent10s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold10s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent10s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566850078
    NUM_BYTES = 8
    discharge_alert_threshold_10s: float
    discharge_measured_current_10s: float
    charge_alert_threshold_10s: float
    charge_measured_current_10s: float


def decode_sp_detail_10s(data: bytes) -> BmsVmuSpDetail10s:
    assert len(data) == BmsVmuSpDetail10s.NUM_BYTES
    # SG_ DischargeAlertThreshold10s : 48|16@1+ (0.1,0)
    discharge_alert_threshold_10s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ DischargeMeasuredCurrent10s : 32|16@1+ (0.1,0)
    discharge_measured_current_10s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ ChargeAlertThreshold10s : 16|16@1+ (0.1,0)
    charge_alert_threshold_10s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ ChargeMeasuredCurrent10s : 0|16@1+ (0.1,0)
    charge_measured_current_10s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetail10s(
        discharge_alert_threshold_10s=discharge_alert_threshold_10s,
        discharge_measured_current_10s=discharge_measured_current_10s,
        charge_alert_threshold_10s=charge_alert_threshold_10s,
        charge_measured_current_10s=charge_measured_current_10s,
    )


def encode_sp_detail_10s(msg: BmsVmuSpDetail10s) -> bytes:
    data = bytearray(BmsVmuSpDetail10s.NUM_BYTES)
    # SG_ ChargeMeasuredCurrent10s : 0|16@1+ (0.1,0)
    val = int(round(msg.charge_measured_current_10s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ ChargeAlertThreshold10s : 16|16@1+ (0.1,0)
    val = int(round(msg.charge_alert_threshold_10s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ DischargeMeasuredCurrent10s : 32|16@1+ (0.1,0)
    val = int(round(msg.discharge_measured_current_10s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ DischargeAlertThreshold10s : 48|16@1+ (0.1,0)
    val = int(round(msg.discharge_alert_threshold_10s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data


# -------------------- 30S --------------------


@dataclass
class BmsVmuSpDetail30s:
    """
    BO_ 2566850334 BMS_VMU_SP_DETAIL_30S: 8 Vector__XXX
     SG_ DischargeAlertThreshold30s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent30s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold30s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent30s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566850334
    NUM_BYTES = 8
    discharge_alert_threshold_30s: float
    discharge_measured_current_30s: float
    charge_alert_threshold_30s: float
    charge_measured_current_30s: float


def decode_sp_detail_30s(data: bytes) -> BmsVmuSpDetail30s:
    assert len(data) == BmsVmuSpDetail30s.NUM_BYTES
    # SG_ DischargeAlertThreshold30s : 48|16@1+ (0.1,0)
    discharge_alert_threshold_30s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ DischargeMeasuredCurrent30s : 32|16@1+ (0.1,0)
    discharge_measured_current_30s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ ChargeAlertThreshold30s : 16|16@1+ (0.1,0)
    charge_alert_threshold_30s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ ChargeMeasuredCurrent30s : 0|16@1+ (0.1,0)
    charge_measured_current_30s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetail30s(
        discharge_alert_threshold_30s=discharge_alert_threshold_30s,
        discharge_measured_current_30s=discharge_measured_current_30s,
        charge_alert_threshold_30s=charge_alert_threshold_30s,
        charge_measured_current_30s=charge_measured_current_30s,
    )


def encode_sp_detail_30s(msg: BmsVmuSpDetail30s) -> bytes:
    data = bytearray(BmsVmuSpDetail30s.NUM_BYTES)
    # SG_ ChargeMeasuredCurrent30s : 0|16@1+ (0.1,0)
    val = int(round(msg.charge_measured_current_30s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ ChargeAlertThreshold30s : 16|16@1+ (0.1,0)
    val = int(round(msg.charge_alert_threshold_30s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ DischargeMeasuredCurrent30s : 32|16@1+ (0.1,0)
    val = int(round(msg.discharge_measured_current_30s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ DischargeAlertThreshold30s : 48|16@1+ (0.1,0)
    val = int(round(msg.discharge_alert_threshold_30s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data


# -------------------- 60S --------------------


@dataclass
class BmsVmuSpDetail60s:
    """
    BO_ 2566850590 BMS_VMU_SP_DETAIL_60S: 8 Vector__XXX
     SG_ DischargeAlertThreshold60s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent60s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold60s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent60s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """

    MESSAGE_ID = 2566850590
    NUM_BYTES = 8
    discharge_alert_threshold_60s: float
    discharge_measured_current_60s: float
    charge_alert_threshold_60s: float
    charge_measured_current_60s: float


def decode_sp_detail_60s(data: bytes) -> BmsVmuSpDetail60s:
    assert len(data) == BmsVmuSpDetail60s.NUM_BYTES
    # SG_ DischargeAlertThreshold60s : 48|16@1+ (0.1,0)
    discharge_alert_threshold_60s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ DischargeMeasuredCurrent60s : 32|16@1+ (0.1,0)
    discharge_measured_current_60s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ ChargeAlertThreshold60s : 16|16@1+ (0.1,0)
    charge_alert_threshold_60s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ ChargeMeasuredCurrent60s : 0|16@1+ (0.1,0)
    charge_measured_current_60s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetail60s(
        discharge_alert_threshold_60s=discharge_alert_threshold_60s,
        discharge_measured_current_60s=discharge_measured_current_60s,
        charge_alert_threshold_60s=charge_alert_threshold_60s,
        charge_measured_current_60s=charge_measured_current_60s,
    )


def encode_sp_detail_60s(msg: BmsVmuSpDetail60s) -> bytes:
    data = bytearray(BmsVmuSpDetail60s.NUM_BYTES)
    # SG_ ChargeMeasuredCurrent60s : 0|16@1+ (0.1,0)
    val = int(round(msg.charge_measured_current_60s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ ChargeAlertThreshold60s : 16|16@1+ (0.1,0)
    val = int(round(msg.charge_alert_threshold_60s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ DischargeMeasuredCurrent60s : 32|16@1+ (0.1,0)
    val = int(round(msg.discharge_measured_current_60s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ DischargeAlertThreshold60s : 48|16@1+ (0.1,0)
    val = int(round(msg.discharge_alert_threshold_60s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data
