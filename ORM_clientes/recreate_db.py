# recreate_db.py  (ADVERTENCIA: borra datos)
from database import Engine
from models import Base

print("Dropping all tables (si existen) y recreando esquema desde models.py...")
Base.metadata.drop_all(bind=Engine)
Base.metadata.create_all(bind=Engine)
print("Hecho: tablas recreadas con claves foráneas según models.py.")
