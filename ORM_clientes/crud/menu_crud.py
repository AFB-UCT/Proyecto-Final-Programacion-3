import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session

from models import Menus

def crear_menu(db: Session, nombre: str):
    nuevo_menu = Menus(nombre=nombre)
    
    db.add(nuevo_menu)
    db.commit()
    db.refresh(nuevo_menu)
    
    return nuevo_menu

def obtener_menu(db: Session, menu_id: int):
    return db.query(Menus).filter(Menus.id == menu_id).first()

def obtener_menus(db: Session):
    return db.query(Menus).all()

def eliminar_menu(db: Session, menu_id: int):
    menu = db.query(Menus).filter(Menus.id == menu_id).first()
    
    if menu:
        db.delete(menu)
        db.commit()
    
    return menu

def actualizar_menu(db: Session, menu_id: int, nombre: str):
    menu = db.query(Menus).filter(Menus.id == menu_id).first()
    
    if menu:
        menu.nombre = nombre
        db.commit()
        db.refresh(menu)
    
    return menu

if __name__ == "__main__":
    print("menu_crud")