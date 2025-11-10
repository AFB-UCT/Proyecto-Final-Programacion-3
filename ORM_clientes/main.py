from sqlalchemy import inspect
from database import Base, Engine
from models import Cliente, Ingredientes, Pedido, Menus



if __name__ == '__main__':
    
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)


inspector = inspect(Engine)
print(inspector.get_table_names())