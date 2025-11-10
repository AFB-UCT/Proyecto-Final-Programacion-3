#Configuración Base de Datos

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table, inspect

Base = declarative_base()
Engine = create_engine('sqlite:///Restaurant.db') #Conexion a BD

Session = sessionmaker(Engine)
session = Session()



    
    
