import socket
import sqlite3
import json

# Configuración del servidor TCP
HOST = '0.0.0.0'
PORT = 5001

# Conexión a la base de datos
conn = sqlite3.connect('sensores.db', check_same_thread=False)
cursor = conn.cursor()

def insertar_datos_json(data_json_str):

    try:

        data = json.loads(data_json_str)
        id_sensor = data['id_sensor']
        fecha_hora = data['fecha_hora']
        temperatura = data['temperatura']
        presion = data['presion']
        humedad = data['humedad']
        cursor.execute(

            'INSERT INTO datos_sensor (id, fecha_hora, temperatura, presion, humedad) VALUES (?, ?, ?, ?, ?)',

            (id_sensor, fecha_hora, temperatura, presion, humedad)

        )

        conn.commit()

        print('Datos insertados correctamente.')

    except Exception as e:

        print('Error al insertar datos:', e)

# Iniciar servidor TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor TCP escuchando en {HOST}:{PORT}')

    while True:
        client_socket, addr = s.accept()
        with client_socket:
            print('Conexión desde', addr)
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print('Datos recibidos:', data)
                insertar_datos_json(data)