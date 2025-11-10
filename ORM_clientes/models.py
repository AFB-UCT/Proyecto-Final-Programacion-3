from sqlalchemy import Column, Integer, String, ForeignKey, Table, inspect
from database import Base

class Ingredientes(Base):
    __tablename__ = "Ingredientes"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    cantidad = Column(Integer(), nullable=False, unique=True)
    
    def __str__(self):
        return self.nombre
    
class Menus(Base):
    __tablename__ = "Menús"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    def __str__(self):
        return self.nombre
    
    
class Pedido(Base):
    __tablename__ = "Pedido"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer(), nullable=False)
    precio = Column(Integer(), nullable=False)
    

    
    
    
class Cliente(Base):
    __tablename__ = "Cliente"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    
    