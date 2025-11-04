# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa","unid", 1),
                Ingrediente("Pan de completo","unid", 1),
                Ingrediente("Palta","kg",0.5),
                Ingrediente("Tomate","kg",0.2),
            ],
            precio=1800,
            icono_path="IMG/icono_hotdog_sin_texto_64x64.png",
        ),
    
        CrearMenu(
                nombre="Papas Fritas",
                ingredientes=[Ingrediente("Papas", "kg", 5)],
                precio=500,
                icono_path="IMG/icono_papas_fritas_64x64.png"
        ),
        CrearMenu(
                nombre="Pepsi",
                ingredientes=[Ingrediente("Pepsi", "unid", 1)],
                precio=1100,
                icono_path="IMG/icono_cola_64x64.png"
        ),
        CrearMenu(
                nombre="Coca-Cola",
                ingredientes=[Ingrediente("Coca cola", "unid", 1)],
                precio=1100,
                icono_path="IMG/icono_cola_lata_64x64.png"
        ),
        CrearMenu(
                nombre="Hamburguesa",
                ingredientes=[
                    Ingrediente("Pan de Hamburguesa", "unid", 1),
                    Ingrediente("Lamina de queso", "unid", 1),
                    Ingrediente("Churrasco de carne", "unid", 1)
                ],
                precio=3500,
                icono_path="IMG/icono_hamburguesa_negra_64x64.png"    
        ),
        CrearMenu(
                nombre="Pollo Frito",
                ingredientes=[
                    Ingrediente("Presa de pollo", "kg", 1),
                    Ingrediente("Porcion de harina", "kg", 1),
                    Ingrediente("Porcion de aceite", "unid", 1)
                ],
                precio=2800,
                icono_path="IMG/icono_pollo_frito_64x64.png"
        ),
        CrearMenu(
                nombre="Ensalada mixta",
                ingredientes=[
                    Ingrediente("Lechuga", "unid", 1),
                    Ingrediente("Tomate", "kg", 1),
                    Ingrediente("Zanahoria rallada", "kg", 1)
                ],
                precio=1500,
                icono_path="IMG/icono_ensalada_mixta_64x64.png"
                
        ),
        CrearMenu(
                nombre="Empanada de Queso",
                ingredientes=[
                    Ingrediente("Masa de empanada", "unid", 1),
                    Ingrediente("Queso", "kg", 1)
                ],
                precio=1000,
                icono_path="IMG/icono_empanada_queso_64x64.png"
        ),
        CrearMenu(
                nombre="Chorrillana",
                ingredientes=[
                    Ingrediente("Papas", "kg", 5),
                    Ingrediente("Vienesa", "unid", 3),
                    Ingrediente("Huevos", "unid", 2)
                ],
                precio=3000,
                icono_path="IMG/icono_chorrillana_64x64.png"
        ),
        CrearMenu(
                nombre="Panqueques con Manjar",
                ingredientes=[
                    Ingrediente("Masa", "unid", 1),
                    Ingrediente("Panqueque", "unid", 3),
                    Ingrediente("Manjar", "kg", 1)
                ],
                precio=2000,
                icono_path="IMG/icono_panqueques_con_manjar_64x64.png"
        )
            
]

