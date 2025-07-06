import socket
from datetime import datetime

HOST = 'localhost'
PORT = 5000

# Simular un paquete de datos (ID, fecha_hora, temperatura, presion, humedad)
datos = f'1,{datetime.now().strftime("%Y-%m-%d %H:%M:%S")},27.5,1013.25,45.0'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(datos.encode('utf-8'))

print('Datos enviados:', datos)