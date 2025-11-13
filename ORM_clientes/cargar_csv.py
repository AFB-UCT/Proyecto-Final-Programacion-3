import pandas as pd
import sqlite3

# Lee el archivo CSV
df = pd.read_csv('ingredientes_menu.csv')

# Verifica si existen valores negativos en los ingredientes
numeric_cols = df.select_dtypes(include=['number']).columns

# Filtrar filas con valores negativos
negativos = df[(df[numeric_cols] < 0).any(axis=1)]

if not negativos.empty:
    print("Valores negativos encontrados:")
    print(negativos)
    # Eliminar las filas con valores negativos antes de guardar
    df = df[(df[numeric_cols] >= 0).all(axis=1)]
else:
    print("Ingredientes cargados")

# Conectar a la base de datos
conn = sqlite3.connect("PixelFood.db")

# Guardar los datos limpios en la tabla 'ingredientes'
df.to_sql('ingredientes', conn, if_exists='replace', index=False)

conn.commit()

conn.close()






