from receive import receive_data
from verify import verify_data
from bin_to_json import bin_to_json
from forward import forward_data

def servidor_intermedio():
    print("Servidor intermedio iniciado...")
    
    for data_bin in receive_data():
        print(f"Datos recibidos: {data_bin}")
        print(f"Longitud: {len(data_bin)} bytes")
        
        if verify_data(data_bin):
            print(" Datos válidos")
            data_json = bin_to_json(data_bin)
            forward_data(data_json)
            print(f"JSON enviado: {data_json}")
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