# database.py
from contextlib import contextmanager
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

URL = "sqlite:///PixelFood.db"

Engine = create_engine(URL, echo=False, future=True)

Base = declarative_base()

Session = sessionmaker(bind=Engine, autoflush=False, autocommit=False, future=True)
session = Session()


@contextmanager
def get_session():
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def test_connection() -> bool:
    try:
        with Engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print("Error al conectar con la BD:", e)
        return False

def init_db():
    Base.metadata.create_all(bind=Engine)

def inspect_tables():
    inspector = inspect(Engine)
    return inspector.get_table_names()
