import socket
from config import FINAL_SERVER_HOST, FINAL_SERVER_PORT

def forward_data(data_json):

    data_bytes = data_json.encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((FINAL_SERVER_HOST, FINAL_SERVER_PORT))
        s.sendall(data_bytes)