#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

struct Datos_sensor{
    int16_t id;
    uint64_t timestamp;
    float temperatura;
    float presion;
    float humedad;
    uint32_t checksum;
};
int main(int argc, char const* argv[]){
    socfd = socket(domain, type, protocol)
}

