MESSAGE_ID_BMS_VMU_FAILURE = 2566852638

from dataclasses import dataclass

@dataclass
class BmsVmuFailure:
    """
    BO_ 2566852638 BMS_VMU_FAILURE: 8 Vector__XXX
     SG_ Safety_Reserved : 61|3@1+ (1,0) [0|0] "" Vector__XXX
     SG_ Safety_ApplComm : 60|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_JunctionBoxTemperature : 59|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_ContextAlim : 58|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Vpack : 57|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_CurrSensor : 56|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_TempSensor : 55|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_VoltSensor : 54|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Hvil : 53|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_EmergencyStop : 52|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_CommAuxShunt : 51|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveMaxim : 50|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveMeasTimeout : 49|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveId : 48|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveNumber : 47|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveComm : 46|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_SlaveSpiComm : 45|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Config : 44|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Contactor : 43|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Oil : 42|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Curmax60s : 41|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Curmax30s : 40|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Curmax10s : 39|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Curmax5s : 38|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Curmax2s : 37|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_VoltImbalance : 36|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Voltmin : 35|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Voltmax : 34|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_TempImbalance : 33|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_TempmaxMod : 32|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Reserved : 11|21@1+ (1,0) [0|0] "" Vector__XXX
     SG_ CurmaxFuse : 10|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Charger : 9|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ InternalTemperature : 8|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ InternalPowerAlimentation : 7|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ PrechargeContactor : 6|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Contactor : 5|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Config : 4|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ AuxShunt : 3|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ uCCommunication : 2|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ ExternalCommunication : 1|1@1- (1,0) [0|1] "" Vector__XXX
     SG_ Safety_Generic : 0|1@1- (1,0) [0|1] "" Vector__XXX
    """
    NUM_BYTES = 8
    safety_reserved: int
    safety_appl_comm: bool
    safety_junction_box_temperature: bool
    safety_context_alim: bool
    safety_vpack: bool
    safety_curr_sensor: bool
    safety_temp_sensor: bool
    safety_volt_sensor: bool
    safety_hvil: bool
    safety_emergency_stop: bool
    safety_comm_aux_shunt: bool
    safety_slave_maxim: bool
    safety_slave_meas_timeout: bool
    safety_slave_id: bool
    safety_slave_number: bool
    safety_slave_comm: bool
    safety_slave_spi_comm: bool
    safety_config: bool
    safety_contactor: bool
    safety_oil: bool
    safety_curmax60s: bool
    safety_curmax30s: bool
    safety_curmax10s: bool
    safety_curmax5s: bool
    safety_curmax2s: bool
    safety_volt_imbalance: bool
    safety_voltmin: bool
    safety_voltmax: bool
    safety_temp_imbalance: bool
    safety_tempmax_mod: bool
    reserved: int
    curmax_fuse: bool
    charger: bool
    internal_temperature: bool
    internal_power_alimentation: bool
    precharge_contactor: bool
    contactor: bool
    config: bool
    aux_shunt: bool
    uc_communication: bool
    external_communication: bool
    safety_generic: bool

def decode_bms_vmu_failure(data: bytes) -> BmsVmuFailure:
    assert len(data) == BmsVmuFailure.NUM_BYTES

    # SG_ Safety_Reserved : 61|3@1+ (1,0) [0|0] "" Vector__XXX
    safety_reserved = (int.from_bytes(data, 'big') >> 61) & 0x07

    # SG_ Safety_ApplComm : 60|1@1- (1,0) [0|1] "" Vector__XXX
    safety_appl_comm = (int.from_bytes(data, 'big') >> 60) & 0x01

    # SG_ Safety_JunctionBoxTemperature : 59|1@1- (1,0) [0|1] "" Vector__XXX
    safety_junction_box_temperature = (int.from_bytes(data, 'big') >> 59) & 0x01

    # SG_ Safety_ContextAlim : 58|1@1- (1,0) [0|1] "" Vector__XXX
    safety_context_alim = (int.from_bytes(data, 'big') >> 58) & 0x01

    # SG_ Safety_Vpack : 57|1@1- (1,0) [0|1] "" Vector__XXX
    safety_vpack = (int.from_bytes(data, 'big') >> 57) & 0x01

    # SG_ Safety_CurrSensor : 56|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curr_sensor = (int.from_bytes(data, 'big') >> 56) & 0x01

    # SG_ Safety_TempSensor : 55|1@1- (1,0) [0|1] "" Vector__XXX
    safety_temp_sensor = (int.from_bytes(data, 'big') >> 55) & 0x01

    # SG_ Safety_VoltSensor : 54|1@1- (1,0) [0|1] "" Vector__XXX
    safety_volt_sensor = (int.from_bytes(data, 'big') >> 54) & 0x01

    # SG_ Safety_Hvil : 53|1@1- (1,0) [0|1] "" Vector__XXX
    safety_hvil = (int.from_bytes(data, 'big') >> 53) & 0x01

    # SG_ Safety_EmergencyStop : 52|1@1- (1,0) [0|1] "" Vector__XXX
    safety_emergency_stop = (int.from_bytes(data, 'big') >> 52) & 0x01

    # SG_ Safety_CommAuxShunt : 51|1@1- (1,0) [0|1] "" Vector__XXX
    safety_comm_aux_shunt = (int.from_bytes(data, 'big') >> 51) & 0x01

    # SG_ Safety_SlaveMaxim : 50|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_maxim = (int.from_bytes(data, 'big') >> 50) & 0x01

    # SG_ Safety_SlaveMeasTimeout : 49|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_meas_timeout = (int.from_bytes(data, 'big') >> 49) & 0x01

    # SG_ Safety_SlaveId : 48|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_id = (int.from_bytes(data, 'big') >> 48) & 0x01

    # SG_ Safety_SlaveNumber : 47|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_number = (int.from_bytes(data, 'big') >> 47) & 0x01

    # SG_ Safety_SlaveComm : 46|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_comm = (int.from_bytes(data, 'big') >> 46) & 0x01

    # SG_ Safety_SlaveSpiComm : 45|1@1- (1,0) [0|1] "" Vector__XXX
    safety_slave_spi_comm = (int.from_bytes(data, 'big') >> 45) & 0x01

    # SG_ Safety_Config : 44|1@1- (1,0) [0|1] "" Vector__XXX
    safety_config = (int.from_bytes(data, 'big') >> 44) & 0x01

    # SG_ Safety_Contactor : 43|1@1- (1,0) [0|1] "" Vector__XXX
    safety_contactor = (int.from_bytes(data, 'big') >> 43) & 0x01

    # SG_ Safety_Oil : 42|1@1- (1,0) [0|1] "" Vector__XXX
    safety_oil = (int.from_bytes(data, 'big') >> 42) & 0x01

    # SG_ Safety_Curmax60s : 41|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curmax60s = (int.from_bytes(data, 'big') >> 41) & 0x01

    # SG_ Safety_Curmax30s : 40|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curmax30s = (int.from_bytes(data, 'big') >> 40) & 0x01

    # SG_ Safety_Curmax10s : 39|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curmax10s = (int.from_bytes(data, 'big') >> 39) & 0x01

    # SG_ Safety_Curmax5s : 38|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curmax5s = (int.from_bytes(data, 'big') >> 38) & 0x01

    # SG_ Safety_Curmax2s : 37|1@1- (1,0) [0|1] "" Vector__XXX
    safety_curmax2s = (int.from_bytes(data, 'big') >> 37) & 0x01

    # SG_ Safety_VoltImbalance : 36|1@1- (1,0) [0|1] "" Vector__XXX
    safety_volt_imbalance = (int.from_bytes(data, 'big') >> 36) & 0x01

    # SG_ Safety_Voltmin : 35|1@1- (1,0) [0|1] "" Vector__XXX
    safety_voltmin = (int.from_bytes(data, 'big') >> 35) & 0x01

    # SG_ Safety_Voltmax : 34|1@1- (1,0) [0|1] "" Vector__XXX
    safety_voltmax = (int.from_bytes(data, 'big') >> 34) & 0x01

    # SG_ Safety_TempImbalance : 33|1@1- (1,0) [0|1] "" Vector__XXX
    safety_temp_imbalance = (int.from_bytes(data, 'big') >> 33) & 0x01

    # SG_ Safety_TempmaxMod : 32|1@1- (1,0) [0|1] "" Vector__XXX
    safety_tempmax_mod = (int.from_bytes(data, 'big') >> 32) & 0x01

    # SG_ Reserved : 11|21@1+ (1,0) [0|0] "" Vector__XXX
    reserved = (int.from_bytes(data, 'big') >> 11) & 0x1FFFFF

    # SG_ CurmaxFuse : 10|1@1- (1,0) [0|1] "" Vector__XXX
    curmax_fuse = (int.from_bytes(data, 'big') >> 10) & 0x01

    # SG_ Charger : 9|1@1- (1,0) [0|1] "" Vector__XXX
    charger = (int.from_bytes(data, 'big') >> 9) & 0x01

    # SG_ InternalTemperature : 8|1@1- (1,0) [0|1] "" Vector__XXX
    internal_temperature = (int.from_bytes(data, 'big') >> 8) & 0x01

    # SG_ InternalPowerAlimentation : 7|1@1- (1,0) [0|1] "" Vector__XXX
    internal_power_alimentation = (int.from_bytes(data, 'big') >> 7) & 0x01

    # SG_ PrechargeContactor : 6|1@1- (1,0) [0|1] "" Vector__XXX
    precharge_contactor = (int.from_bytes(data, 'big') >> 6) & 0x01

    # SG_ Contactor : 5|1@1- (1,0) [0|1] "" Vector__XXX
    contactor = (int.from_bytes(data, 'big') >> 5) & 0x01

    # SG_ Config : 4|1@1- (1,0) [0|1] "" Vector__XXX
    config = (int.from_bytes(data, 'big') >> 4) & 0x01

    # SG_ AuxShunt : 3|1@1- (1,0) [0|1] "" Vector__XXX
    aux_shunt = (int.from_bytes(data, 'big') >> 3) & 0x01

    # SG_ uCCommunication : 2|1@1- (1,0) [0|1] "" Vector__XXX
    uc_communication = (int.from_bytes(data, 'big') >> 2) & 0x01

    # SG_ ExternalCommunication : 1|1@1- (1,0) [0|1] "" Vector__XXX
    external_communication = (int.from_bytes(data, 'big') >> 1) & 0x01

    # SG_ Safety_Generic : 0|1@1- (1,0) [0|1] "" Vector__XXX
    safety_generic = (int.from_bytes(data, 'big') >> 0) & 0x01

    return BmsVmuFailure(
        safety_reserved=safety_reserved,
        safety_appl_comm=bool(safety_appl_comm),
        safety_junction_box_temperature=bool(safety_junction_box_temperature),
        safety_context_alim=bool(safety_context_alim),
        safety_vpack=bool(safety_vpack),
        safety_curr_sensor=bool(safety_curr_sensor),
        safety_temp_sensor=bool(safety_temp_sensor),
        safety_volt_sensor=bool(safety_volt_sensor),
        safety_hvil=bool(safety_hvil),
        safety_emergency_stop=bool(safety_emergency_stop),
        safety_comm_aux_shunt=bool(safety_comm_aux_shunt),
        safety_slave_maxim=bool(safety_slave_maxim),
        safety_slave_meas_timeout=bool(safety_slave_meas_timeout),
        safety_slave_id=bool(safety_slave_id),
        safety_slave_number=bool(safety_slave_number),
        safety_slave_comm=bool(safety_slave_comm),
        safety_slave_spi_comm=bool(safety_slave_spi_comm),
        safety_config=bool(safety_config),
        safety_contactor=bool(safety_contactor),
        safety_oil=bool(safety_oil),
        safety_curmax60s=bool(safety_curmax60s),
        safety_curmax30s=bool(safety_curmax30s),
        safety_curmax10s=bool(safety_curmax10s),
        safety_curmax5s=bool(safety_curmax5s),
        safety_curmax2s=bool(safety_curmax2s),
        safety_volt_imbalance=bool(safety_volt_imbalance),
        safety_voltmin=bool(safety_voltmin),
        safety_voltmax=bool(safety_voltmax),
        safety_temp_imbalance=bool(safety_temp_imbalance),
        safety_tempmax_mod=bool(safety_tempmax_mod),
        reserved=reserved,
        curmax_fuse=bool(curmax_fuse),
        charger=bool(charger),
        internal_temperature=bool(internal_temperature),
        internal_power_alimentation=bool(internal_power_alimentation),
        precharge_contactor=bool(precharge_contactor),
        contactor=bool(contactor),
        config=bool(config),
        aux_shunt=bool(aux_shunt),
        uc_communication=bool(uc_communication),
        external_communication=bool(external_communication),
        safety_generic=bool(safety_generic),
    )

def encode_bms_vmu_failure(msg: BmsVmuFailure) -> bytes:
    value = 0
    # SG_ Safety_Reserved : 61|3@1+ (1,0) [0|0] "" Vector__XXX
    value |= (msg.safety_reserved & 0x07) << 61
    # SG_ Safety_ApplComm : 60|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_appl_comm) & 0x01) << 60
    # SG_ Safety_JunctionBoxTemperature : 59|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_junction_box_temperature) & 0x01) << 59
    # SG_ Safety_ContextAlim : 58|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_context_alim) & 0x01) << 58
    # SG_ Safety_Vpack : 57|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_vpack) & 0x01) << 57
    # SG_ Safety_CurrSensor : 56|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curr_sensor) & 0x01) << 56
    # SG_ Safety_TempSensor : 55|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_temp_sensor) & 0x01) << 55
    # SG_ Safety_VoltSensor : 54|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_volt_sensor) & 0x01) << 54
    # SG_ Safety_Hvil : 53|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_hvil) & 0x01) << 53
    # SG_ Safety_EmergencyStop : 52|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_emergency_stop) & 0x01) << 52
    # SG_ Safety_CommAuxShunt : 51|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_comm_aux_shunt) & 0x01) << 51
    # SG_ Safety_SlaveMaxim : 50|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_maxim) & 0x01) << 50
    # SG_ Safety_SlaveMeasTimeout : 49|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_meas_timeout) & 0x01) << 49
    # SG_ Safety_SlaveId : 48|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_id) & 0x01) << 48
    # SG_ Safety_SlaveNumber : 47|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_number) & 0x01) << 47
    # SG_ Safety_SlaveComm : 46|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_comm) & 0x01) << 46
    # SG_ Safety_SlaveSpiComm : 45|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_slave_spi_comm) & 0x01) << 45
    # SG_ Safety_Config : 44|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_config) & 0x01) << 44
    # SG_ Safety_Contactor : 43|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_contactor) & 0x01) << 43
    # SG_ Safety_Oil : 42|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_oil) & 0x01) << 42
    # SG_ Safety_Curmax60s : 41|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curmax60s) & 0x01) << 41
    # SG_ Safety_Curmax30s : 40|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curmax30s) & 0x01) << 40
    # SG_ Safety_Curmax10s : 39|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curmax10s) & 0x01) << 39
    # SG_ Safety_Curmax5s : 38|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curmax5s) & 0x01) << 38
    # SG_ Safety_Curmax2s : 37|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_curmax2s) & 0x01) << 37
    # SG_ Safety_VoltImbalance : 36|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_volt_imbalance) & 0x01) << 36
    # SG_ Safety_Voltmin : 35|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_voltmin) & 0x01) << 35
    # SG_ Safety_Voltmax : 34|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_voltmax) & 0x01) << 34
    # SG_ Safety_TempImbalance : 33|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_temp_imbalance) & 0x01) << 33
    # SG_ Safety_TempmaxMod : 32|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_tempmax_mod) & 0x01) << 32
    # SG_ Reserved : 11|21@1+ (1,0) [0|0] "" Vector__XXX
    value |= (msg.reserved & 0x1FFFFF) << 11
    # SG_ CurmaxFuse : 10|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.curmax_fuse) & 0x01) << 10
    # SG_ Charger : 9|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.charger) & 0x01) << 9
    # SG_ InternalTemperature : 8|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.internal_temperature) & 0x01) << 8
    # SG_ InternalPowerAlimentation : 7|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.internal_power_alimentation) & 0x01) << 7
    # SG_ PrechargeContactor : 6|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.precharge_contactor) & 0x01) << 6
    # SG_ Contactor : 5|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.contactor) & 0x01) << 5
    # SG_ Config : 4|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.config) & 0x01) << 4
    # SG_ AuxShunt : 3|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.aux_shunt) & 0x01) << 3
    # SG_ uCCommunication : 2|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.uc_communication) & 0x01) << 2
    # SG_ ExternalCommunication : 1|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.external_communication) & 0x01) << 1
    # SG_ Safety_Generic : 0|1@1- (1,0) [0|1] "" Vector__XXX
    value |= (int(msg.safety_generic) & 0x01) << 0

    return value.to_bytes(BmsVmuFailure.NUM_BYTES, 'big')
