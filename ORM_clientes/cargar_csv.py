# cargar_ingredientes_csv.py
import csv
from sqlalchemy.exc import IntegrityError
from database import Session
from models import Ingredientes

def cargar_ingredientes_desde_csv(ruta_csv: str):
    """
    Lee un archivo CSV con columnas: nombre, cantidad, unidad
    y carga cada ingrediente en la base de datos.
    """
    ingredientes_insertados = 0
    ingredientes_omitidos = 0

    with Session() as db:
        with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)

            for fila in lector:
                nombre = fila.get("nombre", "").strip()
                unidad = fila.get("unidad", "").strip() or None
                cantidad = float(fila.get("cantidad", 0))


                if not nombre:
                    print(f"Fila sin nombre: {fila}")
                    continue


                existente = db.query(Ingredientes).filter_by(nombre=nombre).first()
                if existente:
                    print(f"⏭Ingrediente '{nombre}' ya existe, se omite.")
                    ingredientes_omitidos += 1
                    continue

                nuevo = Ingredientes(nombre=nombre, cantidad=cantidad, unidad=unidad)
                db.add(nuevo)
                ingredientes_insertados += 1

        try:
            db.commit()
            print(f"Se insertaron {ingredientes_insertados} ingredientes nuevos.")
            print(f"Se omitieron {ingredientes_omitidos} ya existentes.")
        except IntegrityError as e:
            db.rollback()
            print("Error de integridad:", e)

if __name__ == "__main__":
    ruta = "ingredientes_menu.csv"
    cargar_ingredientes_desde_csv(ruta)
    print("Ingredientes cargados")
