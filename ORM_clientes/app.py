import customtkinter as ctk
from tkinter import ttk, messagebox
from database import session
from models import Cliente, Ingredientes, Menus, Pedido
import csv

class RestaurantApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.session = session
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Sistema Restaurante - ORM")
        self.root.geometry("1200x700")
        
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.setup_clientes_tab()
        self.setup_ingredientes_tab()
        self.setup_menus_tab()
        self.setup_pedidos_tab()
        self.setup_compras_tab()
        self.setup_estadisticas_tab()
        
        self.root.mainloop()
    
    # === PESTAÑA CLIENTES ===
    def setup_clientes_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Clientes")
        
        # Frame superior - Formulario
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Gestión de Clientes", font=('Arial', 16, 'bold')).pack(pady=5)
        
        # Campos de entrada
        input_frame = ctk.CTkFrame(form_frame)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cliente_nombre = ctk.CTkEntry(input_frame, width=200)
        self.cliente_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Agregar Cliente", command=self.agregar_cliente).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar Campos", command=self.limpiar_campos_clientes).pack(side='left', padx=5)
        
        # Frame inferior - Lista
        list_frame = ctk.CTkFrame(frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Lista de Clientes", font=('Arial', 14)).pack(pady=5)
        
        # Treeview
        columns = ('ID', 'Nombre')
        self.clientes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.clientes_tree.heading(col, text=col)
            self.clientes_tree.column(col, width=100)
        
        self.clientes_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones de acción
        action_frame = ctk.CTkFrame(list_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ctk.CTkButton(action_frame, text="Actualizar Lista", command=self.cargar_clientes).pack(side='left', padx=5)
        ctk.CTkButton(action_frame, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side='left', padx=5)
        
        self.cargar_clientes()
    
    def agregar_cliente(self):
        nombre = self.cliente_nombre.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        try:
            nuevo_cliente = Cliente(nombre=nombre)
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
            for cliente in clientes:
                self.clientes_tree.insert('', 'end', values=(cliente.id, cliente.nombre))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}")
    
    def eliminar_cliente(self):
        seleccion = self.clientes_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        cliente_id = self.clientes_tree.item(seleccion[0])['values'][0]
        
        try:
            cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if cliente:
                self.session.delete(cliente)
                self.session.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_clientes()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
    
    def limpiar_campos_clientes(self):
        self.cliente_nombre.delete(0, 'end')
    
    # === PESTAÑA INGREDIENTES ===
    def setup_ingredientes_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Ingredientes")
        
        # Frame superior - Formulario
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Gestión de Ingredientes", font=('Arial', 16, 'bold')).pack(pady=5)
        
        input_frame = ctk.CTkFrame(form_frame)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ingrediente_nombre = ctk.CTkEntry(input_frame, width=200)
        self.ingrediente_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.ingrediente_cantidad = ctk.CTkEntry(input_frame, width=200)
        self.ingrediente_cantidad.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Agregar Ingrediente", command=self.agregar_ingrediente).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Cargar desde CSV", command=self.cargar_ingredientes_csv).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar_campos_ingredientes).pack(side='left', padx=5)
        
        # Lista de ingredientes
        list_frame = ctk.CTkFrame(frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Cantidad')
        self.ingredientes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.ingredientes_tree.heading(col, text=col)
            self.ingredientes_tree.column(col, width=100)
        
        self.ingredientes_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.cargar_ingredientes()
    
    def agregar_ingrediente(self):
        nombre = self.ingrediente_nombre.get().strip()
        cantidad = self.ingrediente_cantidad.get().strip()
        
        if not nombre or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                messagebox.showerror("Error", "La cantidad debe ser positiva")
                return
                
            nuevo_ingrediente = Ingredientes(nombre=nombre, cantidad=cantidad)
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
            with open('ingredientes.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    ingrediente = Ingredientes(
                        nombre=row['nombre'],
                        cantidad=int(row['cantidad'])
                    )
                    self.session.add(ingrediente)
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
            for ingrediente in ingredientes:
                self.ingredientes_tree.insert('', 'end', values=(
                    ingrediente.id, ingrediente.nombre, ingrediente.cantidad
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ingredientes: {str(e)}")
    
    def limpiar_campos_ingredientes(self):
        self.ingrediente_nombre.delete(0, 'end')
        self.ingrediente_cantidad.delete(0, 'end')
    
    # === PESTAÑAS RESTANTES ===
    def setup_menus_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Menús")
        ctk.CTkLabel(frame, text="Gestión de Menús - En desarrollo").pack(pady=20)
    
    def setup_pedidos_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Pedidos")
        ctk.CTkLabel(frame, text="Gestión de Pedidos - En desarrollo").pack(pady=20)
    
    def setup_compras_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Compras")
        ctk.CTkLabel(frame, text="Panel de Compras - En desarrollo").pack(pady=20)
    
    def setup_estadisticas_tab(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Estadísticas")
        ctk.CTkLabel(frame, text="Gráficos Estadísticos - En desarrollo").pack(pady=20)

if __name__ == "__main__":
    app = RestaurantApp()