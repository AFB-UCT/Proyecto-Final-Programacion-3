# graficos.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from database import session
from models import Pedido, Menus, Cliente
from sqlalchemy import func, extract
import io
import base64
from collections import Counter

class GraficosManager:
    def __init__(self):
        self.session = session
    
    def generar_grafico_ventas_por_fecha(self, periodo='diario'):
        """Genera gráfico de ventas por fecha"""
        try:
            pedidos = self.session.query(Pedido).all()
            
            if not pedidos:
                return None
            
            # Usando map y filter para procesar datos
            fechas = list(map(lambda p: p.fecha.date(), pedidos))
            totales = list(map(lambda p: p.total, pedidos))
            
            if periodo == 'diario':
                contador = Counter(fechas)
                fechas_unicas = sorted(contador.keys())
                ventas = [contador[fecha] for fecha in fechas_unicas]
                
                plt.figure(figsize=(10, 6))
                plt.bar(fechas_unicas, ventas)
                plt.title('Ventas Diarias')
                plt.xlabel('Fecha')
                plt.ylabel('Número de Pedidos')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
            elif periodo == 'mensual':
                meses = list(map(lambda f: f.strftime('%Y-%m'), fechas))
                contador = Counter(meses)
                meses_unicos = sorted(contador.keys())
                ventas = [contador[mes] for mes in meses_unicos]
                
                plt.figure(figsize=(10, 6))
                plt.bar(meses_unicos, ventas)
                plt.title('Ventas Mensuales')
                plt.xlabel('Mes')
                plt.ylabel('Número de Pedidos')
                plt.xticks(rotation=45)
                plt.tight_layout()
            
            # Convertir gráfico a imagen base64
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            return base64.b64encode(img.getvalue()).decode()
            
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            return None
    
    def generar_grafico_menus_populares(self):
        """Genera gráfico de menús más comprados"""
        try:
            pedidos = self.session.query(Pedido).all()
            
            if not pedidos:
                return None
            
            # Usando reduce para contar menús
            from functools import reduce
            todos_menus = reduce(lambda x, y: x + y, 
                               [pedido.menus for pedido in pedidos], [])
            
            nombres_menus = list(map(lambda m: m.nombre, todos_menus))
            contador = Counter(nombres_menus)
            
            if not contador:
                return None
            
            menus = list(contador.keys())
            cantidades = list(contador.values())
            
            plt.figure(figsize=(10, 6))
            plt.bar(menus, cantidades)
            plt.title('Menús Más Comprados')
            plt.xlabel('Menú')
            plt.ylabel('Cantidad Vendida')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            return base64.b64encode(img.getvalue()).decode()
            
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            return None
    
    def generar_grafico_uso_ingredientes(self):
        """Genera gráfico de uso de ingredientes"""
        try:
            from models import menus_ingredientes, Ingredientes
            from sqlalchemy import select
            
            # Consulta para obtener uso de ingredientes
            resultado = self.session.execute(
                select([Ingredientes.nombre, func.sum(menus_ingredientes.c.cantidad_requerida)])
                .select_from(menus_ingredientes.join(Ingredientes))
                .group_by(Ingredientes.nombre)
            ).fetchall()
            
            if not resultado:
                return None
            
            ingredientes = list(map(lambda x: x[0], resultado))
            usos = list(map(lambda x: x[1] or 0, resultado))
            
            plt.figure(figsize=(10, 6))
            plt.pie(usos, labels=ingredientes, autopct='%1.1f%%')
            plt.title('Uso de Ingredientes en Menús')
            plt.tight_layout()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            return base64.b64encode(img.getvalue()).decode()
            
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            return None