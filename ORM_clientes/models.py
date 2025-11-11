from sqlalchemy import Column, Integer, String, ForeignKey, Table, inspect
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)

    pedidos=relationship("Pedido", back_populates="cliente")

class Ingredientes(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    cantidad = Column(Integer(), nullable=False, unique=True)
    
    def __str__(self):
        return self.nombre
    
class Menus(Base):
    __tablename__ = "menus"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    def __str__(self):
        return self.nombre
    
    
class Pedido(Base):
    __tablename__ = "pedido"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer(), nullable=False)
    precio = Column(Integer(), nullable=False)

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", back_populates="pedidos")
    
