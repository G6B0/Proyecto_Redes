#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <chrono>
#include <thread>
#include <random>
#include <ctime>
#include <iomanip>

// Estructura para los datos del sensor
struct SensorData {
    int16_t id;
    uint64_t timestamp;
    float temperatura;
    float presion;
    float humedad;
    uint32_t checksum;
} __attribute__((packed));

class SensorClient {
private:
    int sock;
    struct sockaddr_in serv_addr;
    std::string server_ip;
    int server_port;
    int16_t sensor_id;
    std::mt19937 rng;
    
    // Función simple de checksum
    uint32_t calculateChecksum(const SensorData& data) {
        uint32_t sum = 0;
        sum += data.id;
        sum += static_cast<uint32_t>(data.timestamp);
        sum += static_cast<uint32_t>(data.temperatura * 100);
        sum += static_cast<uint32_t>(data.presion * 100);
        sum += static_cast<uint32_t>(data.humedad * 100);
        return sum;
    }
    
    void encryptData(SensorData& data, uint8_t key = 0xAB) {
    uint8_t* ptr = reinterpret_cast<uint8_t*>(&data);
    for (size_t i = 0; i < 22; ++i) {  // Solo cifrar bytes 0 a 21
        ptr[i] ^= key;
    }
}
    
    // Generar datos simulados del sensor
    SensorData generateSensorData() {
        SensorData data;
        data.id = sensor_id;
        
        // Timestamp actual
        auto now = std::chrono::system_clock::now();
        auto time_t = std::chrono::system_clock::to_time_t(now);
        data.timestamp = static_cast<uint64_t>(time_t);
        
        // Generar datos simulados con algo de variación
        std::uniform_real_distribution<float> temp_dist(18.0f, 28.0f);
        std::uniform_real_distribution<float> pres_dist(1000.0f, 1025.0f);
        std::uniform_real_distribution<float> hum_dist(35.0f, 70.0f);
        
        data.temperatura = temp_dist(rng);
        data.presion = pres_dist(rng);
        data.humedad = hum_dist(rng);
        
        // Calcular checksum antes del cifrado
        data.checksum = calculateChecksum(data);
        
        return data;
    }
    
public:
    SensorClient(const std::string& ip, int port, int16_t id) 
        : server_ip(ip), server_port(port), sensor_id(id), sock(-1) {
        // Inicializar generador aleatorio
        rng.seed(std::chrono::steady_clock::now().time_since_epoch().count());
    }
    
    ~SensorClient() {
        disconnect();
    }
    
    bool connect() {
        // Crear socket
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            std::cerr << "Error creando socket" << std::endl;
            return false;
        }
        
        // Configurar dirección del servidor
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(server_port);
        
        if (inet_pton(AF_INET, server_ip.c_str(), &serv_addr.sin_addr) <= 0) {
            std::cerr << "Dirección IP inválida: " << server_ip << std::endl;
            close(sock);
            sock = -1;
            return false;
        }
        
        // Conectar al servidor
        if (::connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
            std::cerr << "Error conectando al servidor " << server_ip << ":" << server_port << std::endl;
            close(sock);
            sock = -1;
            return false;
        }
        
        std::cout << " Conectado al servidor " << server_ip << ":" << server_port << std::endl;
        std::cout << " Sensor ID: " << sensor_id << std::endl;
        return true;
    }
    
    void disconnect() {
        if (sock >= 0) {
            close(sock);
            sock = -1;
            std::cout << " Desconectado del servidor" << std::endl;
        }
    }
    
    bool sendSensorData() {
        if (sock < 0) {
            std::cerr << " No hay conexión activa" << std::endl;
            return false;
        }
        
        // Generar datos del sensor
        SensorData data = generateSensorData();
        
        // Mostrar datos antes del cifrado
        std::cout << "\n Enviando datos del sensor:" << std::endl;
        std::cout << "   ID: " << data.id << std::endl;
        std::cout << "   Timestamp: " << data.timestamp << std::endl;
        std::cout << "   Temperatura: " << std::fixed << std::setprecision(2) << data.temperatura << "°C" << std::endl;
        std::cout << "   Presión: " << data.presion << " hPa" << std::endl;
        std::cout << "   Humedad: " << data.humedad << "%" << std::endl;
        std::cout << "   Checksum: 0x" << std::hex << data.checksum << std::dec << std::endl;
        
        // Cifrar datos (excepto checksum)
        encryptData(data);
        
        // Enviar datos
        ssize_t bytes_sent = send(sock, &data, sizeof(data), 0);
        if (bytes_sent < 0) {
            std::cerr << " Error enviando datos" << std::endl;
            return false;
        }
        
        if (bytes_sent != sizeof(data)) {
            std::cerr << "  Advertencia: Solo se enviaron " << bytes_sent << " de " << sizeof(data) << " bytes" << std::endl;
        }
        
        std::cout << " Datos enviados correctamente (" << bytes_sent << " bytes)" << std::endl;
        return true;
    }
    
    bool reconnect() {
        std::cout << " Intentando reconectar..." << std::endl;
        disconnect();
        
        // Esperar un poco antes de reconectar
        std::this_thread::sleep_for(std::chrono::seconds(2));
        
        return connect();
    }
    
    void runContinuous(int interval_seconds = 5, int max_failures = 3) {
        int consecutive_failures = 0;
        
        std::cout << " Iniciando envío continuo cada " << interval_seconds << " segundos" << std::endl;
        std::cout << " Presiona Ctrl+C para detener" << std::endl;
        
        while (true) {
            if (!sendSensorData()) {
                consecutive_failures++;
                std::cout << " Fallo #" << consecutive_failures << " de " << max_failures << std::endl;
                
                if (consecutive_failures >= max_failures) {
                    std::cout << " Demasiados fallos consecutivos, intentando reconectar..." << std::endl;
                    
                    if (reconnect()) {
                        consecutive_failures = 0;
                        std::cout << " Reconexión exitosa" << std::endl;
                    } else {
                        std::cout << " Fallo en reconexión, esperando..." << std::endl;
                        std::this_thread::sleep_for(std::chrono::seconds(10));
                        continue;
                    }
                }
            } else {
                consecutive_failures = 0;
            }
            
            // Esperar antes del próximo envío
            std::this_thread::sleep_for(std::chrono::seconds(interval_seconds));
        }
    }
};

int main(int argc, char* argv[]) {
    std::string server_ip = "127.0.0.1";  // localhost por defecto
    int server_port = 5000;               // puerto por defecto
    int16_t sensor_id = 1;                // ID del sensor por defecto
    int interval = 5;                     // intervalo en segundos
    
    // Procesar argumentos de línea de comandos
    if (argc >= 2) server_ip = argv[1];
    if (argc >= 3) server_port = std::atoi(argv[2]);
    if (argc >= 4) sensor_id = std::atoi(argv[3]);
    if (argc >= 5) interval = std::atoi(argv[4]);
    
    std::cout << " Cliente Sensor IoT" << std::endl;
    std::cout << " Servidor: " << server_ip << ":" << server_port << std::endl;
    std::cout << " Sensor ID: " << sensor_id << std::endl;
    std::cout << " Intervalo: " << interval << " segundos" << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    
    try {
        SensorClient client(server_ip, server_port, sensor_id);
        
        // Intentar conectar
        if (!client.connect()) {
            std::cerr << " No se pudo conectar al servidor" << std::endl;
            return 1;
        }
        
        // Ejecutar envío continuo
        client.runContinuous(interval);
        
    } catch (const std::exception& e) {
        std::cerr << " Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}