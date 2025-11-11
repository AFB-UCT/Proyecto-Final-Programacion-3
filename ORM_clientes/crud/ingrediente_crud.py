from sqlalchemy.orm import Session

from models import Ingredientes

def crear_ingrediente(db: Session, nombre: str, cantidad: int):
    nuevo_ingrediente = Ingredientes(
        nombre=nombre,
        cantidad=cantidad
    )
    
    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)
    
    return nuevo_ingrediente

def obtener_ingrediente(db: Session, ingrediente_id: int):
    return db.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()

def obtener_ingredientes(db: Session):
    return db.query(Ingredientes).all()

def eliminar_ingrediente(db: Session, ingrediente_id: int):
    ingrediente = db.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
    
    if ingrediente:
        db.delete(ingrediente)
        db.commit()
    
    return ingrediente

def actualizar_ingrediente(db: Session, ingrediente_id: int, nombre: str = None, cantidad: int = None):
    ingrediente = db.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
    
    if ingrediente:
        if nombre is not None:
            ingrediente.nombre = nombre
        if cantidad is not None:
            ingrediente.cantidad = cantidad
            
        db.commit()
        db.refresh(ingrediente)
    
    return ingrediente