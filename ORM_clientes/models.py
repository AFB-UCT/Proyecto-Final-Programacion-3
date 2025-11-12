from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

menus_ingredientes = Table('menus_ingredientes', Base.metadata, 
                        Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
                        Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True))

pedido_menu = Table('pedido_menu', Base.metadata,
                    Column('pedido_id', Integer, ForeignKey('pedido.id'), primary_key=True),
                    Column(('menu_id'), Integer, ForeignKey('menus.id'), primary_key=True))

class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)

    pedidos=relationship("Pedido", back_populates="cliente")

class Ingredientes(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    cantidad = Column(Integer(), nullable=False)
    
    menus = relationship("Menus", secondary=menus_ingredientes, back_populates="ingredientes")
    
class Menus(Base):
    __tablename__ = "menus"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    ingredientes=relationship("Ingredientes", secondary=menus_ingredientes, back_populates="menus")
    pedidos=relationship("Pedido", secondary=pedido_menu, back_populates="menus")
    
    
class Pedido(Base):
    __tablename__ = "pedido"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    cantidad = Column(Integer(), nullable=False)
    precio = Column(Integer(), nullable=False)

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", back_populates="pedidos")

    menus = relationship("Menus", secondary=pedido_menu, back_populates="pedidos")
    
    
