# main.py (actualizado)
from sqlalchemy import inspect
from database import Base, Engine, session
from models import Cliente, Ingredientes, Pedido, Menus
from crud.cliente_crud import *

if __name__ == '__main__':
    
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)

    inspector = inspect(Engine)
    print(inspector.get_table_names())
    
    # Probar creación de cliente con el nuevo modelo
    cliente1 = crear_cliente(session, nombre="Carlos", email="carlos@gmail.com")
    print(f"Cliente creado: {cliente1.nombre} - {cliente1.email}")