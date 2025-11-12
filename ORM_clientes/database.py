#Configuración Base de Datos

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, sessionmaker


Base = declarative_base()
Engine = create_engine('sqlite:///PixelFood.db') #Conexion a BD

Session = sessionmaker(Engine)
session = Session()



    
    
