#!/usr/bin/env python3
"""
Cliente de Consulta
– Consulta periódicamente la API REST (/datos)
– Verifica umbrales y levanta alertas
– Limpia pantalla en cada iteración para no llenar la terminal
"""

import aiohttp, asyncio, json
from datetime import datetime
import os, sys

API_URL   = "http://localhost:5002/datos"
INTERVAL  = 5                               # segundos entre consultas

THRESHOLDS = {
    "temperatura": (5.0, 40.0),
    "presion":     (950.0, 1050.0),
    "humedad":     (20.0, 80.0),
}

def clear_screen() -> None:
    """Borra la terminal de forma portable."""
    print("\x1bc", end="")  # secuencia ANSI (funciona en VS Code/macOS/Linux)

def alertas(row: dict) -> list[str]:
    """Devuelve lista de alertas para la fila dada."""
    msgs = []
    tmin, tmax = THRESHOLDS["temperatura"]
    pmin, pmax = THRESHOLDS["presion"]
    hmin, hmax = THRESHOLDS["humedad"]
    if not tmin <= row["temperatura"] <= tmax:
        msgs.append(f"Temperatura fuera de rango ({row['temperatura']})")
    if not pmin <= row["presion"] <= pmax:
        msgs.append(f"Presión fuera de rango ({row['presion']})")
    if not hmin <= row["humedad"] <= hmax:
        msgs.append(f"Humedad fuera de rango ({row['humedad']})")
    return msgs

def imprimir_tabla(filas: list[dict]) -> None:
    """Imprime la tabla (solo hora) y borra pantalla cada ciclo."""
    clear_screen()
    ahora = datetime.now().strftime("%H:%M:%S")
    print(f"CLIENTE CONSULTA : Última actualización: {ahora}")
    print("—" * 100)

    # Encabezados               Sensor  Hora       Temp      Presión         Humedad
    print(f"{'Sensor':<6} {'Hora':<9} {'Temp (°C)':<11} "
          f"{'Presión (hPa)':<14} {'Humedad (%)':<12} Alertas")
    print("=" * 100)

    # Muestra las 5 lecturas más recientes
    for r in filas[-5:]:
        hora = datetime.fromtimestamp(int(r["fecha_hora"])).strftime("%H:%M:%S")
        al   = "; ".join(alertas(r))
        print(f"{r['id']:<6} {hora:<9} {r['temperatura']:<11.1f} "
              f"{r['presion']:<14.2f} {r['humedad']:<12.1f} {al}")

    print("—" * 100)
    print("Umbrales:", THRESHOLDS)


async def obtener_datos(api_url: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, ssl=False) as resp:
            return await resp.json()

async def fetch_loop(api_url: str, interval: int):
    while True:
        try:
            filas = await obtener_datos(api_url)
            imprimir_tabla(filas)
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(interval)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default=API_URL, help="URL del endpoint /datos")
    parser.add_argument("--interval", type=int, default=INTERVAL,
                        help="Segundos entre consultas")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fetch_loop(args.api, args.interval))
    except KeyboardInterrupt:
        print("\nRecibida señal SIGTERM: cerrando…")
        print("Cliente detenido con éxito")

if __name__ == "__main__":
    main()

