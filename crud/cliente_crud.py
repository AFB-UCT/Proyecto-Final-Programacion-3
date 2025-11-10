from sqlalchemy.orm import Session

from ORM.models import Cliente
import os
import sys

sys.path.append(os.path.dirname(__file__))

def crear_cliente(db: Session, nombre: str, edad:int):

    nuevo_cliente = Cliente(nombre=nombre, edad=edad)

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

def actualizar_cliente(db: Session, cliente_id:int, nombre:str, edad: int):

    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente:
        cliente.nombre = nombre
        cliente.edad = edad

        db.commit()

        db.refresh(cliente)
    return cliente