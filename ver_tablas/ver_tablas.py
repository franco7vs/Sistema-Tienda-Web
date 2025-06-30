import sqlite3

# Conectamos a la base de datos actual del sistema web
conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

# Ejecutamos una consulta para obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()

# Mostramos el nombre de cada tabla
print("Tablas en la base de datos:")
for tabla in tablas:
    print("-", tabla[0])

conn.close()
