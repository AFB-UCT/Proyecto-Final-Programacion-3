import sys
import os
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session

from models import Cliente

def crear_cliente(db: Session, nombre: str):

    nuevo_cliente = Cliente(nombre=nombre)

    db.add(nuevo_cliente)

    db.commit()

    db.refresh(nuevo_cliente)

    return(nuevo_cliente)

def obtener_cliente(db: Session, cliente_id: int):

    return db.query(Cliente).filter(Cliente.id==cliente_id).first()

def obtener_clientes(db: Session):
    return db.query(Cliente).all()

def eliminar_cliente(db: Session, cliente_id:int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente:
        db.delete(cliente)

        db.commit()

    return cliente

def actualizar_cliente(db: Session, cliente_id:int, nombre:str):

    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente:
        cliente.nombre = nombre

        db.commit()

        db.refresh(cliente)
    return cliente

if __name__ == "__main__":
    print("cliente_crud")