import socket
from config import HOST, PORT, EXPECTED_SIZE

def receive_data():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
        S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        S.bind((HOST, PORT))
        S.listen(1)
        connection, address = S.accept()

        with connection:
            data = b""
            while len(data) < EXPECTED_SIZE:
                package = connection.recv(EXPECTED_SIZE - len(data))
                if not package:
                    raise ConnectionError("ERROR: Conexión cerrada inesperadamente.")
                data = data + package

    return data