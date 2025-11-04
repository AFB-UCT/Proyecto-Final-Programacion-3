from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  
#-------------------------------
#----------CAMBIOS--------------
#-------------------------------
    def agregar_menu(self, menu: CrearMenu):
        for pedido_menu in self.menus:
            if pedido_menu.nombre == menu.nombre:
                pedido_menu.cantidad += 1
                return
        menu.cantidad = 1
        self.menus.append(menu)
#-------------------------------
#-------------------------------
#-------------------------------

    def eliminar_menu(self, nombre_menu: str):
        for menu in self.menus:
            if menu.nombre.lower() == nombre_menu.lower():
                self.menus.remove(menu)
                print(f"Menú '{nombre_menu}' eliminado del pedido.")
                return True
        print(f"Menú '{nombre_menu}' no encontrado en el pedido.")
        return False

    def mostrar_pedido(self):
        if not self.menus:
            print("No hay menús en el pedido.")
            return
        print("Menús en el pedido:")
        for menu in self.menus:
            print(f"- {menu.nombre} (${menu.precio})")

    def calcular_total(self) -> float:
        return sum(menu.precio * menu.cantidad for menu in self.menus)
