from sqlalchemy.orm import Session
from models import Ingredientes

def insertar_ingrediente(db: Session, id: int, nombre: str, cantidad: int):
    
    nuevo_ingrediente = Ingredientes(id=id, nombre=nombre, cantidad=cantidad)
    
    db.add(nuevo_ingrediente)
    