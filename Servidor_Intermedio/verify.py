import struct
from config import EXPECTED_SIZE

def verify_data(data_bin):

    if len(data_bin) != EXPECTED_SIZE:
        return False

    try:
        unpacked = struct.unpack('<hQfffI', data_bin)
    except struct.error as e:
        return False

    id_sensor = unpacked[0]
    timestamp = unpacked[1]
    temperatura = unpacked[2]
    presion = unpacked[3]
    humedad = unpacked[4]
    checksum = unpacked[5]

    data_without_checksum = data_bin[0:-4]
    checksum_calculation = sum(data_without_checksum)

    if checksum_calculation != checksum:
        return False
    
    return True