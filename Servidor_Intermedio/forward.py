import socket
from config import FINAL_SERVER_HOST, FINAL_SERVER_PORT
import threading
import time

pending_queue = []

def forward_data(data_json):
    data_bytes = data_json.encode('utf-8')

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)  #Timeout de 3 segundos para conexión y ACK
            s.connect((FINAL_SERVER_HOST, FINAL_SERVER_PORT))
            s.sendall(data_bytes)

            ack = s.recv(1024)

            if ack.strip() == b'ACK':
                print(" ACK recibido del servidor final")
                return True
            
            else:
                print(f" Respuesta inesperada del servidor final: {ack}")
                return False
            
    except socket.timeout:
            print(" Timeout esperando ACK del servidor final (no respondió)")
            return False
    except socket.error as e:
            print(f" Error al conectar o comunicar con servidor final: {e}")
            return False
    
def retry_pending ():
     """
     Intenta reenviar datos pendientes periodicamente
     """

     while True:
          if pending_queue:
               print(f"Intentando reenviar {len(pending_queue)} datos pendientes")
          for data_json in pending_queue[:]:
               success = forward_data(data_json)
               if success:
                    pending_queue.remove(data_json)
                    print("Dato reenviado y removido de la cola pendiente")
               else:
                    print("No se pudo reenviar datos, seguirá en cola")

          time.sleep(10)


def reintento():
     """
     Lanza un thread que corre retry_pending() en paralelo
     """
     thread = threading.Thread(target=retry_pending, daemon= True)
     thread.start()
        
