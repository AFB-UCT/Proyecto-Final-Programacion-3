import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database import get_session
from models import Ingredientes

# ---------------------------------------------------------
#   CREAR INGREDIENTE
# ---------------------------------------------------------
def crear_ingrediente(nombre: str, cantidad: float = 0.0, unidad: str = None):
    nombre = (nombre or "").strip()
    if not nombre:
        raise ValueError("Nombre de ingrediente vacío.")

    # Normalizar cantidad
    try:
        cantidad = float(cantidad or 0)
    except (ValueError, TypeError):
        raise ValueError("Cantidad inválida.")

    if cantidad < 0:
        raise ValueError("Cantidad no puede ser negativa.")

    with get_session() as db:
        existente = db.query(Ingredientes).filter(Ingredientes.nombre == nombre).first()
        if existente:
            raise ValueError("Ingrediente ya existe. Usa actualizar_ingrediente para modificar.")

        nuevo = Ingredientes(nombre=nombre, cantidad=cantidad, unidad=unidad)
        db.add(nuevo)
        db.commit()       # ← NECESARIO
        db.refresh(nuevo) # ← ahora sí funciona

        return nuevo


# ---------------------------------------------------------
#   OBTENER INGREDIENTE POR ID
# ---------------------------------------------------------
def obtener_ingrediente(id_: int):
    with get_session() as db:
        return db.query(Ingredientes).filter(Ingredientes.id == id_).first()


# ---------------------------------------------------------
#   BUSCAR INGREDIENTE POR NOMBRE
# ---------------------------------------------------------
def buscar_ingrediente_por_nombre(nombre: str):
    with get_session() as db:
        return db.query(Ingredientes).filter(Ingredientes.nombre == nombre).first()


# ---------------------------------------------------------
#   ACTUALIZAR INGREDIENTE
# ---------------------------------------------------------
def actualizar_ingrediente(id_: int, nombre: str = None, unidad: str = None, cantidad: float = None):
    with get_session() as db:
        ing = db.query(Ingredientes).filter(Ingredientes.id == id_).first()
        if not ing:
            raise ValueError("Ingrediente no encontrado.")

        if nombre:
            ing.nombre = nombre.strip()

        if cantidad is not None:
            try:
                cantidad = float(cantidad)
            except (ValueError, TypeError):
                raise ValueError("Cantidad inválida.")
            if cantidad < 0:
                raise ValueError("Cantidad no puede ser negativa.")
            ing.cantidad = cantidad

        if unidad is not None:
            ing.unidad = unidad

        db.commit()       # ← NECESARIO
        db.refresh(ing)   # ← ahora sí funciona

        return ing


# ---------------------------------------------------------
#   ELIMINAR INGREDIENTE
# ---------------------------------------------------------
def eliminar_ingrediente(id_: int):
    with get_session() as db:
        ing = db.query(Ingredientes).filter(Ingredientes.id == id_).first()
        if not ing:
            raise ValueError("Ingrediente no encontrado.")

        db.delete(ing)
        db.commit()       # ← NECESARIO

        return True


# ---------------------------------------------------------
#   SUMAR STOCK POR NOMBRE
# ---------------------------------------------------------
def sumar_stock_por_nombre(nombre: str, cantidad: float, unidad: str = None):
    nombre = (nombre or "").strip()
    if not nombre:
        raise ValueError("Nombre vacío.")

    try:
        cantidad = float(cantidad)
    except (ValueError, TypeError):
        raise ValueError("Cantidad inválida.")

    with get_session() as db:

        ing = db.query(Ingredientes).filter(Ingredientes.nombre == nombre).first()

        if ing:
            ing.cantidad += cantidad

            # Si no tiene unidad y ahora viene una, la asignamos
            if unidad:
                ing.unidad = unidad

            db.commit()
            db.refresh(ing)
            return ing

        # Crear nuevo ingrediente con unidad
        nuevo = Ingredientes(
            nombre=nombre,
            cantidad=cantidad,
            unidad=unidad
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
