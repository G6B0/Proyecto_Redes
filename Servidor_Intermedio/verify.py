import struct
from config import EXPECTED_SIZE

def verify_data(data_bin):

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

    #Calcular checksum igual que el emisor
    calculated = (
    id_sensor +
    (timestamp & 0xFFFFFFFF) +
    int(temperatura * 100) +
    int(presion * 100) +
    int(humedad * 100)
    ) & 0xFFFFFFFF

    
    return calculated == checksum