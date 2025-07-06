import socket
import sqlite3

# Configuración del servidor TCP
HOST = '0.0.0.0'
PORT = 5000

# Conexión a la base de datos
conn = sqlite3.connect('sensores.db', check_same_thread=False)
cursor = conn.cursor()

def insertar_datos(data):
    try:
        id_sensor, fecha_hora, temperatura, presion, humedad = data.strip().split(',')
        cursor.execute('INSERT INTO datos_sensor (id, fecha_hora, temperatura, presion, humedad) VALUES (?, ?, ?, ?, ?)',
                       (int(id_sensor), fecha_hora, float(temperatura), float(presion), float(humedad)))
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
                insertar_datos(data)