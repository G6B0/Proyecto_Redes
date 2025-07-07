import socket
import struct
from config import HOST, PORT, EXPECTED_SIZE

def decrypt_data(data, key=0xAB):
    """
    Descifra según la lógica del emisor:
    """
    if len(data) < 26:
        raise ValueError(f"Datos insuficientes para descifrar: {len(data)} < 26")
    
    real_data = data[:26]
    decrypted = bytearray(real_data)
    
    # Cifrar todo excepto los últimos 4 bytes (22-25)
    for i in range(22):  # Solo cifrar bytes 0-21
        decrypted[i] ^= key
    
    # Añadir los bytes extra (padding) sin modificar
    if len(data) > 26:
        decrypted.extend(data[26:])
    
    return bytes(decrypted)

def parse_sensor_data(data):
    """
    Deserializa los datos binarios a estructura SensorData
    Layout correcto: id, timestamp, temperatura, presion, humedad, checksum
    """
    if len(data) != EXPECTED_SIZE:
        raise ValueError(f"Tamaño de datos incorrecto: {len(data)} != {EXPECTED_SIZE}")
    
   
    
    try:
        # Según el layout real del compilador:
        # int16_t id (offset 0)
        id_sensor = struct.unpack('<h', data[0:2])[0]
        
        # uint64_t timestamp (offset 2)
        timestamp = struct.unpack('<Q', data[2:10])[0]
        
        # float temperatura (offset 10)
        temperatura = struct.unpack('<f', data[10:14])[0]
        
        # float presion (offset 14)
        presion = struct.unpack('<f', data[14:18])[0]
        
        # float humedad (offset 18)
        humedad = struct.unpack('<f', data[18:22])[0]
        
        # uint32_t checksum (offset 22)
        checksum = struct.unpack('<I', data[22:26])[0]
        
        return {
            'id': id_sensor,
            'timestamp': timestamp,
            'temperatura': temperatura,
            'presion': presion,
            'humedad': humedad,
            'checksum': checksum
        }
    except struct.error as e:
        raise ValueError(f"Error al deserializar datos: {e}")
    except IndexError as e:
        raise ValueError(f"Error de índice al deserializar: {e}")

def calculate_checksum(sensor_data):
    """
    Calcula el checksum exactamente como lo hace el emisor:
    suma simple de: id + timestamp + (temp*100) + (pres*100) + (hum*100)
    """
    checksum = 0
    
    # ID directo
    checksum += sensor_data['id']
    
    # Timestamp convertido a uint32_t (solo los primeros 32 bits)
    checksum += sensor_data['timestamp'] & 0xFFFFFFFF
    
    # Floats multiplicados por 100 y convertidos a uint32_t
    checksum += int(sensor_data['temperatura'] * 100) & 0xFFFFFFFF
    checksum += int(sensor_data['presion'] * 100) & 0xFFFFFFFF
    checksum += int(sensor_data['humedad'] * 100) & 0xFFFFFFFF
    
    return checksum & 0xFFFFFFFF

def process_single_message(data):
    """
    Procesa un solo mensaje del sensor
    """
    try:
        # 1. Descifrar los datos
        decrypted_data = decrypt_data(data)
        print(f"🔍 Bytes descifrados: {decrypted_data.hex()}")

        
        # 2. Deserializar a estructura legible
        sensor_data = parse_sensor_data(decrypted_data)
        
        return sensor_data
        
    except Exception as e:
        print(f" Error procesando datos: {e}")
        return None

def handle_client_connection(connection, address):
    """
    Maneja una conexión de cliente, potencialmente con múltiples mensajes
    """
    print(f" Conexión desde {address}")
    message_count = 0
    
    try:
        while True:
            # Recibir un mensaje completo
            data = b""
            while len(data) < EXPECTED_SIZE:
                try:
                    # Usar timeout para evitar bloqueos indefinidos
                    connection.settimeout(10.0)  # 10 segundos timeout
                    package = connection.recv(EXPECTED_SIZE - len(data))
                    if not package:
                        if data:
                            print(f"  Conexión cerrada con datos parciales: {len(data)} bytes")
                        return message_count
                    data += package
                except socket.timeout:
                    if data:
                        print(f"  Timeout con datos parciales: {len(data)} bytes")
                    return message_count
                except Exception as e:
                    print(f" Error recibiendo datos: {e}")
                    return message_count
            
            print(f" Mensaje #{message_count + 1} - Recibidos {len(data)} bytes")
            
            # Procesar el mensaje
            sensor_data = process_single_message(data)
            if sensor_data:
                message_count += 1
                yield sensor_data
            
            # Limpiar buffer para el próximo mensaje
            data = b""
            
    except Exception as e:
        print(f" Error en conexión: {e}")
    finally:
        print(f"Total mensajes procesados de {address}: {message_count}")

def receive_data():
    """
    Servidor principal que acepta conexiones y procesa mensajes
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Permitir múltiples conexiones en cola
        print(f" Servidor escuchando en {HOST}:{PORT}")
        
        while True:
            try:
                connection, address = server_socket.accept()
                
                with connection:
                    # Procesar todos los mensajes de esta conexión
                    for sensor_data in handle_client_connection(connection, address):
                        yield sensor_data
                        
            except KeyboardInterrupt:
                print(f"\n  Servidor detenido por usuario")
                break
            except Exception as e:
                print(f" Error aceptando conexión: {e}")
                continue