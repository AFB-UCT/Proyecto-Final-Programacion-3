import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database import get_session
from models import Pedido

def crear_pedido(descripcion: str, total: float, cliente_id: int, estado: str = "pendiente", fecha: datetime = None):
    descripcion = (descripcion or "").strip()
    if not descripcion:
        raise ValueError("Descripción del pedido vacía.")

    try:
        total = float(total)
    except (ValueError, TypeError):
        raise ValueError("Total inválido.")

    if total < 0:
        raise ValueError("Total no puede ser negativo.")

    with get_session() as db:
        nuevo_pedido = Pedido(
            descripcion=descripcion,
            total=total,
            cliente_id=cliente_id,
            estado=estado,
            fecha=fecha or datetime.utcnow()
        )
        
        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)
        
        return nuevo_pedido


def obtener_pedido(id_: int):
    with get_session() as db:
        return db.query(Pedido).filter(Pedido.id == id_).first()

def obtener_pedidos():
    with get_session() as db:
        return db.query(Pedido).all()

def obtener_pedidos_por_cliente(cliente_id: int):
    with get_session() as db:
        return db.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()


def actualizar_pedido(id_: int, descripcion: str = None, total: float = None, cliente_id: int = None, estado: str = None, fecha: datetime = None):
    with get_session() as db:
        pedido = db.query(Pedido).filter(Pedido.id == id_).first()
        if not pedido:
            raise ValueError("Pedido no encontrado.")

        if descripcion:
            pedido.descripcion = descripcion.strip()

        if total is not None:
            try:
                total = float(total)
            except (ValueError, TypeError):
                raise ValueError("Total inválido.")
            if total < 0:
                raise ValueError("Total no puede ser negativo.")
            pedido.total = total

        if cliente_id is not None:
            pedido.cliente_id = cliente_id

        if estado is not None:
            pedido.estado = estado

        if fecha is not None:
            pedido.fecha = fecha

        db.commit()
        db.refresh(pedido)

        return pedido


def eliminar_pedido(id_: int):
    with get_session() as db:
        pedido = db.query(Pedido).filter(Pedido.id == id_).first()
        if not pedido:
            raise ValueError("Pedido no encontrado.")

        db.delete(pedido)
        db.commit()

        return True


def agregar_menu_a_pedido(pedido_id: int, menu_id: int):
    with get_session() as db:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise ValueError("Pedido no encontrado.")

        from models import Menus
        menu = db.query(Menus).filter(Menus.id == menu_id).first()
        if not menu:
            raise ValueError("Menú no encontrado.")

        if menu not in pedido.menus:
            pedido.menus.append(menu)
            db.commit()
            db.refresh(pedido)

        return pedido


def remover_menu_de_pedido(pedido_id: int, menu_id: int):
    with get_session() as db:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise ValueError("Pedido no encontrado.")

        from models import Menus
        menu = db.query(Menus).filter(Menus.id == menu_id).first()
        if not menu:
            raise ValueError("Menú no encontrado.")

        if menu in pedido.menus:
            pedido.menus.remove(menu)
            db.commit()
            db.refresh(pedido)

        return pedido


def obtener_total_ventas_por_periodo(fecha_inicio: datetime, fecha_fin: datetime):
    with get_session() as db:
        pedidos = db.query(Pedido).filter(
            Pedido.fecha >= fecha_inicio,
            Pedido.fecha <= fecha_fin,
            Pedido.estado == "completado"
        ).all()
        
        # Usando reduce para calcular el total (ejemplo de programación funcional)
        from functools import reduce
        if pedidos:
            total_ventas = reduce(lambda x, y: x + y.total, pedidos, 0)
        else:
            total_ventas = 0
            
        return total_ventas

if __name__ == "__main__":
    print("pedido_crud actualizado con misma estructura")