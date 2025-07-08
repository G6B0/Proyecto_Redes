# Proyecto_Redes
Proyecto Semestral Redes de Computadores

## Instrucciones de uso

Este proyecto solamente funciona en linux.

1. Instalar Flask y aiohttp.

   Teniendo python3 y pip3 ya instalados, ejecute:
   ```bash
   pip3 install flask aiohttp
   ```
   
2. Abrir los directorios de los archivos.

     Abra 5 terminales y abra los directorios: `Cliente_Sensor`, `Servidor_Intermedio`, en las otras 2 terminales: `Servidor_Final` y la ultima terminal en el directorio `Cliente_Consulta`

3. Compile Cliente_Sensor.cpp con el siguiente comando:
   
     ```bash
     g++ -o Sensor Cliente_Sensor.cpp -std=c++11 -pthread
     ```
     
4. Ejecute el programa en el siguiente orden:
   En terminal 1 Servidor_Final
   ```bash
     python3 base.py
     ```
    ```bash
     python3 tcp.py
     ```
   En terminal 2 en Servidor_Final
    ```bash
     python3 api_rest.py
     ```
   En terminal 3 en Servidor_Final
    ```bash
     python3 servidor_intermedio.py
     ```
   En terminal 4 en Servidor_Final
    ```bash
     ./Sensor
     ```
   En terminal 5 en Cliente_Consulta
     ```bash
     python3 cliente_consulta.py
     ```

## HOST y PORT utilizados:

`Cliente Sensor` a `Servidor_Intermedio`; HOST: Local (0.0.0.0), PORT: 5000

`Servidor_Intermedio` a `Servidor_Final`; HOST: (127.0.0.1), PORT: 5001

`Servidor_Final` a `API`; HOST: Local (0.0.0.0), PORT: 5002

## Para la visualización del html

Se debe entrar a  http://localhost:5002/ y luego hacer click en Actualizar Datos
