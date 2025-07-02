from receive import receive_data
from verify import verify_data
from bin_to_json import bin_to_json
from forward import forward_data

def servidor_intermedio():

    data_bin = receive_data()

    if verify_data(data_bin):
        data_json = bin_to_json(data_bin)
        forward_data(data_json)