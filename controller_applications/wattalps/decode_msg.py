from .messages.msg_charge import BmsVmuSpCharge, decode_charge
from .messages.msg_conf import BmsVmuConfVersion, decode_conf_version
from .messages.msg_drive import BmsVmuSpDrive, decode_drive
from .messages.msg_force_cooling import VmuBmsForceCooling, decode_force_cooling
from .messages.msg_force_heating import VmuBmsForceHeating, decode_force_heating
from .messages.msg_force_pumping import VmuBmsForcePumping, decode_force_pumping
from .messages.msg_gen_data_record import (
    VmuBmsGenDataRecord3,
    decode_gen_data_record_3,
    VmuBmsGenDataRecord2,
    decode_gen_data_record_2,
    VmuBmsGenDataRecord1,
    decode_gen_data_record_1,
)
from .messages.msg_sp_detail import (
    BmsVmuSpDetail2s,
    BmsVmuSpDetail5s,
    BmsVmuSpDetail10s,
    BmsVmuSpDetail30s,
    BmsVmuSpDetail60s,
    decode_sp_detail_2s,
    decode_sp_detail_10s,
    decode_sp_detail_30s,
    decode_sp_detail_5s,
    decode_sp_detail_60s,
)
from .messages.msg_sp_detail_rms import (
    BmsVmuSpDetailRms1,
    BmsVmuSpDetailRms2,
    BmsVmuSpDetailRms3,
    BmsVmuSpDetailRms4,
    BmsVmuSpDetailRms5,
    decode_sp_detail_rms_1,
    decode_sp_detail_rms_2,
    decode_sp_detail_rms_3,
    decode_sp_detail_rms_4,
    decode_sp_detail_rms_5,
)
from .messages.msg_status import (
    BmsVmuStatus,
    VmuBmsStatus,
    decode_bms_vmu_status,
    decode_vmu_bms_status,
)
from .messages.msg_vmu_info import BmsVmuInfo, decode_info
from .messages.msg_vmu_info_cells import BmsVmuInfoCells, decode_info_cells
from .messages.msg_vmu_info_insulation import (
    BmsVmuInfoInsulation,
    decode_info_insulation,
)
from .messages.msg_vmu_info_jb_temp import (
    BmsVmuInfoJbTemperature,
    decode_info_jb_temperature,
)
from .messages.msg_vmu_info_temp import BmsVmuInfoTemperature, decode_info_temperature
from .messages.msg_vmu_stats import BmsVmuStats, decode_vmu_stats
from .messages.msg_warnings import BmsVmuFailure, decode_bms_vmu_failure


MESSAGE_DECODERS = {
    BmsVmuSpCharge.MESSAGE_ID: decode_charge,
    BmsVmuConfVersion.MESSAGE_ID: decode_conf_version,
    BmsVmuSpDrive.MESSAGE_ID: decode_drive,
    BmsVmuSpDetail2s.MESSAGE_ID: decode_sp_detail_2s,
    BmsVmuSpDetail5s.MESSAGE_ID: decode_sp_detail_5s,
    BmsVmuSpDetail10s.MESSAGE_ID: decode_sp_detail_10s,
    BmsVmuSpDetail30s.MESSAGE_ID: decode_sp_detail_30s,
    BmsVmuSpDetail60s.MESSAGE_ID: decode_sp_detail_60s,
    BmsVmuSpDetailRms1.MESSAGE_ID: decode_sp_detail_rms_1,
    BmsVmuSpDetailRms2.MESSAGE_ID: decode_sp_detail_rms_2,
    BmsVmuSpDetailRms3.MESSAGE_ID: decode_sp_detail_rms_3,
    BmsVmuSpDetailRms4.MESSAGE_ID: decode_sp_detail_rms_4,
    BmsVmuSpDetailRms5.MESSAGE_ID: decode_sp_detail_rms_5,
    BmsVmuStatus.MESSAGE_ID: decode_bms_vmu_status,
    VmuBmsStatus.MESSAGE_ID: decode_vmu_bms_status,
    BmsVmuInfo.MESSAGE_ID: decode_info,
    BmsVmuInfoCells.MESSAGE_ID: decode_info_cells,
    BmsVmuInfoInsulation.MESSAGE_ID: decode_info_insulation,
    BmsVmuInfoJbTemperature.MESSAGE_ID: decode_info_jb_temperature,
    BmsVmuInfoTemperature.MESSAGE_ID: decode_info_temperature,
    BmsVmuStats.MESSAGE_ID: decode_vmu_stats,
    BmsVmuFailure.MESSAGE_ID: decode_bms_vmu_failure,
}


def decode_message_from_id(message_id: int, data: bytes):
    decode_fnc = MESSAGE_DECODERS.get(message_id, None)
    if decode_fnc is not None:
        try:
            data = decode_fnc(data)
        except Exception as e:
            print(
                f"An error occured trying to decode message id {message_id} with data:\n{data}"
            )
            print(f"Error was{e}")
