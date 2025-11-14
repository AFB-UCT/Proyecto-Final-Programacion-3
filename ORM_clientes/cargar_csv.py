# cargar_ingredientes_csv.py

import csv
import os
from crud.ingrediente_crud import sumar_stock_por_nombre

def cargar_ingredientes_desde_csv(ruta_csv: str):
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No existe el archivo: {ruta_csv}")

    insertados = 0
    actualizados = 0
    omitidos = 0

    with open(ruta_csv, newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            nombre = (fila.get("nombre") or "").strip()
            if not nombre:
                print("Fila sin nombre -> omitir:", fila)
                omitidos += 1
                continue
            try:
                cantidad = float((fila.get("cantidad") or 0))
            except (ValueError, TypeError):
                print("Cantidad inválida -> omitir:", fila)
                omitidos += 1
                continue
            unidad = (fila.get("unidad") or "").strip() or None

            ing = sumar_stock_por_nombre(nombre, cantidad, unidad)

            print(f"Procesado: {nombre} +{cantidad} {unidad or ''}")
            insertados += 1

    print(f"Proceso finalizado. Filas procesadas: {insertados}. Omitidos: {omitidos}.")

if __name__ == "__main__":
    ruta = "ingredientes_menu.csv"
    cargar_ingredientes_desde_csv(ruta)
