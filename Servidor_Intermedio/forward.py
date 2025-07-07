import socket
from config import FINAL_SERVER_HOST, FINAL_SERVER_PORT

def forward_data(data_json):
    data_bytes = data_json.encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)  #Timeout de 3 segundos para conexión y ACK

        try:
            s.connect((FINAL_SERVER_HOST, FINAL_SERVER_PORT))
            s.sendall(data_bytes)

            ack = s.recv(1024)

            if ack.strip() == b'ACK':
                print(" ACK recibido del servidor final")
            else:
                print(f" Respuesta inesperada del servidor final: {ack}")
        except socket.timeout:
            print(" Timeout esperando ACK del servidor final (no respondió)")
        except socket.error as e:
            print(f" Error al conectar o comunicar con servidor final: {e}")
