# Proyecto_Redes
Proyecto Semestral Redes de Computadores

## Instrucciones de uso

Este proyecto solamente funciona en linux.

1. Instalar Flask.

   Teniendo python3 y pip3 ya instalados, ejecute:
   ```bash
   pip3 install flask
   ```
   
2. Abrir los directorios de los archivos.

     Abra 4 terminales y abra los directorios: `Cliente Sensor`, `Servidor_Intermedio` y en las otras 2 terminales: `Servidor_Final`

3. Compile Cliente_Sensor.cpp con el siguiente comando:
   
     ```bash
     g++ -o Sensor Cliente_Sensor.cpp -std=c++11 -pthread
     ```
     
4. Ejecute el programa en el siguiente orden:
   
    ```bash
     python3 tcp.py
     ```
    ```bash
     python3 api_rest.py
     ```
    ```bash
     python3 servidor_intermedio.py
     ```
    ```bash
     ./Sensor
     ```

## HOST y PORT utilizados:

`Cliente Sensor` a `Servidor_Intermedio`; HOST: Local (0.0.0.0), PORT: 5000

`Servidor_Intermedio` a `Servidor_Final`; HOST: Local (127.0.0.1), PORT: 5001

`Servidor_Final` a `API`; HOST: Local (0.0.0.0), PORT: 5002
