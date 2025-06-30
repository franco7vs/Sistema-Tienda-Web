import sqlite3

conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT,
    telefono TEXT,
    direccion TEXT
)
""")

conn.commit()
conn.close()

print("Tabla 'clientes' creada o ya existía.")
