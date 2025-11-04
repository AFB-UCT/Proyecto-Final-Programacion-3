# IMenu.py
from dataclasses import dataclass, field
from typing import Protocol, List, Optional
from Ingrediente import Ingrediente
from Stock import Stock

@dataclass
class IMenu(Protocol):
    nombre: str
    ingredientes: List[Ingrediente] = field(default_factory=list)
    precio: float = 0.0
    cantidad: int = field(default=0, compare=False)
    icono_path: Optional[str] = None

    def esta_disponible(self, stock: Stock) -> bool:
        pass