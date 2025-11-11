from sqlalchemy.orm import Session

from models import Pedido

def crear_pedido(db: Session, nombre: str, cantidad: int, precio: int, cliente_id: int):
    nuevo_pedido = Pedido(
        nombre=nombre,
        cantidad=cantidad,
        precio=precio,
        cliente_id=cliente_id
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

def actualizar_pedido(db: Session, pedido_id: int, nombre: str = None, cantidad: int = None, precio: int = None, cliente_id: int = None):
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
            
        db.commit()
        db.refresh(pedido)
    
    return pedido