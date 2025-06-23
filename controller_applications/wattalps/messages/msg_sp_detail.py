from dataclasses import dataclass

# -------------------- 2S --------------------
MESSAGE_ID_SP_DETAIL_2S = 2566849566

@dataclass
class BmsVmuSpDetail2s:
    """
    BO_ 2566849566 BMS_VMU_SP_DETAIL_2S: 8 Vector__XXX
     SG_ DischargeAlertThreshold2s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent2s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold2s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent2s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
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
MESSAGE_ID_SP_DETAIL_5S = 2566849822

@dataclass
class BmsVmuSpDetail5s:
    """
    BO_ 2566849822 BMS_VMU_SP_DETAIL_5S: 8 Vector__XXX
     SG_ DischargeAlertThreshold5s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent5s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold5s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent5s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
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
MESSAGE_ID_SP_DETAIL_10S = 2566850078

@dataclass
class BmsVmuSpDetail10s:
    """
    BO_ 2566850078 BMS_VMU_SP_DETAIL_10S: 8 Vector__XXX
     SG_ DischargeAlertThreshold10s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent10s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold10s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent10s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
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
MESSAGE_ID_SP_DETAIL_30S = 2566850334

@dataclass
class BmsVmuSpDetail30s:
    """
    BO_ 2566850334 BMS_VMU_SP_DETAIL_30S: 8 Vector__XXX
     SG_ DischargeAlertThreshold30s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent30s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold30s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent30s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
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
MESSAGE_ID_SP_DETAIL_60S = 2566850590

@dataclass
class BmsVmuSpDetail60s:
    """
    BO_ 2566850590 BMS_VMU_SP_DETAIL_60S: 8 Vector__XXX
     SG_ DischargeAlertThreshold60s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ DischargeMeasuredCurrent60s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeAlertThreshold60s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ ChargeMeasuredCurrent60s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
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

from dataclasses import dataclass

# -------------------- RMS_1 --------------------
MESSAGE_ID_SP_DETAIL_RMS_1 = 2566850846

@dataclass
class BmsVmuSpDetailRms1:
    """
    BO_ 2566850846 BMS_VMU_SP_DETAIL_RMS_1: 8 Vector__XXX
     SG_ RmsAlertThreshold5s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent5s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsAlertThreshold2s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent2s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
    NUM_BYTES = 8
    rms_alert_threshold_5s: float
    rms_measured_current_5s: float
    rms_alert_threshold_2s: float
    rms_measured_current_2s: float

def decode_sp_detail_rms_1(data: bytes) -> BmsVmuSpDetailRms1:
    assert len(data) == BmsVmuSpDetailRms1.NUM_BYTES
    # SG_ RmsAlertThreshold5s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_5s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ RmsMeasuredCurrent5s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_5s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ RmsAlertThreshold2s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_2s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ RmsMeasuredCurrent2s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_2s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetailRms1(
        rms_alert_threshold_5s=rms_alert_threshold_5s,
        rms_measured_current_5s=rms_measured_current_5s,
        rms_alert_threshold_2s=rms_alert_threshold_2s,
        rms_measured_current_2s=rms_measured_current_2s,
    )

def encode_sp_detail_rms_1(msg: BmsVmuSpDetailRms1) -> bytes:
    data = bytearray(BmsVmuSpDetailRms1.NUM_BYTES)
    # SG_ RmsMeasuredCurrent2s : 0|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_2s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ RmsAlertThreshold2s : 16|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_2s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ RmsMeasuredCurrent5s : 32|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_5s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ RmsAlertThreshold5s : 48|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_5s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data

# -------------------- RMS_2 --------------------
MESSAGE_ID_SP_DETAIL_RMS_2 = 2566851102

@dataclass
class BmsVmuSpDetailRms2:
    """
    BO_ 2566851102 BMS_VMU_SP_DETAIL_RMS_2: 8 Vector__XXX
     SG_ RmsAlertThreshold30s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent30s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsAlertThreshold10s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent10s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
    NUM_BYTES = 8
    rms_alert_threshold_30s: float
    rms_measured_current_30s: float
    rms_alert_threshold_10s: float
    rms_measured_current_10s: float

def decode_sp_detail_rms_2(data: bytes) -> BmsVmuSpDetailRms2:
    assert len(data) == BmsVmuSpDetailRms2.NUM_BYTES
    # SG_ RmsAlertThreshold30s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_30s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ RmsMeasuredCurrent30s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_30s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ RmsAlertThreshold10s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_10s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ RmsMeasuredCurrent10s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_10s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetailRms2(
        rms_alert_threshold_30s=rms_alert_threshold_30s,
        rms_measured_current_30s=rms_measured_current_30s,
        rms_alert_threshold_10s=rms_alert_threshold_10s,
        rms_measured_current_10s=rms_measured_current_10s,
    )

def encode_sp_detail_rms_2(msg: BmsVmuSpDetailRms2) -> bytes:
    data = bytearray(BmsVmuSpDetailRms2.NUM_BYTES)
    # SG_ RmsMeasuredCurrent10s : 0|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_10s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ RmsAlertThreshold10s : 16|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_10s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ RmsMeasuredCurrent30s : 32|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_30s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ RmsAlertThreshold30s : 48|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_30s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data

# -------------------- RMS_3 --------------------
MESSAGE_ID_SP_DETAIL_RMS_3 = 2566851358

@dataclass
class BmsVmuSpDetailRms3:
    """
    BO_ 2566851358 BMS_VMU_SP_DETAIL_RMS_3: 8 Vector__XXX
     SG_ RmsAlertThreshold120s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent120s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsAlertThreshold60s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent60s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
    NUM_BYTES = 8
    rms_alert_threshold_120s: float
    rms_measured_current_120s: float
    rms_alert_threshold_60s: float
    rms_measured_current_60s: float

def decode_sp_detail_rms_3(data: bytes) -> BmsVmuSpDetailRms3:
    assert len(data) == BmsVmuSpDetailRms3.NUM_BYTES
    # SG_ RmsAlertThreshold120s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_120s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ RmsMeasuredCurrent120s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_120s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ RmsAlertThreshold60s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_60s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ RmsMeasuredCurrent60s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_60s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetailRms3(
        rms_alert_threshold_120s=rms_alert_threshold_120s,
        rms_measured_current_120s=rms_measured_current_120s,
        rms_alert_threshold_60s=rms_alert_threshold_60s,
        rms_measured_current_60s=rms_measured_current_60s,
    )

def encode_sp_detail_rms_3(msg: BmsVmuSpDetailRms3) -> bytes:
    data = bytearray(BmsVmuSpDetailRms3.NUM_BYTES)
    # SG_ RmsMeasuredCurrent60s : 0|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_60s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ RmsAlertThreshold60s : 16|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_60s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ RmsMeasuredCurrent120s : 32|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_120s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ RmsAlertThreshold120s : 48|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_120s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data

# -------------------- RMS_4 --------------------
MESSAGE_ID_SP_DETAIL_RMS_4 = 2566851614

@dataclass
class BmsVmuSpDetailRms4:
    """
    BO_ 2566851614 BMS_VMU_SP_DETAIL_RMS_4: 8 Vector__XXX
     SG_ RmsAlertThreshold480s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent480s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsAlertThreshold240s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent240s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
    NUM_BYTES = 8
    rms_alert_threshold_480s: float
    rms_measured_current_480s: float
    rms_alert_threshold_240s: float
    rms_measured_current_240s: float

def decode_sp_detail_rms_4(data: bytes) -> BmsVmuSpDetailRms4:
    assert len(data) == BmsVmuSpDetailRms4.NUM_BYTES
    # SG_ RmsAlertThreshold480s : 48|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_480s = ((data[6] << 8) | data[7]) * 0.1
    # SG_ RmsMeasuredCurrent480s : 32|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_480s = ((data[4] << 8) | data[5]) * 0.1
    # SG_ RmsAlertThreshold240s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_240s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ RmsMeasuredCurrent240s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_240s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetailRms4(
        rms_alert_threshold_480s=rms_alert_threshold_480s,
        rms_measured_current_480s=rms_measured_current_480s,
        rms_alert_threshold_240s=rms_alert_threshold_240s,
        rms_measured_current_240s=rms_measured_current_240s,
    )

def encode_sp_detail_rms_4(msg: BmsVmuSpDetailRms4) -> bytes:
    data = bytearray(BmsVmuSpDetailRms4.NUM_BYTES)
    # SG_ RmsMeasuredCurrent240s : 0|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_240s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ RmsAlertThreshold240s : 16|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_240s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    # SG_ RmsMeasuredCurrent480s : 32|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_480s / 0.1))
    data[4] = (val >> 8) & 0xFF
    data[5] = val & 0xFF
    # SG_ RmsAlertThreshold480s : 48|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_480s / 0.1))
    data[6] = (val >> 8) & 0xFF
    data[7] = val & 0xFF
    return data

# -------------------- RMS_5 --------------------
MESSAGE_ID_SP_DETAIL_RMS_5 = 2566851870

@dataclass
class BmsVmuSpDetailRms5:
    """
    BO_ 2566851870 BMS_VMU_SP_DETAIL_RMS_5: 4 Vector__XXX
     SG_ RmsAlertThreshold900s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
     SG_ RmsMeasuredCurrent900s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    """
    NUM_BYTES = 4
    rms_alert_threshold_900s: float
    rms_measured_current_900s: float

def decode_sp_detail_rms_5(data: bytes) -> BmsVmuSpDetailRms5:
    assert len(data) == BmsVmuSpDetailRms5.NUM_BYTES
    # SG_ RmsAlertThreshold900s : 16|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_alert_threshold_900s = ((data[2] << 8) | data[3]) * 0.1
    # SG_ RmsMeasuredCurrent900s : 0|16@1+ (0.1,0) [0|6553.5] "A" Vector__XXX
    rms_measured_current_900s = ((data[0] << 8) | data[1]) * 0.1
    return BmsVmuSpDetailRms5(
        rms_alert_threshold_900s=rms_alert_threshold_900s,
        rms_measured_current_900s=rms_measured_current_900s,
    )

def encode_sp_detail_rms_5(msg: BmsVmuSpDetailRms5) -> bytes:
    data = bytearray(BmsVmuSpDetailRms5.NUM_BYTES)
    # SG_ RmsMeasuredCurrent900s : 0|16@1+ (0.1,0)
    val = int(round(msg.rms_measured_current_900s / 0.1))
    data[0] = (val >> 8) & 0xFF
    data[1] = val & 0xFF
    # SG_ RmsAlertThreshold900s : 16|16@1+ (0.1,0)
    val = int(round(msg.rms_alert_threshold_900s / 0.1))
    data[2] = (val >> 8) & 0xFF
    data[3] = val & 0xFF
    return data
