import struct
import json

def bin_to_json(data_bin):

    unpacked = struct.unpack('<hQfffI', data_bin)

    id_sensor = unpacked[0]
    timestamp = unpacked[1]
    temperatura = unpacked[2]
    presion = unpacked[3]
    humedad = unpacked[4]
    checksum = unpacked[5]

    datos = {
        "id": id_sensor,
        "timestamp": timestamp,
        "temperatura": temperatura,
        "presion": presion,
        "humedad": humedad,
        "checksum": checksum
    }

    data_json = json.dumps(datos)

    return data_json