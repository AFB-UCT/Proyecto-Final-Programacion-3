# test.py (actualizado para usar el nuevo pedido_crud)
from sqlalchemy import inspect
from database import Base, Engine, session
from models import Cliente, Ingredientes, Menus, Pedido
from crud.pedido_crud import crear_pedido, agregar_menu_a_pedido
import os

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
    session.commit()
    
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
    hamburguesa = Menus(nombre="Hamburguesa Clásica", descripcion="Deliciosa hamburguesa con carne, queso y vegetales", precio=6500)
    hamburguesa_especial = Menus(nombre="Hamburguesa Especial", descripcion="Hamburguesa premium con todos los ingredientes", precio=8500)
    sandwich = Menus(nombre="Sandwich Vegetariano", descripcion="Sandwich saludable con vegetales frescos", precio=4500)
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
    
    # 4. CREAR PEDIDOS COMPLETOS USANDO EL CRUD
    print("\n4. 🛒 CREANDO PEDIDOS COMPLETOS...")
    
    try:
        # Crear pedidos usando el CRUD
        pedido1 = crear_pedido(
            descripcion="Pedido de Ana - Hamburguesas", 
            total=15000, 
            cliente_id=cliente1.id,
            estado="completado"
        )
        
        pedido2 = crear_pedido(
            descripcion="Pedido de Carlos - Sandwich", 
            total=4500, 
            cliente_id=cliente2.id,
            estado="completado"
        )
        
        # Agregar menús a los pedidos usando el CRUD
        agregar_menu_a_pedido(pedido1.id, hamburguesa.id)
        agregar_menu_a_pedido(pedido1.id, hamburguesa_especial.id)
        agregar_menu_a_pedido(pedido2.id, sandwich.id)
        
        print("✅ Pedidos creados con relaciones usando CRUD")
        
    except Exception as e:
        print(f"❌ Error creando pedidos: {e}")
        return
    
    # 5. VERIFICAR TODO FUNCIONA
    print("\n5. ✅ VERIFICANDO INTEGRACIÓN COMPLETA...")
    
    # Verificar clientes y sus pedidos
    print(f"\n👥 CLIENTES Y SUS PEDIDOS:")
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(f"   {cliente.nombre} ({cliente.email}): {len(cliente.pedidos)} pedido(s)")
        for pedido in cliente.pedidos:
            print(f"      📦 {pedido.descripcion} - ${pedido.total} - {pedido.estado}")
            for menu in pedido.menus:
                print(f"         🍽️  {menu.nombre} - ${menu.precio}")
    
    # Verificar menús y sus ingredientes
    print(f"\n🍽️  MENÚS Y INGREDIENTES:")
    menus = session.query(Menus).all()
    for menu in menus:
        print(f"   {menu.nombre} (${menu.precio}): {len(menu.ingredientes)} ingredientes")
        for ing in menu.ingredientes:
            print(f"      🥬 {ing.nombre} (stock: {ing.cantidad} {ing.unidad})")
    
    # Verificar stock total
    print(f"\n📦 INVENTARIO ACTUAL:")
    ingredientes = session.query(Ingredientes).all()
    for ing in ingredientes:
        print(f"   {ing.nombre}: {ing.cantidad} {ing.unidad}")
    
    # 6. VERIFICAR ARCHIVO FÍSICO
    print(f"\n6. 📁 VERIFICANDO ARCHIVO FÍSICO...")
    if os.path.exists('PixelFood.db'):
        stats = os.stat('PixelFood.db')
        print(f"✅ PixelFood.db existe")
        print(f"   📏 Tamaño: {stats.st_size} bytes")
    else:
        print("❌ PixelFood.db no existe")
    
    session.close()
    
    print(f"\n🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
    print(f"   La base de datos PixelFood.db está lista para usar con tu aplicación")
    print(f"   Ejecuta 'python app.py' para usar el sistema completo")

if __name__ == '__main__':
    test_completo()