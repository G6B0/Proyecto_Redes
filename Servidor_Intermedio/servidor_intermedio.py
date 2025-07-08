from receive import receive_data
from verify import verify_data
from bin_to_json import bin_to_json
from forward import forward_data, pending_queue, reintento
from config import MAX_QUEUE_SIZE

def servidor_intermedio():
    print("Servidor intermedio iniciado...")
    reintento()
    
    for data_bin in receive_data():
        print(f"Datos recibidos: {data_bin}")
        print(f"Longitud: {len(data_bin)} bytes")
        
        if verify_data(data_bin):
            print(" Datos válidos")
            data_json = bin_to_json(data_bin)
            success = forward_data(data_json)
            print(f"JSON enviado: {data_json}")
            if not success:
                if len(pending_queue) < MAX_QUEUE_SIZE:
                    print("Guardando dato para reintento")
                    pending_queue.append(data_json)
                else:
                    print("Cola Llena, descartando dato")
            else:
                print(f"JSON enviado correctamente: {data_json}")
        else:
            print(" Datos inválidos - no pasaron verificación")
            # Debug: intentar desempaquetar de todas formas
            try:
                data_json = bin_to_json(data_bin)
                print(f"JSON (sin verificar): {data_json}")
            except Exception as e:
                print(f"Error al desempaquetar: {e}")

def main():
    servidor_intermedio()

if __name__ == "__main__":
    main()