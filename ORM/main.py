import sys
import os

sys.path.append('crud')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base, Cliente
from crud.cliente_crud import crear_cliente

Base = declarative_base()
Engine = create_engine('sqlite:///PixelFood.db')


Session = sessionmaker(Engine)
session = Session()


if __name__ == "__main__":
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)

inspector = inspect(Engine)
print(inspector.get_table_names())

cliente1=crear_cliente(session, nombre="Pedro", edad=30)