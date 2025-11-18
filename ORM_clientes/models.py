# models.py (actualizado)
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

menus_ingredientes = Table('menus_ingredientes', Base.metadata, 
                        Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
                        Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
                        Column('cantidad_requerida', Float, nullable=False, default=1.0))

pedido_menu = Table('pedido_menu', Base.metadata,
                    Column('pedido_id', Integer, ForeignKey('pedido.id'), primary_key=True),
                    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
                    Column('cantidad', Integer, nullable=False, default=1))

class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    pedidos = relationship("Pedido", back_populates="cliente")

class Ingredientes(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    unidad = Column(String(50), nullable=True)
    cantidad = Column(Float(), nullable=False, default=0.0)
    
    menus = relationship("Menus", secondary=menus_ingredientes, back_populates="ingredientes")
    
class Menus(Base):
    __tablename__ = "menus"
    
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float(), nullable=False, default=0.0)
    
    ingredientes = relationship("Ingredientes", secondary=menus_ingredientes, back_populates="menus")
    pedidos = relationship("Pedido", secondary=pedido_menu, back_populates="menus")
    
class Pedido(Base):
    __tablename__ = "pedido"
    
    id = Column(Integer(), primary_key=True)
    descripcion = Column(String(100), nullable=False)
    total = Column(Float(), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="pendiente")

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", back_populates="pedidos")
    menus = relationship("Menus", secondary=pedido_menu, back_populates="pedidos")