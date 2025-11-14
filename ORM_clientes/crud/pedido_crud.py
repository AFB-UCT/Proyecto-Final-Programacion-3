import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from models import Pedido

def crear_pedido(db: Session, nombre: str, cantidad: int, precio: float, cliente_id: int, fecha: datetime = None):
    nuevo_pedido = Pedido(
        nombre=nombre,
        cantidad=cantidad,
        precio=precio,
        cliente_id=cliente_id,
        fecha=fecha or datetime.utcnow()
    )
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    return nuevo_pedido

def obtener_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def obtener_pedidos(db: Session):
    return db.query(Pedido).all()

def eliminar_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if pedido:
        db.delete(pedido)
        db.commit()
    
    return pedido

def actualizar_pedido(db: Session, pedido_id: int, nombre: str = None, cantidad: int = None, precio: float = None, cliente_id: int = None, fecha: datetime = None):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if pedido:
        if nombre is not None:
            pedido.nombre = nombre
        if cantidad is not None:
            pedido.cantidad = cantidad
        if precio is not None:
            pedido.precio = precio
        if cliente_id is not None:
            pedido.cliente_id = cliente_id
        if fecha is not None:
            pedido.fecha = fecha
            
        db.commit()
        db.refresh(pedido)
    
    return pedido

if __name__ == "__main__":
    print("pedido_crud actualizado")
