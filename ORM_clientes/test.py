from sqlalchemy import inspect
from database import Base, Engine, session
from models import Cliente, Ingredientes, Menus, Pedido
import os

# NOTA: AL EJECUTAR ESTE COMANDO TODOS LOS PARAMETROS DEL DATABASE SE RESETEAN, USAR CON PRECAUSION


def test_completo():
    print("🚀 INICIANDO TEST COMPLETO - CREACIÓN BD + DATOS + PRUEBAS")
    
    # 1. CREAR ARCHIVO FÍSICO PixelFood.db
    print("\n1. 🗃️ CREANDO ARCHIVO PixelFood.db...")
    
    if os.path.exists('PixelFood.db'):
        os.remove('PixelFood.db')
        print("🗑️  Archivo anterior eliminado")
    
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)
    
    if os.path.exists('PixelFood.db'):
        print(f"✅ PixelFood.db creada ({os.path.getsize('PixelFood.db')} bytes)")
    else:
        print("❌ Error: No se creó PixelFood.db")
        return
    
    inspector = inspect(Engine)
    print(f"📊 Tablas creadas: {inspector.get_table_names()}")
    
    # 2. POBLAR CON DATOS DE EJEMPLO
    print("\n2. 📥 POBLANDO BASE DE DATOS...")
    
    # Crear clientes
    cliente1 = Cliente(nombre="Ana García", email="ana123@outlook.com")
    cliente2 = Cliente(nombre="Carlos López", email="carlos@gmail.com") 
    cliente3 = Cliente(nombre="María Torres", email="maria000@gmail.com")
    session.add_all([cliente1, cliente2, cliente3])
    
    # Crear ingredientes
    ingredientes = [
        Ingredientes(nombre="Pan", unidad="unidad", cantidad=100),
        Ingredientes(nombre="Carne", unidad="kg", cantidad=50),
        Ingredientes(nombre="Queso", unidad="kg" ,cantidad=30),
        Ingredientes(nombre="Lechuga", unidad="kg" ,cantidad=40),
        Ingredientes(nombre="Tomate", unidad="kg", cantidad=25),
        Ingredientes(nombre="Cebolla", unidad="kg", cantidad=35),
        Ingredientes(nombre="Salsa", unidad="unidades", cantidad=60)
    ]
    session.add_all(ingredientes)
    
    # Crear menús
    hamburguesa = Menus(nombre="Hamburguesa Clásica")
    hamburguesa_especial = Menus(nombre="Hamburguesa Especial")
    sandwich = Menus(nombre="Sandwich Vegetariano")
    session.add_all([hamburguesa, hamburguesa_especial, sandwich])
    
    session.commit()
    print("✅ Datos básicos creados")
    
    # 3. ESTABLECER RELACIONES
    print("\n3. 🔗 ESTABLECIENDO RELACIONES...")
    
    # Obtener ingredientes
    pan = session.query(Ingredientes).filter_by(nombre="Pan").first()
    carne = session.query(Ingredientes).filter_by(nombre="Carne").first()
    queso = session.query(Ingredientes).filter_by(nombre="Queso").first()
    lechuga = session.query(Ingredientes).filter_by(nombre="Lechuga").first()
    tomate = session.query(Ingredientes).filter_by(nombre="Tomate").first()
    cebolla = session.query(Ingredientes).filter_by(nombre="Cebolla").first()
    salsa = session.query(Ingredientes).filter_by(nombre="Salsa").first()
    
    # Asignar ingredientes a menús
    hamburguesa.ingredientes.extend([pan, carne, queso, lechuga, tomate])
    hamburguesa_especial.ingredientes.extend([pan, carne, queso, lechuga, tomate, cebolla, salsa])
    sandwich.ingredientes.extend([pan, lechuga, tomate, cebolla, salsa])
    
    session.commit()
    print("✅ Relaciones menús-ingredientes establecidas")
    
    # 4. CREAR PEDIDOS COMPLETOS
    print("\n4. 🛒 CREANDO PEDIDOS COMPLETOS...")
    
    pedido1 = Pedido(nombre="Pedido de Ana", cantidad=2, precio=6500, cliente_id=cliente1.id)
    pedido2 = Pedido(nombre="Pedido de Carlos", cantidad=1, precio=3200, cliente_id=cliente2.id)
    
    # Asignar menús a pedidos
    pedido1.menus.extend([hamburguesa, hamburguesa_especial])
    pedido2.menus.extend([sandwich])
    
    session.add_all([pedido1, pedido2])
    session.commit()
    print("✅ Pedidos creados con relaciones")
    
    # 5. VERIFICAR TODO FUNCIONA
    print("\n5. ✅ VERIFICANDO INTEGRACIÓN COMPLETA...")
    
    # Verificar clientes y sus pedidos
    print(f"\n👥 CLIENTES Y SUS PEDIDOS:")
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(f"   {cliente.nombre}: {len(cliente.pedidos)} pedido(s)")
        for pedido in cliente.pedidos:
            print(f"      📦 {pedido.nombre} - ${pedido.precio}")
            for menu in pedido.menus:
                print(f"         🍽️  {menu.nombre}")
    
    # Verificar menús y sus ingredientes
    print(f"\n🍽️  MENÚS Y INGREDIENTES:")
    menus = session.query(Menus).all()
    for menu in menus:
        print(f"   {menu.nombre}: {len(menu.ingredientes)} ingredientes")
        for ing in menu.ingredientes:
            print(f"      🥬 {ing.nombre} (stock: {ing.cantidad})")
    
    # Verificar stock total
    print(f"\n📦 INVENTARIO ACTUAL:")
    ingredientes = session.query(Ingredientes).all()
    for ing in ingredientes:
        print(f"   {ing.nombre}: {ing.cantidad} unidades")
    
    # 6. VERIFICAR ARCHIVO FÍSICO
    print(f"\n6. 📁 VERIFICANDO ARCHIVO FÍSICO...")
    if os.path.exists('PixelFood.db'):
        stats = os.stat('PixelFood.db')
        print(f"✅ PixelFood.db existe")
        print(f"   📏 Tamaño: {stats.st_size} bytes")
        print(f"   📅 Creado: {stats.st_ctime}")
        print(f"   ✏️  Modificado: {stats.st_mtime}")
    else:
        print("❌ PixelFood.db no existe")
    
    session.close()
    
    print(f"\n🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
    print(f"   La base de datos PixelFood.db está lista para usar con tu aplicación")
    print(f"   Ejecuta 'python app.py' para usar el sistema completo")

if __name__ == '__main__':
    test_completo()