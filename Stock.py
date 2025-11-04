from Ingrediente import Ingrediente


class Stock:
    def __init__(self):
        self.lista_ingredientes = []
        
        #treeview
    def agregar_ingrediente(self, ingrediente): #Append
        
        for ing in self.lista_ingredientes:
            if ing.nombre.lower() == ingrediente.nombre.lower() and ing.unidad == ingrediente.unidad:
                ing.cantidad += ingrediente.cantidad
                print(f"Cantidad actualizada de '{ing.nombre}': {ing.cantidad}")
                return
        self.lista_ingredientes.append(ingrediente)
        print(f"Ingrediente '{ingrediente.nombre}' agregado.")

    def eliminar_ingrediente(self, nombre_ingrediente):
        encontrado = False
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre.lower() == nombre_ingrediente.lower():
                self.lista_ingredientes.remove(ingrediente)
                print(f"Ingrediente '{nombre_ingrediente}' eliminado.")
                encontrado = True
                break
        if not encontrado:
            print(f"Ingrediente '{nombre_ingrediente}' no encontrado.")
        return encontrado

    def verificar_stock(self, nombre_ingrediente):
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                print(f"Stock de '{nombre_ingrediente}': {ingrediente.cantidad}")
                return ingrediente.cantidad
        print(f"Ingrediente '{nombre_ingrediente}' no encontrado.")
        return None

    def actualizar_stock(self, nombre_ingrediente, nueva_cantidad):
        for ingrediente in self.lista_ingredientes:
            if ingrediente.nombre == nombre_ingrediente:
                ingrediente.cantidad = nueva_cantidad
                print(f"Stock de '{nombre_ingrediente}' actualizado a {nueva_cantidad}.")
                return True
        print(f"Ingrediente '{nombre_ingrediente}' no encontrado.")
        return False

    def obtener_elementos_menu(self):
        return [ingrediente.nombre for ingrediente in self.lista_ingredientes]

