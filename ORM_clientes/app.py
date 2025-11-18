# app.py (completo)
import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from database import session
from models import Cliente, Ingredientes, Menus, Pedido
from graficos import GraficosManager
import csv
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image, ImageTk
from functools import reduce

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RestaurantApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.session = session
        self.graficos_manager = GraficosManager()
        self.carrito_compras = []
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Sistema Restaurante - ORM")
        self.root.geometry("1200x700")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.setup_clientes_tab()
        self.setup_ingredientes_tab()
        self.setup_menus_tab()
        self.setup_pedidos_tab()
        self.setup_compras_tab()
        self.setup_estadisticas_tab()
        
        self.root.mainloop()
    
    # === PESTAÑA CLIENTES (MEJORADA) ===
    def setup_clientes_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Clientes")
        
        # Frame principal con dos columnas
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columna izquierda - Formulario
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Gestión de Clientes", font=('Arial', 16, 'bold')).pack(pady=10)
        
        form_frame = ctk.CTkFrame(left_frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre:").pack(anchor='w', pady=(5,0))
        self.cliente_nombre = ctk.CTkEntry(form_frame, width=200)
        self.cliente_nombre.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Email:").pack(anchor='w')
        self.cliente_email = ctk.CTkEntry(form_frame, width=200)
        self.cliente_email.pack(fill='x', pady=(0,10))
        
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frame, text="Agregar Cliente", command=self.agregar_cliente).pack(side='left', padx=(0,5))
        ctk.CTkButton(btn_frame, text="Limpiar Campos", command=self.limpiar_campos_clientes).pack(side='left')
        
        # Columna derecha - Lista
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        ctk.CTkLabel(right_frame, text="Lista de Clientes", font=('Arial', 14)).pack(pady=10)
        
        # Treeview con scrollbar
        tree_frame = ctk.CTkFrame(right_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Email', 'Pedidos')
        self.clientes_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.clientes_tree.heading(col, text=col)
            self.clientes_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.clientes_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botones de acción
        action_frame = ctk.CTkFrame(right_frame)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(action_frame, text="Actualizar Lista", command=self.cargar_clientes).pack(side='left', padx=5)
        ctk.CTkButton(action_frame, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side='left', padx=5)
        
        self.cargar_clientes()
    
    def agregar_cliente(self):
        nombre = self.cliente_nombre.get().strip()
        email = self.cliente_email.get().strip()
        
        if not nombre or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar formato de email usando filter
        if not list(filter(lambda x: '@' in x and '.' in x, [email])):
            messagebox.showerror("Error", "Formato de email inválido")
            return
        
        try:
            # Verificar email único usando filter
            clientes_existentes = self.session.query(Cliente).all()
            email_existente = list(filter(lambda c: c.email.lower() == email.lower(), clientes_existentes))
            
            if email_existente:
                messagebox.showerror("Error", "El email ya está registrado")
                return
                
            nuevo_cliente = Cliente(nombre=nombre, email=email)
            self.session.add(nuevo_cliente)
            self.session.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            self.limpiar_campos_clientes()
            self.cargar_clientes()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudo agregar el cliente: {str(e)}")
    
    def cargar_clientes(self):
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        try:
            clientes = self.session.query(Cliente).all()
            
            # Usando map para formatear los datos
            clientes_data = list(map(lambda c: (
                c.id, 
                c.nombre, 
                c.email, 
                len(c.pedidos)
            ), clientes))
            
            for cliente_data in clientes_data:
                self.clientes_tree.insert('', 'end', values=cliente_data)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}")
    
    def eliminar_cliente(self):
        seleccion = self.clientes_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        cliente_id = self.clientes_tree.item(seleccion[0])['values'][0]
        cliente_nombre = self.clientes_tree.item(seleccion[0])['values'][1]
        
        try:
            cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if cliente:
                # Validar que no tenga pedidos usando filter
                pedidos_cliente = list(filter(lambda p: p.cliente_id == cliente_id, cliente.pedidos))
                if pedidos_cliente:
                    messagebox.showerror("Error", "No se puede eliminar un cliente con pedidos asociados")
                    return
                    
                self.session.delete(cliente)
                self.session.commit()
                messagebox.showinfo("Éxito", f"Cliente {cliente_nombre} eliminado correctamente")
                self.cargar_clientes()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
    
    def limpiar_campos_clientes(self):
        self.cliente_nombre.delete(0, 'end')
        self.cliente_email.delete(0, 'end')
    
    # === PESTAÑA INGREDIENTES (MEJORADA) ===
    def setup_ingredientes_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Ingredientes")
        
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columna izquierda - Formulario
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Gestión de Ingredientes", font=('Arial', 16, 'bold')).pack(pady=10)
        
        form_frame = ctk.CTkFrame(left_frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre:").pack(anchor='w', pady=(5,0))
        self.ingrediente_nombre = ctk.CTkEntry(form_frame)
        self.ingrediente_nombre.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Cantidad:").pack(anchor='w')
        self.ingrediente_cantidad = ctk.CTkEntry(form_frame)
        self.ingrediente_cantidad.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Unidad:").pack(anchor='w')
        self.ingrediente_unidad = ctk.CTkEntry(form_frame)
        self.ingrediente_unidad.pack(fill='x', pady=(0,10))
        
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frame, text="Agregar Ingrediente", command=self.agregar_ingrediente).pack(side='left', padx=(0,5))
        ctk.CTkButton(btn_frame, text="Cargar desde CSV", command=self.cargar_ingredientes_csv).pack(side='left', padx=(0,5))
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_campos_ingredientes).pack(side='left')
        
        # Columna derecha - Lista
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        ctk.CTkLabel(right_frame, text="Inventario de Ingredientes", font=('Arial', 14)).pack(pady=10)
        
        tree_frame = ctk.CTkFrame(right_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Cantidad', 'Unidad')
        self.ingredientes_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.ingredientes_tree.heading(col, text=col)
            self.ingredientes_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.ingredientes_tree.yview)
        self.ingredientes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ingredientes_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_ingredientes()
    
    def agregar_ingrediente(self):
        nombre = self.ingrediente_nombre.get().strip()
        cantidad_str = self.ingrediente_cantidad.get().strip()
        unidad = self.ingrediente_unidad.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        try:
            cantidad = float(cantidad_str) if cantidad_str else 0.0
            if cantidad < 0:
                messagebox.showerror("Error", "La cantidad debe ser positiva")
                return
                
            # Verificar nombre único usando filter
            ingredientes_existentes = self.session.query(Ingredientes).all()
            nombre_existente = list(filter(lambda i: i.nombre.lower() == nombre.lower(), ingredientes_existentes))
            
            if nombre_existente:
                messagebox.showerror("Error", "El ingrediente ya existe")
                return
                
            nuevo_ingrediente = Ingredientes(nombre=nombre, cantidad=cantidad, unidad=unidad or None)
            self.session.add(nuevo_ingrediente)
            self.session.commit()
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente")
            self.limpiar_campos_ingredientes()
            self.cargar_ingredientes()
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudo agregar el ingrediente: {str(e)}")
    
    def cargar_ingredientes_csv(self):
        try:
            with open('ingredientes_menu.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Usando map para procesar las filas
                def procesar_fila(fila):
                    nombre = fila['nombre'].strip()
                    cantidad = float(fila['cantidad']) if fila['cantidad'] else 0.0
                    unidad = fila.get('unidad', '').strip() or None
                    
                    # Buscar si existe usando filter
                    existente = self.session.query(Ingredientes).filter(Ingredientes.nombre == nombre).first()
                    if existente:
                        existente.cantidad += cantidad
                        if unidad and not existente.unidad:
                            existente.unidad = unidad
                    else:
                        nuevo = Ingredientes(nombre=nombre, cantidad=cantidad, unidad=unidad)
                        self.session.add(nuevo)
                
                # Aplicar map a todas las filas
                list(map(procesar_fila, list(reader)))
                
                self.session.commit()
                messagebox.showinfo("Éxito", "Ingredientes cargados desde CSV")
                self.cargar_ingredientes()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudieron cargar los ingredientes: {str(e)}")
    
    def cargar_ingredientes(self):
        for item in self.ingredientes_tree.get_children():
            self.ingredientes_tree.delete(item)
        
        try:
            ingredientes = self.session.query(Ingredientes).all()
            
            # Usando map para formatear datos
            ingredientes_data = list(map(lambda i: (
                i.id, 
                i.nombre, 
                f"{i.cantidad} {i.unidad or ''}".strip(),
                i.unidad or "Sin unidad"
            ), ingredientes))
            
            for ingrediente_data in ingredientes_data:
                self.ingredientes_tree.insert('', 'end', values=ingrediente_data)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ingredientes: {str(e)}")
    
    def limpiar_campos_ingredientes(self):
        self.ingrediente_nombre.delete(0, 'end')
        self.ingrediente_cantidad.delete(0, 'end')
        self.ingrediente_unidad.delete(0, 'end')
    
    # === PESTAÑA MENÚS (COMPLETA) ===
    def setup_menus_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Menús")
        
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columna izquierda - Formulario
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Gestión de Menús", font=('Arial', 16, 'bold')).pack(pady=10)
        
        form_frame = ctk.CTkFrame(left_frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre del Menú:").pack(anchor='w', pady=(5,0))
        self.menu_nombre = ctk.CTkEntry(form_frame)
        self.menu_nombre.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Descripción:").pack(anchor='w')
        self.menu_descripcion = ctk.CTkEntry(form_frame)
        self.menu_descripcion.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Precio:").pack(anchor='w')
        self.menu_precio = ctk.CTkEntry(form_frame)
        self.menu_precio.pack(fill='x', pady=(0,10))
        
        ctk.CTkLabel(form_frame, text="Ingredientes (ID:cantidad, separados por coma):").pack(anchor='w')
        self.menu_ingredientes = ctk.CTkTextbox(form_frame, height=80)
        self.menu_ingredientes.pack(fill='x', pady=(0,10))
        
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frame, text="Crear Menú", command=self.crear_menu).pack(side='left', padx=(0,5))
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_campos_menu).pack(side='left')
        
        # Columna derecha - Lista
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        ctk.CTkLabel(right_frame, text="Menús Disponibles", font=('Arial', 14)).pack(pady=10)
        
        tree_frame = ctk.CTkFrame(right_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Descripción', 'Precio', 'Ingredientes')
        self.menus_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.menus_tree.heading(col, text=col)
            self.menus_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.menus_tree.yview)
        self.menus_tree.configure(yscrollcommand=scrollbar.set)
        
        self.menus_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_menus()
    
    def crear_menu(self):
        nombre = self.menu_nombre.get().strip()
        descripcion = self.menu_descripcion.get().strip()
        precio_str = self.menu_precio.get().strip()
        ingredientes_text = self.menu_ingredientes.get("1.0", "end").strip()
        
        if not nombre or not precio_str:
            messagebox.showerror("Error", "Nombre y precio son obligatorios")
            return
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return
            
            # Verificar nombre único
            menu_existente = self.session.query(Menus).filter(Menus.nombre == nombre).first()
            if menu_existente:
                messagebox.showerror("Error", "Ya existe un menú con ese nombre")
                return
            
            nuevo_menu = Menus(nombre=nombre, descripcion=descripcion, precio=precio)
            self.session.add(nuevo_menu)
            
            # Procesar ingredientes
            if ingredientes_text:
                lineas = ingredientes_text.split('\n')
                for linea in lineas:
                    if ':' in linea:
                        partes = linea.split(':')
                        if len(partes) == 2:
                            ingrediente_id = int(partes[0].strip())
                            cantidad = float(partes[1].strip())
                            
                            ingrediente = self.session.query(Ingredientes).filter(Ingredientes.id == ingrediente_id).first()
                            if ingrediente:
                                # Aquí necesitaríamos una tabla intermedia con cantidades
                                nuevo_menu.ingredientes.append(ingrediente)
                            else:
                                messagebox.showwarning("Advertencia", f"Ingrediente ID {ingrediente_id} no encontrado")
            
            self.session.commit()
            messagebox.showinfo("Éxito", "Menú creado correctamente")
            self.limpiar_campos_menu()
            self.cargar_menus()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudo crear el menú: {str(e)}")
    
    def cargar_menus(self):
        for item in self.menus_tree.get_children():
            self.menus_tree.delete(item)
        
        try:
            menus = self.session.query(Menus).all()
            for menu in menus:
                ingredientes = ", ".join([ing.nombre for ing in menu.ingredientes])
                self.menus_tree.insert('', 'end', values=(
                    menu.id, 
                    menu.nombre, 
                    menu.descripcion or "",
                    f"${menu.precio:.0f}",
                    ingredientes
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los menús: {str(e)}")
    
    def limpiar_campos_menu(self):
        self.menu_nombre.delete(0, 'end')
        self.menu_descripcion.delete(0, 'end')
        self.menu_precio.delete(0, 'end')
        self.menu_ingredientes.delete("1.0", "end")
    
    # === PESTAÑA PEDIDOS (COMPLETA) ===
    def setup_pedidos_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Pedidos")
        
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(main_frame, text="Historial de Pedidos", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Descripción', 'Cliente', 'Total', 'Fecha', 'Estado')
        self.pedidos_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.pedidos_tree.heading(col, text=col)
            self.pedidos_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.pedidos_tree.yview)
        self.pedidos_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pedidos_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Actualizar Lista", command=self.cargar_pedidos).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Ver Detalles", command=self.ver_detalles_pedido).pack(side='left', padx=5)
        
        self.cargar_pedidos()
    
    def cargar_pedidos(self):
        for item in self.pedidos_tree.get_children():
            self.pedidos_tree.delete(item)
        
        try:
            pedidos = self.session.query(Pedido).all()
            
            # Usando map para formatear datos
            pedidos_data = list(map(lambda p: (
                p.id,
                p.descripcion,
                p.cliente.nombre if p.cliente else "Sin cliente",
                f"${p.total:.0f}",
                p.fecha.strftime("%Y-%m-%d %H:%M"),
                p.estado
            ), pedidos))
            
            for pedido_data in pedidos_data:
                self.pedidos_tree.insert('', 'end', values=pedido_data)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los pedidos: {str(e)}")
    
    def ver_detalles_pedido(self):
        seleccion = self.pedidos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido para ver detalles")
            return
        
        pedido_id = self.pedidos_tree.item(seleccion[0])['values'][0]
        
        try:
            pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
            if pedido:
                detalles = f"Pedido ID: {pedido.id}\n"
                detalles += f"Descripción: {pedido.descripcion}\n"
                detalles += f"Cliente: {pedido.cliente.nombre if pedido.cliente else 'N/A'}\n"
                detalles += f"Total: ${pedido.total:.0f}\n"
                detalles += f"Fecha: {pedido.fecha.strftime('%Y-%m-%d %H:%M')}\n"
                detalles += f"Estado: {pedido.estado}\n"
                detalles += f"Menús: {', '.join([menu.nombre for menu in pedido.menus])}"
                
                messagebox.showinfo("Detalles del Pedido", detalles)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los detalles: {str(e)}")
    
    # === PESTAÑA COMPRAS (COMPLETA) ===
    def setup_compras_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Compras")
        
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame superior - Selección de cliente y menús
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(top_frame, text="Panel de Compras", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Selección de cliente
        cliente_frame = ctk.CTkFrame(top_frame)
        cliente_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(cliente_frame, text="Seleccionar Cliente:").pack(side='left', padx=(0,10))
        self.cliente_combo = ctk.CTkComboBox(cliente_frame, values=self.obtener_nombres_clientes(), width=200)
        self.cliente_combo.pack(side='left')
        
        # Selección de menú
        menu_frame = ctk.CTkFrame(top_frame)
        menu_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(menu_frame, text="Seleccionar Menú:").pack(side='left', padx=(0,10))
        self.menu_combo = ctk.CTkComboBox(menu_frame, values=self.obtener_nombres_menus(), width=200)
        self.menu_combo.pack(side='left', padx=(0,10))
        
        ctk.CTkLabel(menu_frame, text="Cantidad:").pack(side='left', padx=(0,10))
        self.cantidad_spinbox = ctk.CTkEntry(menu_frame, width=80)
        self.cantidad_spinbox.insert(0, "1")
        self.cantidad_spinbox.pack(side='left', padx=(0,10))
        
        ctk.CTkButton(menu_frame, text="Agregar al Carrito", command=self.agregar_al_carrito).pack(side='left')
        
        # Frame medio - Carrito
        middle_frame = ctk.CTkFrame(main_frame)
        middle_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(middle_frame, text="Carrito de Compras", font=('Arial', 14)).pack(pady=10)
        
        carrito_frame = ctk.CTkFrame(middle_frame)
        carrito_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Menú', 'Cantidad', 'Precio Unitario', 'Subtotal')
        self.carrito_tree = ttk.Treeview(carrito_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.carrito_tree.heading(col, text=col)
            self.carrito_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(carrito_frame, orient="vertical", command=self.carrito_tree.yview)
        self.carrito_tree.configure(yscrollcommand=scrollbar.set)
        
        self.carrito_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame inferior - Total y botones
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill='x', padx=10, pady=10)
        
        self.total_label = ctk.CTkLabel(bottom_frame, text="Total: $0", font=('Arial', 14, 'bold'))
        self.total_label.pack(side='left', padx=10)
        
        btn_frame = ctk.CTkFrame(bottom_frame)
        btn_frame.pack(side='right', padx=10)
        
        ctk.CTkButton(btn_frame, text="Limpiar Carrito", command=self.limpiar_carrito).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Generar Boleta", command=self.generar_boleta).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Procesar Compra", command=self.procesar_compra).pack(side='left', padx=5)
    
    def obtener_nombres_clientes(self):
        try:
            clientes = self.session.query(Cliente).all()
            return [f"{c.id}: {c.nombre}" for c in clientes]
        except:
            return []
    
    def obtener_nombres_menus(self):
        try:
            menus = self.session.query(Menus).all()
            return [f"{m.id}: {m.nombre} - ${m.precio:.0f}" for m in menus]
        except:
            return []
    
    def agregar_al_carrito(self):
        cliente_text = self.cliente_combo.get()
        menu_text = self.menu_combo.get()
        cantidad_text = self.cantidad_spinbox.get().strip()
        
        if not cliente_text or not menu_text:
            messagebox.showerror("Error", "Seleccione un cliente y un menú")
            return
        
        try:
            cantidad = int(cantidad_text)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            # Extraer ID del menú
            menu_id = int(menu_text.split(':')[0])
            menu = self.session.query(Menus).filter(Menus.id == menu_id).first()
            
            if not menu:
                messagebox.showerror("Error", "Menú no encontrado")
                return
            
            # Agregar al carrito
            item = {
                'menu_id': menu.id,
                'nombre': menu.nombre,
                'cantidad': cantidad,
                'precio_unitario': menu.precio,
                'subtotal': menu.precio * cantidad
            }
            
            self.carrito_compras.append(item)
            self.actualizar_carrito()
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar al carrito: {str(e)}")
    
    def actualizar_carrito(self):
        # Limpiar treeview
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        # Agregar items
        for item in self.carrito_compras:
            self.carrito_tree.insert('', 'end', values=(
                item['nombre'],
                item['cantidad'],
                f"${item['precio_unitario']:.0f}",
                f"${item['subtotal']:.0f}"
            ))
        
        # Calcular total usando reduce
        from functools import reduce
        total = reduce(lambda x, y: x + y['subtotal'], self.carrito_compras, 0)
        self.total_label.configure(text=f"Total: ${total:.0f}")
    
    def limpiar_carrito(self):
        self.carrito_compras.clear()
        self.actualizar_carrito()
    
    def generar_boleta(self):
        if not self.carrito_compras:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        cliente_text = self.cliente_combo.get()
        if not cliente_text:
            messagebox.showerror("Error", "Seleccione un cliente")
            return
        
        try:
            # Crear ventana de boleta
            boleta_window = ctk.CTkToplevel(self.root)
            boleta_window.title("Boleta de Compra")
            boleta_window.geometry("500x600")
            
            # Contenido de la boleta
            contenido = "=== BOLETA DE COMPRA ===\n\n"
            contenido += f"Cliente: {cliente_text}\n"
            contenido += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            contenido += "\n" + "="*40 + "\n"
            
            total = 0
            for item in self.carrito_compras:
                contenido += f"{item['nombre']}\n"
                contenido += f"  Cantidad: {item['cantidad']} x ${item['precio_unitario']:.0f} = ${item['subtotal']:.0f}\n"
                total += item['subtotal']
            
            contenido += "\n" + "="*40 + "\n"
            contenido += f"TOTAL: ${total:.0f}\n"
            contenido += "\n¡Gracias por su compra!"
            
            text_widget = ctk.CTkTextbox(boleta_window, width=480, height=550)
            text_widget.pack(padx=10, pady=10)
            text_widget.insert("1.0", contenido)
            text_widget.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar boleta: {str(e)}")
    
    def procesar_compra(self):
        if not self.carrito_compras:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        cliente_text = self.cliente_combo.get()
        if not cliente_text:
            messagebox.showerror("Error", "Seleccione un cliente")
            return
        
        try:
            # Extraer ID del cliente
            cliente_id = int(cliente_text.split(':')[0])
            cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
            
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado")
                return
            
            # Calcular total
            total = reduce(lambda x, y: x + y['subtotal'], self.carrito_compras, 0)
            
            # Crear pedido
            nuevo_pedido = Pedido(
                descripcion=f"Pedido de {cliente.nombre}",
                total=total,
                cliente_id=cliente_id,
                estado="completado"
            )
            
            self.session.add(nuevo_pedido)
            self.session.flush()  # Para obtener el ID
            
            # Agregar menús al pedido
            for item in self.carrito_compras:
                menu = self.session.query(Menus).filter(Menus.id == item['menu_id']).first()
                if menu:
                    nuevo_pedido.menus.append(menu)
            
            self.session.commit()
            
            messagebox.showinfo("Éxito", f"Compra procesada correctamente. Total: ${total:.0f}")
            self.limpiar_carrito()
            self.cargar_pedidos()
            
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Error al procesar compra: {str(e)}")
    
    # === PESTAÑA ESTADÍSTICAS (COMPLETA) ===
    def setup_estadisticas_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Estadísticas")
        
        main_frame = ctk.CTkFrame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(main_frame, text="Gráficos Estadísticos", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Controles de gráficos
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Seleccionar Gráfico:").pack(side='left', padx=(0,10))
        
        self.grafico_combo = ctk.CTkComboBox(controls_frame, values=[
            "Ventas Diarias",
            "Ventas Mensuales", 
            "Menús Populares",
            "Uso de Ingredientes"
        ], width=200)
        self.grafico_combo.pack(side='left', padx=(0,20))
        
        ctk.CTkButton(controls_frame, text="Generar Gráfico", command=self.mostrar_grafico).pack(side='left')
        
        # Área del gráfico
        self.grafico_frame = ctk.CTkFrame(main_frame)
        self.grafico_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.grafico_label = ctk.CTkLabel(self.grafico_frame, text="Seleccione un tipo de gráfico y haga clic en 'Generar Gráfico'", 
                                         font=('Arial', 12))
        self.grafico_label.pack(expand=True)
    
    def mostrar_grafico(self):
        tipo_grafico = self.grafico_combo.get()
        
        if not tipo_grafico:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de gráfico")
            return
        
        try:
            imagen_base64 = None
            
            if tipo_grafico == "Ventas Diarias":
                imagen_base64 = self.graficos_manager.generar_grafico_ventas_por_fecha('diario')
            elif tipo_grafico == "Ventas Mensuales":
                imagen_base64 = self.graficos_manager.generar_grafico_ventas_por_fecha('mensual')
            elif tipo_grafico == "Menús Populares":
                imagen_base64 = self.graficos_manager.generar_grafico_menus_populares()
            elif tipo_grafico == "Uso de Ingredientes":
                imagen_base64 = self.graficos_manager.generar_grafico_uso_ingredientes()
            
            if imagen_base64:
                self.mostrar_imagen_grafico(imagen_base64)
            else:
                self.grafico_label.configure(text="No hay datos suficientes para generar el gráfico")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
    
    def mostrar_imagen_grafico(self, imagen_base64):
        # Limpiar frame
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        
        # Decodificar imagen
        imagen_bytes = base64.b64decode(imagen_base64)
        imagen = Image.open(BytesIO(imagen_bytes))
        
        # Redimensionar si es muy grande
        ancho, alto = imagen.size
        if ancho > 800:
            ratio = 800 / ancho
            imagen = imagen.resize((800, int(alto * ratio)), Image.Resampling.LANCZOS)
        
        foto = ImageTk.PhotoImage(imagen)
        
        label = ctk.CTkLabel(self.grafico_frame, image=foto, text="")
        label.image = foto  # Mantener referencia
        label.pack(expand=True)

if __name__ == "__main__":
    app = RestaurantApp()