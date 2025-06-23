from dataclasses import dataclass


@dataclass
class VmuBmsGenDataRecord1:
    """
    BO_ 2180980736 VMU_BMS_GEN_DATA_RECORD_1: 8 Vector__XXX
     SG_ GenRecordValue2 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
     SG_ GenRecordValue1 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    """

    # VMU_BMS_GEN_DATA_RECORD_1
    MESSAGE_ID_GEN_DATA_RECORD_1 = 2180980736
    NUM_BYTES = 8
    gen_record_value1: int
    gen_record_value2: int


def decode_gen_data_record_1(data: bytes) -> VmuBmsGenDataRecord1:
    assert len(data) == VmuBmsGenDataRecord1.NUM_BYTES
    # SG_ GenRecordValue2 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value2 = int.from_bytes(data[4:8], byteorder="big", signed=True)
    # SG_ GenRecordValue1 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value1 = int.from_bytes(data[0:4], byteorder="big", signed=True)
    return VmuBmsGenDataRecord1(
        gen_record_value1=gen_record_value1,
        gen_record_value2=gen_record_value2,
    )


def encode_gen_data_record_1(msg: VmuBmsGenDataRecord1) -> bytes:
    data = bytearray(VmuBmsGenDataRecord1.NUM_BYTES)
    # SG_ GenRecordValue1 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[0:4] = msg.gen_record_value1.to_bytes(4, byteorder="big", signed=True)
    # SG_ GenRecordValue2 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[4:8] = msg.gen_record_value2.to_bytes(4, byteorder="big", signed=True)
    return bytes(data)


@dataclass
class VmuBmsGenDataRecord2:
    """
    BO_ 2180980992 VMU_BMS_GEN_DATA_RECORD_2: 8 Vector__XXX
     SG_ GenRecordValue4 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
     SG_ GenRecordValue3 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    """

    # VMU_BMS_GEN_DATA_RECORD_2
    MESSAGE_ID_GEN_DATA_RECORD_2 = 2180980992
    NUM_BYTES = 8
    gen_record_value3: int
    gen_record_value4: int


def decode_gen_data_record_2(data: bytes) -> VmuBmsGenDataRecord2:
    assert len(data) == VmuBmsGenDataRecord2.NUM_BYTES
    # SG_ GenRecordValue4 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value4 = int.from_bytes(data[4:8], byteorder="big", signed=True)
    # SG_ GenRecordValue3 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value3 = int.from_bytes(data[0:4], byteorder="big", signed=True)
    return VmuBmsGenDataRecord2(
        gen_record_value3=gen_record_value3,
        gen_record_value4=gen_record_value4,
    )


def encode_gen_data_record_2(msg: VmuBmsGenDataRecord2) -> bytes:
    data = bytearray(VmuBmsGenDataRecord2.NUM_BYTES)
    # SG_ GenRecordValue3 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[0:4] = msg.gen_record_value3.to_bytes(4, byteorder="big", signed=True)
    # SG_ GenRecordValue4 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[4:8] = msg.gen_record_value4.to_bytes(4, byteorder="big", signed=True)
    return bytes(data)


@dataclass
class VmuBmsGenDataRecord3:
    """
    BO_ 2180981248 VMU_BMS_GEN_DATA_RECORD_3: 8 Vector__XXX
     SG_ GenRecordValue6 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
     SG_ GenRecordValue5 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    """

    # VMU_BMS_GEN_DATA_RECORD_3
    MESSAGE_ID_GEN_DATA_RECORD_3 = 2180981248
    NUM_BYTES = 8
    gen_record_value5: int
    gen_record_value6: int


def decode_gen_data_record_3(data: bytes) -> VmuBmsGenDataRecord3:
    assert len(data) == VmuBmsGenDataRecord3.NUM_BYTES
    # SG_ GenRecordValue6 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value6 = int.from_bytes(data[4:8], byteorder="big", signed=True)
    # SG_ GenRecordValue5 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    gen_record_value5 = int.from_bytes(data[0:4], byteorder="big", signed=True)
    return VmuBmsGenDataRecord3(
        gen_record_value5=gen_record_value5,
        gen_record_value6=gen_record_value6,
    )


def encode_gen_data_record_3(msg: VmuBmsGenDataRecord3) -> bytes:
    data = bytearray(VmuBmsGenDataRecord3.NUM_BYTES)
    # SG_ GenRecordValue5 : 0|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[0:4] = msg.gen_record_value5.to_bytes(4, byteorder="big", signed=True)
    # SG_ GenRecordValue6 : 32|32@1- (1,0) [2.14748e+009|-2.14748e+009] "" Vector__XXX
    data[4:8] = msg.gen_record_value6.to_bytes(4, byteorder="big", signed=True)
    return bytes(data)
