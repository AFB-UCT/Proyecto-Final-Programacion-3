# Definicion de los modelos ORM
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)

    def __str__(self):
        return self.nombre

    def __int__(self):
        return self.edad
    

