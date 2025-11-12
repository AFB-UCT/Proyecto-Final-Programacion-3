from sqlalchemy import Table, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

menu_ingrediente_table = Table(
    "menu_ingrediente",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("menu_id", Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False),
    Column("ingrediente_id", Integer, ForeignKey("ingredientes.id", ondelete="RESTRICT"), nullable=False),
    Column("cantidad", Float, nullable=False), 
    UniqueConstraint("menu_id", "ingrediente_id", name="uix_menu_ingrediente")
)


pedido_menu_table = Table(
    "pedido_menu",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("pedido_id", Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False),
    Column("menu_id", Integer, ForeignKey("menus.id", ondelete="RESTRICT"), nullable=False),
    Column("cantidad", Integer, nullable=False, default=1),
    UniqueConstraint("pedido_id", "menu_id", name="uix_pedido_menu")
)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120), nullable=False)


    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente id={self.id} nombre={self.nombre} email={self.email}>"


class Ingredientes(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True, index=True)
    cantidad = Column(Float, nullable=False, default=0.0)
    unidad = Column(String(30), nullable=True)


    menus = relationship("Menu", secondary=menu_ingrediente_table, back_populates="ingredientes")

    def __repr__(self):
        unit = self.unidad or ""
        return f"<Ingredientes id={self.id} nombre={self.nombre} cantidad={self.cantidad}{unit}>"


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True, index=True)
    descripcion = Column(String(500), nullable=True)
    precio = Column(Float, nullable=False, default=0.0)


    ingredientes = relationship("Ingredientes", secondary=menu_ingrediente_table, back_populates="menus")
    pedidos = relationship("Pedido", secondary=pedido_menu_table, back_populates="menus")

    def __repr__(self):
        return f"<Menu id={self.id} nombre={self.nombre} precio={self.precio}>"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False)
    total = Column(Float, nullable=False, default=0.0)


    cliente = relationship("Cliente", back_populates="pedidos")
    menus = relationship("Menu", secondary=pedido_menu_table, back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido id={self.id} cliente_id={self.cliente_id} total={self.total}>"
